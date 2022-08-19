from glob import glob
import json
from inspect import ismemberdescriptor
from os import path
from flask import current_app as app, jsonify, send_from_directory as send
from api import celery
from api.models import Image
@celery.task()
def getImages(id_exsiccate, image):
    with app.app_context():
        absPath = path.join(app.config['UPLOAD_FOLDER']+'/'+id_exsiccate+'/')
        return send(absPath,path=image,as_attachment=False)
@celery.task()
def requestImageDir(id_exsiccate):
    with app.app_context():
        images = []
        absPath = path.join(app.config['UPLOAD_FOLDER']+'/'+id_exsiccate)
        namesImages  = glob(absPath+'/'+'*')
        for i in namesImages:
            with open(i,'rb') as file:
                images.append(file)
        # namesImages = [i.split('/')[-1] for i in namesImages]
        # print('Images name:', namesImages)
        return jsonify(images)