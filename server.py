from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({'status': 'OK'})
    
@app.route("/modules/")
def getModulesNames():
    return jsonify({'status': 'OK'})

@app.route("/module/<moduleName>")
def getModuleFull(moduleName):
    return jsonify({'status': moduleName})

@app.route("/module/files/<moduleName>")
def getModuleFiles(moduleName):
    return jsonify({'status': moduleName})

@app.route("/module/conf/<moduleName>")
def getModuleConf(moduleName):
    return jsonify({'status': moduleName})

@app.route("/module/view/<moduleName>")
def getModuleDjangoView(moduleName):
    return jsonify({'status': moduleName})

if __name__ == "__main__":
    app.run(debug=True)