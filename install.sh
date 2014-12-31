#!/bin/bash
set -ev

######################################################
# Encapsulate install to be called by other scripts. #
######################################################
pip install pelican==3.5 markdown pycrypto jinja2
