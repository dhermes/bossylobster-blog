#!/bin/sh

set -e

docker run \
  --rm \
  --volume "$(pwd)/generate-tls-certs-on-alpine.sh":/bin/generate-tls-certs-on-alpine.sh \
  --volume "$(pwd):/var/tls-certs" \
  --env CAROOT=/var/tls-certs \
  golang:1.14.4-alpine3.12 \
  /bin/generate-tls-certs-on-alpine.sh
