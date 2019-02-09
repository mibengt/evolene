__author__ = 'tinglev'

def color(line, color_code='\033[0m'):
    print(f'{color_code}{line}\033[0m')

def green(line):
    color(line, '\033[32m')

def black(line):
    color(line, '\033[0m')

def pink(line):
    color(line, '\033[95m')

def red(line):
    color(line, '\033[31m')
