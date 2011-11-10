# Makefile for all our formulations.

.PHONY : all 

all : common cannon dns

clean:
	rm -f common.o cannon dns


common: common.c common.h
	mpicc -c -o common.o common.c

cannon: cannon.c lu1d.c lu2d.c common
	mpicc -o cannon cannon.c lu1d.c lu2d.c common.o

dns: dns.c lu1d.c lu2d.c common
	mpicc -o dns dns.c lu1d.c lu2d.c common.o
