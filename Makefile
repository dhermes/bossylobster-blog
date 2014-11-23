PY?=python
PELICAN?=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
ALT_CONFFILE=$(BASEDIR)/pelicanconf_with_pagination.py

PRINT_SEP='============================================================'

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
	@echo '   make serve-local                 serve at http://192.168.XX.YY      '
	@echo '   make devserver [PORT=8000]       start/restart develop_server.sh    '
	@echo '   make stopserver                  stop local server                  '
	@echo '                                                                       '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html'
	@echo '                                                                       '

render:
	$(PY) render_jinja2_templates.py

html:
	@echo 'Rendering templates...'
	@echo $(PRINT_SEP)
	@make render
	@echo $(PRINT_SEP)
	@echo 'Making first pass with paging'
	@echo $(PRINT_SEP)
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(ALT_CONFFILE) $(PELICANOPTS)
	@echo $(PRINT_SEP)
	@echo 'Storing paging index*.html files for re-use and removing paged output'
	@echo $(PRINT_SEP)
	mv $(OUTPUTDIR)/index*.html $(BASEDIR)
	make clean
	@echo $(PRINT_SEP)
	@echo 'Making second pass without paging'
	@echo $(PRINT_SEP)
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
	@echo $(PRINT_SEP)
	@echo 'Putting back paging index*.html files'
	@echo $(PRINT_SEP)
	mv -f $(BASEDIR)/index*.html $(OUTPUTDIR)
	@echo $(PRINT_SEP)
	@echo 'Removing unwanted pages'
	@echo $(PRINT_SEP)
	rm -f $(OUTPUTDIR)/authors.html
	rm -fr $(OUTPUTDIR)/author/
	rm -f $(OUTPUTDIR)/categories.html
	rm -fr $(OUTPUTDIR)/category/
	rm -f $(OUTPUTDIR)/tags.html
	@echo $(PRINT_SEP)
	@echo 'Rewriting paths for paging index*.html files'
	@echo $(PRINT_SEP)
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
	cd $(OUTPUTDIR) && $(PY) ../pelican_server.py 80 $(shell ./get_local_ip.py)

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
