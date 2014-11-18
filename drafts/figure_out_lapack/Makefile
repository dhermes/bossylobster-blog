# http://stackoverflow.com/questions/714100/os-detecting-makefile
# http://www.seehuhn.de/pages/linear#lapack-hard

# Ubuntu
# $(CC) testdgtsv.c -o testdgtsv_ubu -llapack -lblas
# Mac OS X
# $(CC) testdgtsv.c -o testdgtsv_mac -framework veclib

CC = cc

UNAME := $(shell uname -s)
ifeq ($(UNAME),Linux)
	CCFLAGS = -llapack -lblas
endif
ifeq ($(UNAME),Darwin)
	CCFLAGS = -framework veclib
endif

help:
	@echo 'Usage:'
	@echo '    make test_dgtsv      Build test binary for triangular solve      '
	@echo '    make test_dgtsv_cpp  Build test (C++) binary for triangular solve'
	@echo '    make clean           Remove generated files                      '

test_dgtsv:
	$(CC) test_dgtsv.c -o $@ $(CCFLAGS)

test_dgtsv_cpp:
	$(CC) test_dgtsv.cpp -o $@ $(CCFLAGS)

clean:
	rm test_dgtsv test_dgtsv_cpp

.PHONY: help clean
