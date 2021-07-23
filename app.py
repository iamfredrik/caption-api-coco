# -*- coding: utf-8 -*-
import os
import tensorflow as tf
from flask import Flask, jsonify, request, redirect
import numpy as np
from werkzeug.utils import secure_filename
from flask_cors import CORS

from image_captioning import *

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set({'jpg','jpeg'})

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/caption', methods=['POST'])
def caption():
    checkpoint_path = "./checkpoints/train"

    ckpt = tf.train.Checkpoint(encoder=encoder,decoder=decoder,optimizer = optimizer)

    latest = tf.train.latest_checkpoint(checkpoint_path)
    
    # Restore latest checkpoint
    ckpt.restore(latest)
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return "no file"
        file = request.files['file']
        if file.filename == '':
            return "no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Evaluate the image
            result, attention_plot = evaluate(file_path)
            if result:
                os.remove(file_path)
    
                for i in result:
                    if i=="<end>":
                        result.remove(i)
                    else:
                        pass
                
                result_string = ' '.join(result)
                # Return caption
                return jsonify(caption=result_string)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
