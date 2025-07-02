from flask import Flask
from public import public
from admin import admin
from staff import staff
from pro import pro
from api import api

app=Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Set upload limit to 100 MB


app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(staff)
app.register_blueprint(pro)
app.register_blueprint(api,url_prefix="/api")
app.secret_key="akhila"
app.run(debug=True,port=5884,host="0.0.0.0")