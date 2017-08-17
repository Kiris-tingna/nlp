# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:spider.py
# @time:2017/8/1 0001 15:04
from lxml import html

seed_url = u"http://www.kekenet.com/read/essay/ats/"
x = html.parse(seed_url)
spans = x.xpath("*//ul[@id='menu-list']//li/h2/a")
for span in spans[:10]:
    details_url = span.xpath("attribute::href")[0]
    xx = html.parse(details_url)
    name = span.text
    f = open(name, 'a')
    contents = xx.xpath("//div[@id='article']//p/text()")
    for content in contents:
        if len(str(content)) > 1:
            f.write(content.encode('raw_unicode_escape')+'\n')
    f.close()