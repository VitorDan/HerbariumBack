from flask import current_app as app, request
from webargs.flaskparser import parser
from api.serializers import ExsiccateSerializer
@app.route('/exsiccates/', methods=['GET','POST'])
def exsiccates():
    data = request.form.copy()
    data = ExsiccateSerializer().loads(data['json'])
    print(data)
    return f'<p>Ola mundo</p>'