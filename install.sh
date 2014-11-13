#!/bin/bash
set -ev

######################################################
# Encapsulate install to be called by other scripts. #
######################################################
pip install pelican markdown pycrypto jinja2
npm install -g katex
