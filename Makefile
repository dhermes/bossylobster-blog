.PHONY: help
help:
	@echo 'Makefile for `bossylobster-blog`'
	@echo ''
	@echo 'Usage:'
	@echo '   make run [PORT=...]        Run static-content server, with reloading'
	@echo '   make run-all [PORT=...]    Run static-content server, with reloading; include expired/drafts/future'
	@echo ''

HUGO_PRESENT := $(shell command -v hugo 2> /dev/null)

################################################################################
# Environment variable defaults
################################################################################
PORT ?= 5764

.PHONY: run
run: _require-hugo
	@hugo --minify --log --verbose --port=$(PORT) server

.PHONY: run-all
run-all: _require-hugo
	@hugo --minify --log --verbose --buildDrafts --buildFuture --buildExpired --port=$(PORT) server

.PHONY: _require-hugo
_require-hugo:
ifndef HUGO_PRESENT
	$(error 'hugo is not installed, it can be installed via "go get -u github.com/gohugoio/hugo" or "brew install hugo".')
endif
