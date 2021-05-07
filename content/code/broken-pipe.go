package main

// For posterity:
//
// $ go version
// go version go1.15.3 darwin/amd64
//
// $ git --git-dir ${GOPATH}/src/github.com/spf13/cobra/.git log -1 --pretty=%H
// 08c51e585ca78e4b9408ae034d0cdacdd81aad41
//
// $ git --git-dir ${GOPATH}/src/github.com/lib/pq/.git log -1 --pretty=%H
// e7751f584844fbf92a5a18b13a0af1c855e34460
// $ git --git-dir ${GOPATH}/src/github.com/lib/pq/.git tag --points-at HEAD
// v1.8.0

import (
	"context"
	"database/sql"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"time"

	_ "github.com/lib/pq"
	"github.com/spf13/cobra"
)

const (
	dsnTemplate   = "postgres://superuser:password@localhost:%s/superuser_db?sslmode=disable"
	stateFilename = "./state.txt"
)

func setState(filename, state string) error {
	log.Printf("Setting state to %s\n", state)
	return ioutil.WriteFile(filename, []byte(state), 0644)
}

func makeRootCommand() (*cobra.Command, error) {
	port := ""
	cmd := &cobra.Command{
		Use:           "sql-broken-pipe",
		Short:         "Trigger two SQL queries, setting a statefile to IDLE in between",
		SilenceErrors: true,
		SilenceUsage:  true,
		RunE: func(_ *cobra.Command, _ []string) error {
			dsn := fmt.Sprintf(dsnTemplate, port)
			return executeStatements(dsn, stateFilename)
		},
	}

	cmd.PersistentFlags().StringVar(
		&port,
		"port",
		"",
		"The port to use when connecting to PostgreSQL",
	)

	return cmd, nil
}

func executeStatements(dsn, stateFile string) error {
	ctx := context.Background()

	pool, err := sql.Open("postgres", dsn)
	if err != nil {
		return err
	}
	// Ensure exactly 1 connection is in the pool.
	pool.SetMaxIdleConns(1)
	pool.SetMaxOpenConns(1)

	err = setState(stateFile, "ACTIVE")
	if err != nil {
		return err
	}

	err = pool.PingContext(ctx)
	if err != nil {
		return err
	}

	_, err = pool.ExecContext(ctx, "SELECT 1")
	if err != nil {
		return err
	}

	err = setState(stateFile, "IDLE")
	if err != nil {
		return err
	}

	log.Println("Sleeping for 1 second")
	time.Sleep(time.Second)
	log.Println("Done sleeping")

	_, err = pool.ExecContext(ctx, "SELECT 1")
	if err != nil {
		return err
	}

	return setState(stateFile, "COMPLETE")
}

func run() error {
	log.SetFlags(
		log.Ltime | log.Lmicroseconds | log.LUTC,
	)

	cmd, err := makeRootCommand()
	if err != nil {
		return err
	}

	return cmd.Execute()
}

func main() {
	err := run()
	if err != nil {
		log.Printf("%v\n", err)
		os.Exit(1)
	}
}
