#!/usr/bin/env python
import re, urllib
import web
from numpy import *
from numpy.fft import *

def py(phenny, input): 
   """Call a webservice."""
   text = input.group(2)
   return phenny.reply(str(eval(text)))

py.commands = ['py']
py.example = '.py code'

if __name__ == '__main__': 
   print __doc__.strip()
