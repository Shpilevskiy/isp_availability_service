from flask import Flask
from flask import render_template
from flask_assets import Bundle, Environment

app = Flask(__name__)

# need to move this to util/assets.py
bundles = {

    'index_js': Bundle(
        'vendor/jquery/dist/jquery.min.js',
        'vendor/bootstrap/dist/js/bootstrap.min.js',
        'js/input_helper.js',
        output='gen/index.js'),

    'index_css': Bundle(
        'vendor/bootstrap/dist/css/bootstrap.min.css',
        'vendor/bootstrap/dist/css/bootstrap-theme.min.css',
        'css/index.css',
        output='gen/index.css'),
}
assets = Environment(app)
assets.register(bundles)


@app.route('/')
def index():
    return render_template('index.html')
