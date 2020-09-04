package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"reflect"
	"strings"
	"time"

	apiv2 "github.com/envoyproxy/go-control-plane/envoy/api/v2"
	authv2 "github.com/envoyproxy/go-control-plane/envoy/api/v2/auth"
	corev2 "github.com/envoyproxy/go-control-plane/envoy/api/v2/core"
	discoveryv2 "github.com/envoyproxy/go-control-plane/envoy/service/discovery/v2"
	"github.com/golang/protobuf/ptypes"
	"google.golang.org/grpc"
	"google.golang.org/grpc/metadata"
)

const (
	// EnvoyAdminPort is the (typical) port used for the Envoy Admin API.
	EnvoyAdminPort = "15000"
	// EnvoyUDSForSDS is the (expected) path to the UNIX domain socket (UDS)
	// used for the Istio / Envoy SDS server.
	EnvoyUDSForSDS = "/etc/istio/proxy/SDS"
)

// ServerInfoCLIOptions describes the `command_line_options` field in the
// Envoy Admin API response for `/server_info`.
type ServerInfoCLIOptions struct {
	ServiceNode string `json:"service_node"`
}

// ServerInfoResponse describes the Envoy Admin API response for `/server_info`.
type ServerInfoResponse struct {
	CommandLineOptions ServerInfoCLIOptions `json:"command_line_options"`
}

func getServiceNode() (string, error) {
	url := fmt.Sprintf("http://localhost:%s/server_info", EnvoyAdminPort)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return "", err
	}
	log.Printf(" GET %s\n", url)

	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("Unexpected status code %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	sir := ServerInfoResponse{}
	err = json.Unmarshal(body, &sir)
	if err != nil {
		return "", err
	}

	return sir.CommandLineOptions.ServiceNode, nil
}

func validateMetadata(header, trailer metadata.MD) error {
	expected := metadata.MD{"content-type": []string{"application/grpc"}}
	if !reflect.DeepEqual(expected, header) {
		return fmt.Errorf("Unexpected initial metadata headers: %#v", header)
	}

	expected = metadata.MD{}
	if !reflect.DeepEqual(expected, trailer) {
		return fmt.Errorf("Unexpected trailing metadata headers: %#v", trailer)
	}

	return nil
}

func fetchSecrets(target, serviceNode string) (*apiv2.DiscoveryResponse, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	conn, err := grpc.Dial(target, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		return nil, err
	}
	defer conn.Close()

	var header, trailer metadata.MD
	c := discoveryv2.NewSecretDiscoveryServiceClient(conn)
	request := &apiv2.DiscoveryRequest{Node: &corev2.Node{Id: serviceNode}}
	response, err := c.FetchSecrets(ctx, request, grpc.Header(&header), grpc.Trailer(&trailer))
	if err != nil {
		return nil, err
	}

	err = validateMetadata(header, trailer)
	if err != nil {
		return nil, err
	}

	return response, nil
}

func extractTLSCertificate(response *apiv2.DiscoveryResponse) (*authv2.TlsCertificate, error) {
	if response == nil {
		return nil, errors.New("Expected non-nil response")
	}

	if response.Nonce != response.VersionInfo {
		return nil, errors.New("Unexpected nonce")
	}

	if response.ControlPlane != nil {
		return nil, errors.New("Unexpected nil control plane")
	}

	if len(response.Resources) != 1 {
		return nil, fmt.Errorf("Expected 1 resource, got %d", len(response.Resources))
	}

	secret := &authv2.Secret{}
	err := ptypes.UnmarshalAny(response.Resources[0], secret)
	if err != nil {
		return nil, err
	}

	if secret.Name != "" {
		return nil, fmt.Errorf("Unexpected secret name %q", secret.Name)
	}

	tc := secret.GetTlsCertificate()
	if tc == nil {
		return nil, errors.New("Expected `type` oneof to be `tls_certificate`")
	}

	return tc, nil
}

func displayCertificate(tc *authv2.TlsCertificate) error {
	if tc == nil {
		return errors.New("Expected non-nil certificate")
	}

	cc := tc.GetCertificateChain()
	if cc == nil {
		return errors.New("Expected non-nil `certificate_chain`")
	}
	ccBytes := cc.GetInlineBytes()
	pk := tc.GetPrivateKey()
	if pk == nil {
		return errors.New("Expected non-nil `private_key`")
	}
	pkBytes := pk.GetInlineBytes()

	// Make sure the `certificate_chain` and `private_key` inline bytes are
	// the only fields with data.
	expected := &authv2.TlsCertificate{
		CertificateChain: &corev2.DataSource{Specifier: &corev2.DataSource_InlineBytes{InlineBytes: ccBytes}},
		PrivateKey:       &corev2.DataSource{Specifier: &corev2.DataSource_InlineBytes{InlineBytes: pkBytes}},
	}
	if !reflect.DeepEqual(expected, tc) {
		return errors.New("Unexpected fields in TLS certificate")
	}

	log.Println("DiscoveryResponse.Resources[0].GetTlsCertificate()")
	log.Println("  GetCertificateChain():")
	for _, line := range strings.Split(string(ccBytes), "\n") {
		log.Printf("    %s\n", line)
	}
	log.Println("  GetPrivateKey():")
	for _, line := range strings.Split(string(pkBytes), "\n") {
		log.Printf("    %s\n", line)
	}
	return nil
}

func runMain() error {
	log.SetFlags(
		log.Ltime | log.Lmicroseconds | log.Lshortfile | log.LUTC,
	)

	serviceNode, err := getServiceNode()
	if err != nil {
		return err
	}
	log.Printf("Service Node: %q", serviceNode)

	target := fmt.Sprintf("unix://%s", EnvoyUDSForSDS)
	log.Printf("Target: %q", target)
	response, err := fetchSecrets(target, serviceNode)
	if err != nil {
		return err
	}

	tc, err := extractTLSCertificate(response)
	if err != nil {
		return err
	}

	log.Println("")
	log.Printf("DiscoveryResponse.VersionInfo: %q", response.VersionInfo)
	log.Printf("DiscoveryResponse.TypeUrl: %q", response.TypeUrl)
	err = displayCertificate(tc)
	if err != nil {
		return err
	}

	return nil
}

func main() {
	err := runMain()
	if err != nil {
		log.Fatal(err)
	}
}
