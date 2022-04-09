from os import path

class DevConf:
    DIRECTORY = path.abspath(path.dirname(__file__))
    SECRET_KEY = 'abcdasklcx'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:1234@172.17.0.1:5432/herbarium'
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    UPLOAD_FOLDER = DIRECTORY + '/upload/'