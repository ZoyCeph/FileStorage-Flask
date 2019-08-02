# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 09:14:19 2019

@author: ProjectDept
"""

import os, glob, socket
from flask import Flask, render_template, request, send_from_directory
from flask_uploads import UploadSet, configure_uploads, ALL

app = Flask(__name__)

files = UploadSet('files', ALL)
app.config['UPLOADS_DEFAULT_DEST'] = r'D:\testzone'
app.config['UPLOAD_FOLDER'] = 'data/'
configure_uploads(app, files)

MyFolder=r'D:\testzone\files'
pattern = '*.*'
os.chdir(MyFolder)


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

print(' * Current IP: '+get_host_ip())

@app.route('/')
def index():
    return '<a href="/download"> 文件下载 </a><a href="/upload"> 文件上传 </a>'

@app.route('/download')
def filelist():
    maps ={}
    for fname in glob.glob(pattern):
        if os.path.isfile(fname):
            key = fname
            maps[key]= os.path.getsize(fname)/1048576
    return render_template('download.htm', files=maps)

@app.route('/download/<filename>')
def download(filename):
    fname = filename.encode('utf-8').decode('utf-8')
    return send_from_directory(MyFolder, fname, mimetype='application/octet-stream')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'media' in request.files:
        filename = files.save(request.files['media'])
        url = files.url(filename)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)