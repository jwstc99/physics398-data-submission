import os, pathlib
from utils.render_pngs import render
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'sdfasdg23jkh34jk5k325lk25'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            name = request.form.get('person')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], name, filename))
            flash('File Successfully Uploaded')
            return render_template('html/index.html')
    return render_template('html/index.html')

@app.route('/who', methods=['GET', 'POST'])
def pick_user():
    if request.method == 'POST':
        #check to make sure submit was not empty
        if 'person' not in request.form:
            flash('No person part')
            return redirect(request.url)
        name = request.form.get('person')
        if name == 'jack':
            return redirect(url_for('pick_dataset', user='jack'))
        if name == 'david':
            return redirect(url_for('pick_dataset', user='david'))
        if name == 'chang':
            return redirect(url_for('pick_dataset', user='chang'))

    return render_template('html/who.html')

def get_datasets(name):
    data_dir = pathlib.Path(os.path.join(app.config['UPLOAD_FOLDER'], name))
    dsets = []
    for curr_file in data_dir.iterdir():
        dsets.append(curr_file)
    return dsets

@app.route('/datasets/<user>', methods=['GET', 'POST'])
def pick_dataset(user):
    if request.method == 'POST':
        if 'dataset' not in request.form:
            flash('No dataset part')
            return redirect(request.url)
        datafile = request.form.get('dataset')
        #FILL IN GRAPH RENDERER
        tmp = datafile.split('/')[-1]
        dset_name = tmp.split('.')[0]
        try:
            render(datafile, 'pngstore', dset_name, user)
        except:
            render_template('html/graphs/error.html', message = 'Rendering Failed')
    dsets = get_datasets(user)
    return render_template('html/graphs/picker.html', len = len(dsets), datalist = dsets)