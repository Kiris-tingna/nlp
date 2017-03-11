#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag ==  'content':
            p = 1
        else:
            p = 0

    def handle_data(self, data):
        if p == 1:
            print(data)


inp = open('news_tensite_xml.smarty.dat', 'r', encoding='gb18030')
p = 0

parser = MyHTMLParser()
parser.feed(inp.readline())
