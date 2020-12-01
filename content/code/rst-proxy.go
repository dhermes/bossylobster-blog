package main

// For posterity:
//
// $ go version
// go version go1.15.3 darwin/amd64
//
// $ git --git-dir ${GOPATH}/src/github.com/hashicorp/go-multierror/.git log -1 --pretty=%H
// 0d28cf682dbe774898e42a3db11b7ce24b36751a

import (
	"io"
	"io/ioutil"
	"log"
	"net"
	"os"
	"sync"
	"syscall"
	"time"

	multierror "github.com/hashicorp/go-multierror"
)

const (
	dbAddr             = "localhost:13370"
	proxyAddr          = "localhost:23370"
	readTimeout        = 250 * time.Millisecond
	stateCheckInterval = 100 * time.Millisecond
	stateFilename      = "./state.json"
)

type setLingerForRST struct {
	Err error
}

func (slfr *setLingerForRST) Control(fd uintptr) {
	// No-op if already errored on a previous usage.
	if slfr.Err != nil {
		return
	}

	slfr.Err = syscall.SetsockoptLinger(
		int(fd),
		syscall.SOL_SOCKET,
		syscall.SO_LINGER,
		&syscall.Linger{Onoff: 1, Linger: 0},
	)
}

func setRSTSockopt(tc *net.TCPConn) error {
	sc, err := tc.SyscallConn()
	if err != nil {
		return err
	}

	slfr := &setLingerForRST{}
	err = sc.Control(slfr.Control)
	if err != nil {
		return err
	}

	return slfr.Err
}

func appendErrs(errs ...error) error {
	if len(errs) == 0 {
		return nil
	}
	combined := multierror.Append(errs[0], errs[1:]...)
	if len(combined.Errors) == 0 {
		return nil
	}
	return combined
}

func isTimeout(err error) bool {
	noe, ok := err.(*net.OpError)
	if !ok {
		return false
	}

	return noe.Timeout()
}

type forwardState struct {
	Mutex  sync.Mutex
	Errors []error
	Done   bool
}

func (fs *forwardState) AddError(err error) {
	fs.Mutex.Lock()
	defer fs.Mutex.Unlock()
	fs.Errors = append(fs.Errors, err)
	fs.Done = true
}

func (fs *forwardState) IsDone() bool {
	fs.Mutex.Lock()
	defer fs.Mutex.Unlock()
	return fs.Done
}

func (fs *forwardState) MarkDone() {
	fs.Mutex.Lock()
	defer fs.Mutex.Unlock()
	fs.Done = true
}

func forward(wg *sync.WaitGroup, r, w *net.TCPConn, fs *forwardState) {
	defer wg.Done()

	data := make([]byte, 4096)
	for {
		if fs.IsDone() {
			return
		}

		readDeadline := time.Now().Add(readTimeout)
		err := r.SetReadDeadline(readDeadline)
		if err != nil {
			fs.AddError(err)
			return
		}

		n, err := r.Read(data)
		if err == io.EOF {
			fs.MarkDone()
			return
		}
		if err != nil {
			if isTimeout(err) {
				continue
			}
			fs.AddError(err)
			return
		}

		_, err = w.Write(data[:n])
		if err != nil {
			fs.AddError(err)
			return
		}
	}
}

func pollStateFile(wg *sync.WaitGroup, fs *forwardState) {
	defer wg.Done()

	for {
		if fs.IsDone() {
			return
		}

		stateBytes, err := ioutil.ReadFile(stateFilename)
		if err != nil {
			fs.AddError(err)
			return
		}

		state := string(stateBytes)
		if state == "IDLE" {
			log.Println("State file switched to IDLE, closing connection")
			fs.MarkDone()
		}

		time.Sleep(stateCheckInterval)
	}
}

func proxy(tc *net.TCPConn) (err error) {
	addr, err := net.ResolveTCPAddr("tcp", dbAddr)
	if err != nil {
		return
	}

	// Create a server connection as well
	sc, err := net.DialTCP("tcp", nil, addr)
	if err != nil {
		return
	}
	defer func() {
		err = appendErrs(err, sc.Close())
	}()

	wg := sync.WaitGroup{}
	wg.Add(3)
	fs := forwardState{}
	go forward(&wg, tc, sc, &fs)
	go forward(&wg, sc, tc, &fs)
	go pollStateFile(&wg, &fs)
	wg.Wait()

	err = appendErrs(fs.Errors...)
	return
}

func run() error {
	log.SetFlags(
		log.Ltime | log.Lmicroseconds | log.LUTC,
	)

	addr, err := net.ResolveTCPAddr("tcp", proxyAddr)
	if err != nil {
		return err
	}

	log.Printf("Setting up TCP proxy on %s\n", proxyAddr)
	listener, err := net.ListenTCP("tcp", addr)
	if err != nil {
		return err
	}

	// Handle exactly one connection (we don't need a second connection to
	// reproduce the error).
	tc, err := listener.AcceptTCP()
	if err != nil {
		return err
	}
	log.Printf("Handling TCP connection from %s\n", tc.RemoteAddr())

	// Set SO_LINGER so that an RST will be sent when the connection is closed.
	err = setRSTSockopt(tc)
	if err != nil {
		return err
	}

	err = proxy(tc)
	if err != nil {
		return err
	}

	err = tc.Close()
	if err != nil {
		return err
	}

	log.Println("Done proxying connection")
	return nil
}

func main() {
	err := run()
	if err != nil {
		log.Printf("%v\n", err)
		os.Exit(1)
	}
}
