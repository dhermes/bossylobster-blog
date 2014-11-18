PY?=python
PELICAN?=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

help:
	@echo 'Makefile for a pelican Web site                                        '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make render                      render blog posts from templates   '
	@echo '   make html                        (re)generate the web site          '
	@echo '   make clean                       remove the generated files         '
	@echo '   make regenerate                  regenerate files upon modification '
	@echo '   make serve [PORT=8000]           serve site at http://localhost:8000'
	@echo '   make serve-local [PORT=8000]     serve at http://192.168.XX.YY:8000 '
	@echo '   make devserver [PORT=8000]       start/restart develop_server.sh    '
	@echo '   make stopserver                  stop local server                  '
	@echo '                                                                       '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html'
	@echo '                                                                       '

render:
	$(PY) render_jinja2_templates.py

html: render
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
	rm -f $(OUTPUTDIR)/authors.html
	rm -fr $(OUTPUTDIR)/author/
	rm -f $(OUTPUTDIR)/categories.html
	rm -fr $(OUTPUTDIR)/category/
	rm -f $(OUTPUTDIR)/tags.html
	python rewrite_custom_pagination.py

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

regenerate:
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve:
ifdef PORT
	cd $(OUTPUTDIR) && $(PY) ../pelican_server.py $(PORT)
else
	cd $(OUTPUTDIR) && $(PY) ../pelican_server.py
endif

serve-local:
ifdef PORT
	cd $(OUTPUTDIR) && $(PY) ../pelican_server.py $(PORT) $(shell ./get_local_ip.py)
else
	@echo 'No port defined. Run as "make serve-local PORT=8000".'
endif

devserver:
ifdef PORT
	$(BASEDIR)/develop_server.sh restart $(PORT)
else
	$(BASEDIR)/develop_server.sh restart
endif

stopserver:
	kill -9 `cat pelican.pid`
	kill -9 `cat srv.pid`
	@echo 'Stopped Pelican and SimpleHTTPServer processes running in background.'

.PHONY: render html help clean regenerate serve devserver stopserver
