# Makefile for source rpm: sqlite
# $Id$
NAME := sqlite
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
