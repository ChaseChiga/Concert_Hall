import os
from flask import Flask

absolute_path = os.path.dirname(__file__)
relative_path = "uploads"
UPLOAD_FOLDER = os.path.join(absolute_path, relative_path)

app = Flask(__name__)    
app.secret_key = "SomeSuperSecretComplexKey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
