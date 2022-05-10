from crypt import methods
from flask import current_app as app
from flask import send_file as send
from api.images import requestImageDir
@app.route('/images/', methods=['GET'])
def returnImage():
    images = requestImageDir.apply_async(args=['944475cb-36a0-4096-acc9-819441e6221a']).get()
    # _a = requestImageDir.apply_async()
    for i in images:
        send(i, as_attachment=False)
    return f'ola mundo'
