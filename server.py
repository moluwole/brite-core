"""
Server.py file. Instantiates the Flask App with all required configs
"""

from flask import Flask, url_for, render_template, request, redirect, flash
from models.model import FeatureModel
from db import db

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:nigeriA070@localhost/features'
app.secret_key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='


db.init_app(app)


def create_app():
    """
    Return an instance of the Flask App. used to create the database tables using SQLAlchemy
    :return:
    """
    return app


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Get all the feature requests and pass it into the index.html template. Allowed Methods: POST, GET
    :return:
    """
    data = FeatureModel.return_all()
    title = "All Feature Requests"
    return render_template('index.html', data=data, title=title)


@app.route('/new_ticket', methods=['POST', 'GET'])
def new():
    """
    Render the Request New Feature Template. Allowed Methods: POST, GET
    :return:
    """
    return render_template('add.html')


@app.route('/add-new', methods=['POST', 'GET'])
def add_new():
    """
    Function to add a new feature request to the database. Calls the save() function of the FeatureModel class.
    Allowed Methods: POST, GET
    :return:
    """
    title = request.form.get('title')
    description = request.form.get('description')
    client = request.form.get('client')
    client_priority = request.form.get('client_priority')
    target_date = request.form.get('target_date')
    product_areas = request.form.get('product_areas')

    feature_model = FeatureModel(title, description, client, client_priority, target_date, product_areas)
    feature_model.save()

    flash('Your request has been saved', 'success')
    return redirect(url_for('new'))


@app.route('/by-client', methods=['POST', 'GET'])
def get_by_client():
    """
    Get the list of feature requests by client. Allowed Methods: POST, GET
    :return:
    """
    if request.method == 'POST':
        client_name = request.form.get('client_name')
    else:
        client_name = request.args.get('client_name')
    data = FeatureModel.find_by_name(client_name)
    title = "Feature Request by Client: " + str(client_name)
    return render_template('index.html', data=data, title=title)


@app.route('/by-date', methods=['POST', 'GET'])
def get_by_date():
    """
    Get the list of feature requests by Target Date. Allowed Methods: POST, GET
    :return:
    """
    if request.method == 'POST':
        request_date = request.form.get('target_date')
    else:
        request_date = request.args.get('target_date')

    data = FeatureModel.find_by_date(request_date)
    title = "Features with Target Date: " + str(request_date)
    return render_template('index.html', data=data, title=title)


@app.route('/by-product', methods=['POST', 'GET'])
def get_by_product():
    """
    Get the list of feature request by Product Areas. Allowed Methods: POST, GET
    :return:
    """
    if request.method == 'POST':
        request_product = request.form.get('product_areas')
    else:
        request_product = request.args.get('product_areas')

    data = FeatureModel.find_by_product(request_product)
    title = "Features with Product Areas: " + str(request_product)
    return render_template('index.html', data=data, title=title)


if __name__ == '__main__':
    app.run(debug=True)
