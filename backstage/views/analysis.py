from flask import render_template, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import Analysis

analysis = Blueprint('analysis', __name__, template_folder='../templates')

@analysis.route('/dashboard')
@login_required
def dashboard():
    revenue = []
    dataa = []
        
    row = Analysis.category_discharge()
    datab = []
    for i in row:
        temp = {
            'value': i[0],
            'name': i[1]
        }
        datab.append(temp)

    row = Analysis.category_sex()
    datac = []
    for i in row:
        temp = {
            'value': i[0],
            'name': i[1]
        }
        datac.append(temp)
        
    nameList = []
    counter = 0

    countList = []
        
    return render_template('dashboard.html', counter = counter, revenue = revenue, dataa = dataa, datab = datab, datac = datac, nameList = nameList, countList = countList)