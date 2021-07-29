#!/usr/bin/env python3
""" Automaticky generator cisla verze
Automaticky generuje cislo verze z informaci, poskytnutych gitem
Copyright (c) 2019 xPablo.cz
Autor: Pavel Brychta

Modifikace pro Eledio skripty 2020, Pavel Brychta
"""
import subprocess
import fileinput

after = b"0"
mod = b""
isgit = True
try:
    tag = subprocess.check_output(["git", "describe", "--tags", "--always"]).strip()
except Exception:
    revision = b"0.0.0x"
    isgit = False
if isgit:
    if tag.find(b".") < 0:
        tag = b"0.0.0"
    if tag == b"0.0.0":
        after = subprocess.check_output(["git", "rev-list", "--all", "--count"]).strip()
    else:
        if tag.find(b"-") > 0:
            taginfo = tag.split(b'-')
            tag = taginfo[0]
            after = taginfo[1]
        else:
            after = subprocess.check_output(["git", "rev-list", tag + b"..HEAD", "--count"]).strip()
    mod = subprocess.check_output(["git", "diff", "HEAD"]).strip()
    if after == b"0":
        revision = tag
    else:
        revision = tag + b'.' + after
    if mod != b"":
        revision = revision + b"m"

print("APP_VERSION=%s" % revision.decode("utf-8"))

# https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file

# with fileinput.FileInput('eledio-app', inplace=True) as file:
#    for line in file:
#        print(line.replace('{{$APPVERSION$}}', revision.decode("utf-8")), end='')
