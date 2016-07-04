from flask import Flask, jsonify
from flask import render_template
from flask_assets import Bundle, Environment

app = Flask(__name__)

# need to move this to util/assets.py
bundles = {

    'index_js': Bundle(
        'js/lib/jquery.js',
        'js/lib/bootstrap.js',
        'js/input_helper.js',
        output='gen/index.js'),

    'index_css': Bundle(
        'css/lib/bootstrap.min.css',
        'css/index.css',
        output='gen/index.css'),
}
assets = Environment(app)
assets.register(bundles)

@app.route('/')
def index():
    return render_template('index.html')