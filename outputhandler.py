# -*- coding: utf-8 -*-

#system modules
import sys

#my modules
import color

#globals
markers = { 
    'ques'  : color.colorize('[?] '  , color.BLUE   ),
    'feed'  : color.colorize('[*] '  , color.CYAN   ),
    'pos'   : color.colorize('[+] '  , color.GREEN  ),
    'neg'   : color.colorize('[-] '  , color.RED    ),
    'warn'  : color.colorize('[!] '  , color.YELLOW ),
    'error' : color.colorize('[Err] ', color.MAGENTA)
}

table_positions = [15, 20, 50]

def newline():
    sys.stdout.write('\n')

def line(text):
    sys.stdout.write(text)

def question(prompt, paramValue="", necessary=False):
    """Prompt user for an input string"""
    retVal = input(markers['ques'] + prompt + " [" + str(paramValue) + "]: ")
    if not retVal:
        if paramValue:
            return paramValue
        else:
            if necessary:
                return question(prompt, necessary=True)

            else:
                return ''

    return retVal

def info(feed):
    """Print out a feed"""
    line(markers['feed'] + feed)

def success(text, paramValue=None):
    """Print positive msg"""
    if paramValue:
        line(markers['pos'] + "Set " + text + " => " + str(paramValue))
    else:
        line(markers['pos'] + text + '\n')

def fail(text, paramValue=None):
    """Print negative msg"""
    if paramValue:
        line(markers['neg'] + "Set " + text + " => " + str(paramValue))
    else:
        line(markers['neg'] + text + '\n')


def warning(text, warn=""):
    """Print warning msg"""
    if warn:
        line(markers['warn'] + warn + " : " + text)
    else:
        line(markers['warn'] + text)

def error(error='', text=''):
    """Print error msg"""
    line(markers['error'])
    if text:
        line(color.colorize(error + ' : ', color.WHITE) + text)
    else:
        line(color.colorize(error, color.WHITE))
