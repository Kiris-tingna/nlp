# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:kbase3.py
# @time:2017/3/13 0013 14:53
from flask import Flask, request, jsonify
import flask_excel as excel

app=Flask(__name__)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        return jsonify({"result": request.get_array(field_name='file')})
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''

data =  ['标准问题', '', '标准答案', '']
@app.route("/download", methods=['GET'])
def download():
    return excel.make_response_from_array(data, "csv")

if __name__ == "__main__":
    app.run()