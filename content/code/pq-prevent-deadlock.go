package main

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"log"
	"os"
	"sync"
	"time"

	multierror "github.com/hashicorp/go-multierror"
	_ "github.com/lib/pq"
)

const (
	dropTable     = "DROP TABLE IF EXISTS might_deadlock;"
	createTable   = "CREATE TABLE might_deadlock ( counter INTEGER NOT NULL, key TEXT NOT NULL );"
	tableSeedData = "INSERT INTO might_deadlock (counter, key) VALUES (4, 'hello'), (7, 'world'), (10, 'hello'), (5, 'world'), (3, 'world');"
)

type LogWriter struct {
	Start time.Time
}

func (lw LogWriter) Write(bytes []byte) (int, error) {
	d := time.Since(lw.Start)
	s := float64(d) / float64(time.Second)
	return fmt.Printf("%f %s", s, string(bytes))
}

func newLogWriter() LogWriter {
	return LogWriter{Start: time.Now().UTC()}
}

type Config struct {
	LockTimeout    time.Duration
	ContextTimeout time.Duration
}

func (cfg *Config) Parse() error {
	var err error
	cfg.LockTimeout, err = time.ParseDuration(os.Getenv("LOCK_TIMEOUT"))
	if err != nil {
		return err
	}

	cfg.ContextTimeout, err = time.ParseDuration(os.Getenv("CONTEXT_TIMEOUT"))
	if err != nil {
		return err
	}

	return nil
}

func createPool(ctx context.Context, cfg *Config) (*sql.DB, error) {
	dsnTemplate := "postgres://superuser:testpassword_superuser@localhost:28007/superuser_db?lock_timeout=%s&sslmode=disable"
	dsn := fmt.Sprintf(dsnTemplate, cfg.LockTimeout)
	pool, err := sql.Open("postgres", dsn)
	if err != nil {
		return nil, err
	}
	err = pool.PingContext(ctx)
	if err != nil {
		return nil, err
	}

	return pool, nil
}

func ignoreConnDone(err error) error {
	if err == sql.ErrConnDone {
		return nil
	}
	return err
}

func cleanUp(pool *sql.DB) {
	err := ignoreConnDone(pool.Close())
	if err != nil {
		log.Fatal(err)
	}
}

func seedDatabase(ctx context.Context, pool *sql.DB) error {
	_, err := pool.ExecContext(ctx, dropTable)
	if err != nil {
		return err
	}

	_, err = pool.ExecContext(ctx, createTable)
	if err != nil {
		return err
	}

	_, err = pool.ExecContext(ctx, tableSeedData)
	return err
}

func ignoreTxDone(err error) error {
	if err == sql.ErrTxDone {
		return nil
	}
	return err
}

func appendErr(err1, err2 error) error {
	err := multierror.Append(err1, err2)
	if len(err.Errors) == 0 {
		return nil
	}
	return err
}

func txFinalize(tx *sql.Tx, err error) error {
	if tx == nil {
		return err
	}

	rollbackErr := ignoreTxDone(tx.Rollback())
	return appendErr(err, rollbackErr)
}

// contendReads introduces two reads (in a transaction) with a sleep in
// between.
// H/T to https://www.citusdata.com/blog/2018/02/22/seven-tips-for-dealing-with-postgres-locks/
// for the idea on how to "easily" introduce a deadlock.
func contendReads(ctx context.Context, tx *sql.Tx, key1, key2 string, cfg *Config) error {
	updateRows := "UPDATE might_deadlock SET counter = counter + 1 WHERE key = $1;"
	_, err := tx.ExecContext(ctx, updateRows, key1)
	if err != nil {
		return err
	}

	time.Sleep(200 * time.Millisecond)
	_, err = tx.ExecContext(ctx, updateRows, key2)
	return err
}

func intentionalContention(ctx context.Context, pool *sql.DB, cfg *Config) (err error) {
	var tx1, tx2 *sql.Tx
	defer func() {
		err = txFinalize(tx1, err)
		err = txFinalize(tx2, err)
	}()

	log.Println("Starting transactions")
	tx1, err = pool.BeginTx(ctx, nil)
	if err != nil {
		return
	}
	tx2, err = pool.BeginTx(ctx, nil)
	if err != nil {
		return
	}
	log.Println("Transactions opened")

	// Kick off two goroutines that contend with each other.
	wg := sync.WaitGroup{}
	wg.Add(2)
	var contendErr1, contendErr2 error
	go func() {
		defer wg.Done()
		contendErr1 = contendReads(ctx, tx1, "hello", "world", cfg)
	}()
	go func() {
		defer wg.Done()
		contendErr2 = contendReads(ctx, tx2, "world", "hello", cfg)
	}()
	wg.Wait()

	err = appendErr(err, contendErr1)
	err = appendErr(err, contendErr2)

	// Make sure to commit both transactions before moving on.
	if contendErr1 == nil {
		err = appendErr(err, tx1.Commit())
	}

	if contendErr2 == nil {
		err = appendErr(err, tx2.Commit())
	}

	return
}

func displayError(err error) error {
	asMulti, ok := err.(*multierror.Error)
	if !ok {
		return err
	}

	if asMulti == nil || len(asMulti.Errors) == 0 {
		return errors.New("Expected a non-nil / non-empty error")
	}

	log.Println("Error(s):")
	for _, err := range asMulti.Errors {
		log.Printf("- %#v\n", err)
	}

	return nil
}

func main() {
	log.SetFlags(0)
	log.SetOutput(newLogWriter())

	// 1. Set the configuration from the environment.
	cfg := &Config{}
	err := cfg.Parse()
	if err != nil {
		log.Fatal(err)
	}

	// 2. Use the configured timeout to create a context with a deadline.
	deadline := time.Now().Add(cfg.ContextTimeout)
	ctx, cancel := context.WithDeadline(context.Background(), deadline)
	defer cancel()

	// 3. Create a mostly hardcoded connection string and open a connection pool.
	pool, err := createPool(ctx, cfg)
	if err != nil {
		log.Fatal(err)
	}
	defer cleanUp(pool)

	// 4. Create a table schema and insert data to seed the database.
	err = seedDatabase(ctx, pool)
	if err != nil {
		log.Fatal(err)
	}

	// 5. Create two goroutines that intentionally contend with transactions.
	err = intentionalContention(ctx, pool, cfg)
	if err == nil {
		log.Fatal(errors.New("Expected lock contention to occur"))
	}

	// 6. Display the error / errors in as verbose a way as possible.
	err = displayError(err)
	if err != nil {
		log.Fatal(err)
	}
}
