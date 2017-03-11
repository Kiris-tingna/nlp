# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:process_sogou1.py
@time:2017/3/8 0008 13:18
"""
from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()

def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text


def main():
    inp = open('news.sohunews.010806.txt', 'r', encoding='gb18030')
    outp = open('news.sohunews.010806.dat', 'w', encoding='utf8')
    text = inp.read()
    outp.write(dehtml(text))

if __name__ == '__main__':
    main()