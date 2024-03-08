import os
from flask import Flask

UPLOAD_FOLDER = r'C:\Users\akira\Documents\coding_class_assignments\Projects_and_alg\Solo_project\concert_hall\uploads'

app = Flask(__name__)    
app.secret_key = "SomeSuperSecretComplexKey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER