from flask import Flask

app = Flask(__name__, static_folder='app/static' )

from app import routes