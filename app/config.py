from os import path

class DevConf:
    DIRECTORY = path.abspath(path.dirname(__file__))
    SECRET_KEY = 'abcdasklcx'
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:263854@0.0.0.0:5432/herbarium'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:12345@localhost:5432/herbarium'
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    UPLOAD_FOLDER = DIRECTORY + '/upload/'

# sudo docker run --rm -d -v postgres:/var/lib/postgres -v postgres_config:/etc/postgres --name herbariodb -p 5432:5432 --network postnet -e POSTGRES_USER=docker -e POSTGRES_PASSWORD=1234 postgres
# sudo docker exec -ti herbariodb psql -U docker -c "CREATE DATABASE herbario"
# sudo docker exec -ti herbariodb psql -U docker herbario