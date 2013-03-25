#!/usr/bin/env python
import re, urllib
import web

### BEGIN

#!/usr/bin/python
#
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
#
# Usage: ./brainfuck.py [FILE]

import sys
import urllib

def fetch(url):
  return urllib.urlopen(url).read()

def evaluate(code, input):
  code     = cleanup(list(code))
  bracemap = buildbracemap(code)

  cells, codeptr, cellptr = [0], 0, 0

  out = ''

  while codeptr < len(code):
    command = code[codeptr]

    if command == ">":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "<":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "+":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "-":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
    if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
    if command == ".": out = out + chr(cells[cellptr])
    if command == ",":
      c, input = (input[0], input[1:]) if len(input) > 0 else ('\0', '')

      cells[cellptr] = ord(c)
      
    codeptr += 1
  return out

def cleanup(code):
  return filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code)


def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


### END


def bf(phenny, input): 
   """Call a webservice."""
   text = input.group(2)
   if text == None: return phenny.reply(".bf <code> <input>")
   split = text.split(' ')
   code = split[0]

   if code.find("http://") == 0: code = fetch(code)  

   input = split[1] if len(split) > 1 else ''

   return phenny.reply(str(evaluate(code, input)))

bf.commands = ['bf']
bf.example = '.bf <brainfuck code> <input>'
