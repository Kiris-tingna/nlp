# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:view.py
# @time:2017/3/13 0013 12:25
from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template("index.html", text="Hello World")