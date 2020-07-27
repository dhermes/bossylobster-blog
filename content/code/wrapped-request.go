package main

import (
	"bufio"
	"bytes"
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"net/http"
)

func mustNil(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	prefixPROXYProtocol := "PROXY TCP4 198.51.100.22 203.0.113.7 35646 80\r\n"
	caCertFile := "./rootCA-cert.pem"
	addr := "localhost:3443"
	// 1. Create HTTP request and serialize body to byte string.
	r, err := http.NewRequest("GET", "http://"+addr, nil)
	r.Header.Set("User-Agent", "go-raw-socket")
	r.Header.Set("X-Forwarded-For", "127.0.0.4, 127.0.0.3, 127.0.0.2")
	mustNil(err)
	w := bytes.NewBuffer(nil)
	err = r.Write(w)
	mustNil(err)

	// 2. Create TLS config with `localhost` as server name and CA certificate
	//    pool containing custom root CA.
	pool := x509.NewCertPool()
	caCert, err := ioutil.ReadFile(caCertFile)
	mustNil(err)
	if ok := pool.AppendCertsFromPEM(caCert); !ok {
		log.Fatal("Failed to add CA certificate to certificate pool")
	}
	config := &tls.Config{RootCAs: pool, ServerName: "localhost"}

	// 3. Create a raw TCP connection and send PROXY protocol prefix.
	rawConn, err := net.Dial("tcp", addr)
	mustNil(err)
	defer rawConn.Close()
	rawConn.Write([]byte(prefixPROXYProtocol))

	// 4. Wrap raw TCP connection in a TLS envelope, send HTTP request and
	//    read response.
	conn := tls.Client(rawConn, config)
	defer conn.Close()
	n, err := conn.Write(w.Bytes())
	mustNil(err)
	if n != len(w.Bytes()) {
		log.Fatal("Not all bytes were written")
	}
	responseFull := make([]byte, 1024)
	n, err = conn.Read(responseFull)
	mustNil(err)
	if n >= 1024 {
		log.Fatal("Incomplete read")
	}
	responseFull = responseFull[:n]

	// 5. Parse HTTP response (as text) to an `http.Response` and read the body.
	resp, err := http.ReadResponse(bufio.NewReader(bytes.NewReader(responseFull)), r)
	mustNil(err)
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	mustNil(err)
	fmt.Printf(string(body))
}
