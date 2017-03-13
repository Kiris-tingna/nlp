# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:kbase2.py
# @time:2017/3/13 0013 14:33

from flask import Flask, request, jsonify, render_template, session, redirect, url_for, abort, flash
import pyexcel as pe

app = Flask(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
#    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
kbase = "kbase.xlsx"
@app.route('/')
def show_entries():
    record = pe.get_records(file_name=kbase)
    entries = [record[1], record[2], record[3], record[4]]
    return render_template('show_entries.html', entries=entries)

@app.route('/upload')
def upload():
    if request.method == 'POST' and 'excel' in request.files:
        filename = request.files['excel'].filename
        extension = filename.split(".")[-1]
        content = request.files['excel'].read()
        if sys.version_info[0] > 2:
            content = content.decode('utf-8')
        sheet = pe.get_sheet(file_type=extension, file_content=content)
        sheet.name_columns_by_row(0)
        return jsonify({"result": sheet.dict})
    return render_template('upload.html')

@app.route('/download')
def download():
    sheet = pe.Sheet(data)
    output = make_response(sheet.csv)
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    data = [request.form['title'], request.form['title1'], request.form['title2'], request.form['text']]
    sheet = pe.get_sheet(file_name=kbase)
    sheet.row += data
    sheet.save_as(kbase)
    flash('完成知识库内容添加')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == "__main__":
    app.run()