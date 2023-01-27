from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

#TODO: revisar a documentação e gerar uma secret key segura. Além de reposiciona-la em um 'secretsconfig.py'
app.secret_key = 'joao'     

from Models.Models import * 

from Database.database import db_session, engine

Base.metadata.create_all(bind = engine)

from routes import routes

