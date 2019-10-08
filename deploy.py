#!/usr/bin/python
from flask import Flask, jsonify, send_file, request
import os, json
from os import listdir
from os.path import isfile, join

app = Flask(__name__)

directory = 'modules'
categories = [x[0] for x in os.walk(directory)]
modules = [[x[0] for x in os.walk(os.path.join(directory, cat))] for cat in categories]

this_dir = os.path.dirname(os.path.abspath(__file__))

blacklist_extensions = [".pyc"]
blacklist_directories = ["__"]
ignore_files = ["ht_flask.py"]
ignore_folders = ["templates", "core", "build", "dist", "hackingtools", "gui"]

def extractFile(self, zipPathName, password=None):
    #ZipFile only works with 7z with ZypCrypto encryption for setting the password
    try:
        with ZipFile(zipPathName) as zf:
            return zf.extractall(password) if password else zf.extractall()
    except Exception as e:
        Logger.printMessage(message="extractFile", description=str(e), is_error=True)
        return None

def zipDirectory(self, new_folder_name):
    # Creates a Zip File from a directory
    return shutil.make_archive(new_folder_name, 'zip', new_folder_name)

def loadDataLogModules():
    with open(os.path.join(os.path.dirname(__file__) , 'data_log.json')) as json_data_file:
        return json.load(json_data_file)

def __listDirectory__(directory, files=False, exclude_pattern_starts_with=None):
    """
    Devuelve las carpetas contenidas en el directorio indicado. Si se quieren listar los 
    ficheros se deberá indicar el argumento files=True. En el caso de querer excluir ficheros o carpetas
    se indicará en el argumento exclude_pattern_starts_with con el comienzo de los mismos.
    """
    try:
        mypath = os.path.join(this_dir, directory)
        data = ''

        if files:
            data = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        else:
            data = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
        
        if blacklist_extensions:
            new_data = []
            for d in data:
                has_extension = False
                for black_ext in blacklist_extensions:
                    if black_ext in d:
                        has_extension = True
                if not has_extension:
                    new_data.append(d)
            data = new_data

        if exclude_pattern_starts_with: 
            new_data = []
            for d in data:
                if not d.startswith(exclude_pattern_starts_with):
                    new_data.append(d)
            data = new_data

        if blacklist_directories:
            new_data = []
            for d in data:
                for direc in blacklist_directories:
                    if not direc in d:
                        new_data.append(d)
            data = new_data

        if ignore_folders:
            new_data = []
            for d in data:
                exists = False
                for direc in ignore_folders:
                    if direc in d:
                        exists = True
                if not exists:
                    new_data.append(d)
            data = new_data
        
        if files and ignore_files:
            new_data = []
            for d in data:
                for file_ign in ignore_files:
                    if not file_ign in d:
                        new_data.append(d)
            data = new_data

        return data
    except:
        return []

@app.route("/", methods=['GET', 'POST'])
def home():
    return jsonify({'status': 'OK', 'data': [str(rule) for rule in app.url_map.iter_rules()]})
    
@app.route("/changes/", methods=['GET', 'POST'])
def getChanges():
    try:
        return jsonify({'status': 'OK', 'data': loadDataLogModules()})
    except Exception as e:
        return jsonify({'status':  'FAIL', 'data': 'Cant load data'})

@app.route("/categories/", methods=['GET', 'POST'])
def getCategories():
    try:
        return jsonify({'status':  'OK', 'data': __listDirectory__(join(this_dir, directory))})
    except Exception as e:
        return jsonify({'status':  'FAIL', 'data': 'Not exists'})

@app.route("/modules/", methods=['GET', 'POST'])
def getModulesNames():
    modules = []
    for cat in __listDirectory__(join(this_dir, directory)):
        for module in __listDirectory__(join(this_dir, directory, cat)):
            modules.append(module)
    return jsonify({'status': 'OK', 'data': modules})

def getCategoryByModuleName(moduleName):
    for cat in __listDirectory__(join(this_dir, directory)):
        for module in __listDirectory__(join(this_dir, directory, cat)):
            if module in moduleName:
                return cat
    return None

@app.route("/category/<category>", methods=['GET', 'POST'])
def getModulesNamesByCategory(category):
    try:
        return jsonify({'status': 'OK', 'data': __listDirectory__(join(this_dir, directory, category))})
    except Exception as e:
        return jsonify({'status':  'FAIL', 'data': 'Not exists'})

@app.route("/module/download/<moduleName>", methods=['GET', 'POST'])
def downloadModuleFull(moduleName):
    try:
        return send_file(zipDirectory(new_folder_name=join(this_dir, directory, getCategoryByModuleName(moduleName), moduleName.replace('ht_',''))), as_attachment=True)
    except Exception as e:
        return jsonify({'status':  'FAIL', 'data': 'Not exists'})

@app.route("/module/download/files/<moduleName>", methods=['GET', 'POST'])
def downloadModuleFiles(moduleName):
    try:
        return send_file(join(this_dir, directory, getCategoryByModuleName(moduleName), moduleName, '{m}.zip'.format(m=moduleName.replace('ht_',''))), as_attachment=True)
    except Exception as e:
        return jsonify({'status':  'FAIL', 'data': 'Not exists'})

@app.route("/module/download/config/<moduleName>", methods=['GET', 'POST'])
def downloadModuleConf(moduleName):
    try:
        return send_file(join(this_dir, directory, getCategoryByModuleName(moduleName), moduleName, 'ht_{m}.json'.format(m=moduleName.replace('ht_',''))), as_attachment=True)
    except Exception as e:
        return jsonify({'status':  'FAIL', 'data': 'Not exists'})

@app.route("/module/download/views/<moduleName>", methods=['GET', 'POST'])
def downloadModuleDjangoView(moduleName):
    try:
        return send_file(join(this_dir, directory, getCategoryByModuleName(moduleName), moduleName, 'views_ht_{m}.py'.format(m=moduleName.replace('ht_',''))), as_attachment=True)
    except Exception as e:
        return jsonify({'status':  'FAIL', 'data': 'Not exists'})

@app.route("/new/module/upload/<category>/<moduleName>", methods=['GET', 'POST'])
def newModuleUpload(category, moduleName):
    if 'module' not in request.files:
        return jsonify({'status': 'FAIL', 'data': 'No file given'})
    print(extractFile(zipPathName=request.files['module']))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
