from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app
import datetime

UPLOAD_FOLDER = 'static/product'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.productManager'))

@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        pid = request.values.get('delete')
        data = Product.delete_product(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = Product.get_product(pid)
            Product.delete_product(pid)
    
    elif 'edit' in request.values:
        pid = request.values.get('edit')
        return redirect(url_for('manager.edit', pid=pid))
    
    book_data = book()
    return render_template('productManager.html', book_data = book_data, user=current_user.name)

def book():
    book_row = Product.get_all_product()
    book_data = []
    for i in book_row:
        book = {
            '病歷編號': i[0],
            '患者姓名': i[1],
            '性別': i[2],
            '生日': i[3]
        }
        book_data.append(book)
    return book_data

@manager.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 0, 999))
            en = random.choice(string.ascii_letters)
            pid = 'P' + number
            data = Product.get_product(pid)

        name = request.values.get('name')
        price = request.values.get('price')
        category = request.values.get('category')
        description = request.values.get('description')

        if (len(name) < 1 or len(price) < 1):
            return redirect(url_for('manager.productManager'))

        Product.add_product(
            {'pid' : pid,
             'name' : name,
             'price' : price,
             'category' : category,
             'description':description
            }
        )

        return redirect(url_for('manager.productManager'))

    return render_template('productManager.html')

@manager.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':
        Product.update_product(
            {
            'name' : request.values.get('name'),
            'category' : request.values.get('category'),
            'price' : request.values.get('price'),
            'description' : request.values.get('description'),
            'pid' : request.values.get('pid')
            }
        )
        
        return redirect(url_for('manager.productManager'))

    else:
        product = show_info()
        return render_template('edit.html', data=product)


def show_info():
    pid = request.args['pid']
    data = Product.get_product(pid)
    pname = data[1]
    price = data[3]
    category = data[2]
    description = data[4]

    product = {
        '病歷編號': pid,
        '患者姓名': pname,
        '性別': category,
        '生日': price,
        '症狀': description
    }
    return product

# _______________________________________________________________________

@manager.route('/vitalsignManager', methods=['GET', 'POST'])
@login_required
def vitalsignManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'deletevitalsign' in request.values:
        pid = request.values.get('deletevitalsign')
        data = Product.delete_vital_sign(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = Product.get_vital_sign(pid)
            Product.delete_vital_sign(pid)
    
    elif 'editvitalsign' in request.values:
        pid = request.values.get('editvitalsign')
        return redirect(url_for('manager.editvitalsign', pid=pid))
    
    book_data = vital_sign()
    return render_template('vitalsignManager.html', book_data = book_data, user=current_user.name)

def vital_sign():
    book_row = Product.get_all_vital_sign()
    book_data = []
    for i in book_row:
        book = {
            '病歷編號': i[7],
            '測量時間': i[0],
            '呼吸': i[1],
            '收縮': i[2],
            '血氧': i[3],
            '體溫': i[4],
            '預警分數': i[5],
            '風險': i[6],
            '脈搏': i[8],
        }
        book_data.append(book)
    return book_data

@manager.route('/addvitalsign', methods=['GET', 'POST'])
def addvitalsign():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 0, 10))
            pid = 'P' + number
            data = Product.get_vital_sign(pid)

        pid = request.values.get('pid')
        rr = request.values.get('rr')
        bp = request.values.get('bp')
        spo2 = request.values.get('spo2')
        bt = request.values.get('bt')
        risk = request.values.get('risk')
        pulse = request.values.get('pulse')

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        Product.add_vital_sign(
            {
            'seqtime' : str(current_time),
            'pid' : str(pid),
            'rr' : str(rr),
            'bp' : str(bp),
            'spo2' : str(spo2),
            'bt' : str(bt),
            'score' : number,
            'risk' : str(risk),
            'pulse' :str(pulse)
            }
        )

        return redirect(url_for('manager.vitalsignManager'))

    return render_template('vitalsignManager.html')

