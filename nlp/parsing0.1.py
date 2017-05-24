# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:parsing0.1.py
# @time:2017/5/18 0018 15:10
from pyparsing import Word, alphas
greet = Word( alphas ) + "," + Word( alphas ) + "!" # <-- grammar defined here
hello = "Hello, World!"
print (hello, "->", greet.parseString( hello ))

# python3
from pyparsing import Word, alphas,CharsNotIn
greet = CharsNotIn( ',!' ) + "," + CharsNotIn( ',!' ) + "!" # <-- grammar defined here
hello = "你好, 世界!"
print (hello, "->", greet.parseString( hello ))

from pyparsing import Word, Literal, alphas

salutation     = Word( alphas + "'" )
comma          = Literal(",")
greetee        = Word( alphas )
endPunctuation = Literal("!")

greeting = salutation + comma + greetee + endPunctuation
print(greeting)

from pyparsing import Word, Literal, alphas

salutation     = Word( alphas + "'" )
comma          = Literal(",")
greetee        = Word( alphas )
endPunctuation = Literal("!")

greeting = salutation + comma + greetee + endPunctuation

tests = ("Hello, World!",
"Hey, Jude!",
"Hi, Mom!",
"G'day, Mate!",
"Yo, Adrian!",
"Howdy, Pardner!",
"Whattup, Dude!" )

for t in tests:
        print(t, "->", greeting.parseString(t))