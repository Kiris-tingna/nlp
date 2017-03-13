# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:_init_.py
# @time:2017/3/13 0013 12:26
from flask import Flask

app = Flask(__name__)
app.config.from_object("config")

from app import views, models