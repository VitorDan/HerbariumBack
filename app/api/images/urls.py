from os import path
from flask import request, current_app as app
from flask import send_from_directory as send, jsonify
from webargs.flaskparser import parser
from webargs import fields
args_model = {
    'id_exsiccate': fields.UUID(),
    'image': fields.String()
}
@app.route('/images/', methods=['GET'])
def returnImage():
    try:
        _a =  parser.parse(args_model,request,location="querystring")
        id_exsiccate,imgs = _a['id_exsiccate'], _a['image']
        absPath = app.config['UPLOAD_FOLDER']+'/'+id_exsiccate.hex+'/'
        return send(absPath,path=imgs,as_attachment=False)
    except FileNotFoundError as e:
        jsonify(e)
@app.route('/test/', methods=['POST'])
def setImage():
    files = request.form
    print(request.files)
    return f'<p>Ola Mundo</p>'