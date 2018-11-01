__author__ = 'tinglev'


class PrintUtil(object):

    @staticmethod
    def color(line, color='\033[0m'):
        print "{}{}\033[0m".format(color, line)

    @staticmethod
    def green(line):
        PrintUtil.color(line, '\033[32m')

    @staticmethod
    def black(line):
        PrintUtil.color(line, '\033[0m')

    @staticmethod
    def pink(line):
        PrintUtil.color(line, '\033[95m')
    
    @staticmethod
    def red(line):
        PrintUtil.color(line, '\033[31m')
