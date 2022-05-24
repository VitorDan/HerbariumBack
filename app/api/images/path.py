from glob import glob
from os import path
from flask import current_app as app
from api import celery
from api.models import Image
def getImages(absPath):
    print('Images here ......................')
    namesImages  = glob(absPath+'/'+'*')
    if namesImages:
        print(namesImages[0].split('/')[-1])
    else:
        print('diretorio vazio')
    return None
@celery.task()
def requestImageDir(id_exsiccate):
    with app.app_context():
        absPath = path.join(app.config['UPLOAD_FOLDER']+'/'+id_exsiccate)
        namesImages  = glob(absPath+'/'+'*')
        # namesImages = [i.split('/')[-1] for i in namesImages]
        return namesImages