@manager.route('/editvitalsign', methods=['GET', 'POST'])
@login_required
def editvitalsign():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':
        Product.update_vital_sign(
            {
            'septime' : request.values.get('septime'),
            'pid' : request.values.get('pid'),
            'rr' : request.values.get('rr'),
            'bp' : request.values.get('bp'),
            'spo2' : request.values.get('spo2'),
            'bt' : request.values.get('bt'),
            'score' : request.values.get('score'),
            'risk' : request.values.get('risk'),
            'pulse' : request.values.get('pulse')
            }
        )
        
        return redirect(url_for('manager.vitalsignManager'))

    else:
        product = show_vitalsignInfo()
        return render_template('editvitalsign.html', data=product)


def show_vitalsignInfo():
    pid = request.args['pid']
    data = Product.get_vital_sign(pid)
    pid = data[7]
    seqtime = data[0]
    rr = data[1]
    bp = data[2]
    spo2 = data[3]
    bt = data[4]
    score = data[5]
    risk = data[6]
    pulse = data[8]

    product = {
        '病歷編號': pid,
        '測量時間': seqtime,
        '呼吸': rr,
        '收縮': bp,
        '血氧': spo2,
        '體溫': bt,
        '預警分數': score,
        '風險': risk,
        '脈搏': pulse
    }
    return product
# _________________________________________________________________

@manager.route('/doctorManager', methods=['GET', 'POST'])
@login_required
def doctorManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'deletedoctor' in request.values:
        pid = request.values.get('deletedoctor')
        data = Product.delete_doctor(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = Product.get_doctor(pid)
            Product.delete_doctor(pid)
    
    elif 'editdoctor' in request.values:
        pid = request.values.get('editdoctor')
        return redirect(url_for('manager.editdoctor', pid=pid))
    
    book_data = doctor()
    return render_template('doctorManager.html', book_data = book_data, user=current_user.name)

def doctor():
    book_row = Product.get_all_doctor()
    book_data = []
    for i in book_row:
        book = {
            '醫師編號': i[0],
            '醫師姓名': i[1],
            '主治科別': i[2]
        }
        book_data.append(book)
    return book_data

@manager.route('/adddoctor', methods=['GET', 'POST'])
def adddoctor():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 0, 10))
            pid = 'P' + number
            data = Product.get_doctor(pid)

        pid = request.values.get('eid')
        name = request.values.get('name')
        department = request.values.get('department')
        Product.add_doctor(
            {
            'eid' : str(pid),
            'name' : str(name),
            'department' :str(department)
            }
        )

        return redirect(url_for('manager.doctorManager'))

    return render_template('doctorManager.html')

@manager.route('/editdoctor', methods=['GET', 'POST'])
@login_required
def editdoctor():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':
        Product.update_doctor(
            {
            'eid' : request.values.get('eid'),
            'name' : request.values.get('name'),
            'department' : request.values.get('department')
            }
        )
        
        return redirect(url_for('manager.doctorManager'))

    else:
        product = show_doctorInfo()
        return render_template('editdoctor.html', data=product)


def show_doctorInfo():
    eid = request.args['pid']
    data = Product.get_doctor(eid)
    eid = data[0]
    name = data[1]
    department = data[2]

    product = {
        '醫師編號': eid,
        '醫師姓名': name,
        '主治科別': department
    }
    return product


@manager.route('/orderManager', methods=['GET', 'POST'])
@login_required
def orderManager():
    if request.method == 'POST':
        pass
    else:
        order_row = Order_List.get_order()
        order_data = []
        for i in order_row:
            order = {
                '訂單編號': i[0],
                '訂購人': i[1],
                '訂單總價': i[2],
                '訂單時間': i[3]
            }
            order_data.append(order)
            
        orderdetail_row = Order_List.get_orderdetail()
        order_detail = []

        for j in orderdetail_row:
            orderdetail = {
                '訂單編號': j[0],
                '商品名稱': j[1],
                '商品單價': j[2],
                '訂購數量': j[3]
            }
            order_detail.append(orderdetail)

    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)