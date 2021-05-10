PY?=py
PELICAN?=$(PY) -m pelican
PELICANOPTS=

# BASEDIR=$(CURDIR)
BASEDIR=.
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
# PUBLISHCONF=$(BASEDIR)/publishconf.py

THEME_DIR=./localtheme/

SCSS_FILES=$(wildcard $(THEME_DIR)static/sass/*) 
CSS_REQS=$(patsubst  $(THEME_DIR)static/sass/%.scss,$(THEME_DIR)static/css/%.css,$(SCSS_FILES))

DEBUG ?= 1
ifeq ($(DEBUG), 1)
	PELICANOPTS +=
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

html: theme
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

debug: theme
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) --debug 2>&1 | tee debug.log

test: html
	$(PY) -m http.server --directory $(OUTPUTDIR)

# publish: theme
# 	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

# upload: publish
# 	# --cvs-exclude ?
# 	rsync -e "/bin/ssh -p $(SSH_PORT)" -P -rvzc --delete $(OUTPUTDIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

theme: $(CSS_REQS)

%.css: ../sass/%.scss
	dart-sass/sass.bat $< $@ --source-map --style compressed 

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)


help:
	@echo 'Makefile for a pelican Web site'
	@echo '                               '
	@echo 'Usage:                         '
	@echo '   make html                Generate draft html'
	@echo '   make debug               Generate HTML with extra output'
	@echo '   make test                Serve draft html locally'
	@echo '   make publish             Generate using production settings '
	@echo '   make clean               Clean out stale artifacts'
	@echo '   make upload              Upload a publication version via rsync'


.PHONY: html help clean regenerate serve serve-global devserver publish ssh_upload rsync_upload theme
