from typing import Optional
from link import *

class DB():
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()

class Member():
    def get_member(account):
        # sql = "SELECT ACCOUNT, PASSWORD, MID, IDENTITY, NAME FROM MEMBER WHERE ACCOUNT = :id"
        sql = "SELECT USERID, PASSWORD, IDENTITY, NAME FROM ACCOUNT WHERE USERID = :id"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'id' : account}))
    
    def get_all_account():
        # sql = "SELECT ACCOUNT FROM MEMBER"
        sql = "SELECT USERID FROM ACCOUNT"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def create_member(input):
        # sql = 'INSERT INTO MEMBER VALUES (null, :name, :account, :password, :identity)'
        sql = 'INSERT INTO ACCOUNT VALUES (:userid, :password, :identity, :name)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(tno, pid):
        sql = 'DELETE FROM RECORD WHERE TNO=:tno and PID=:pid '
        DB.execute_input(DB.prepare(sql), {'tno': tno, 'pid':pid})
        DB.commit()
        
    def get_order(userid):
        sql = 'SELECT * FROM ORDER_LIST WHERE MID = :id ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':userid}))
    
    def get_role(userid):
        # sql = 'SELECT IDENTITY, NAME FROM MEMBER WHERE MID = :id '
        sql = 'SELECT IDENTITY, NAME FROM ACCOUNT WHERE USERID = :id '
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':userid}))

class Cart():
    def check(user_id):
        sql = 'SELECT * FROM CART, RECORD WHERE CART.MID = :id AND CART.TNO = RECORD.TNO'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
        
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))

    def add_cart(user_id, time):
        sql = 'INSERT INTO CART VALUES (:id, :time, cart_tno_seq.nextval)'
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time})
        DB.commit()

    def clear_cart(user_id):
        sql = 'DELETE FROM CART WHERE MID = :id '
        DB.execute_input( DB.prepare(sql), {'id': user_id})
        DB.commit()
       
class Product():
    def count():
        # sql = 'SELECT COUNT(*) FROM PRODUCT'
        sql = 'SELECT COUNT(*) FROM PATIENT'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    
    def get_product(pid):
        # sql ='SELECT * FROM PRODUCT WHERE PID = :id'
        sql ='SELECT * FROM PATIENT WHERE PNO = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))
    
    def get_doctor(eid):
        sql ='SELECT * FROM DOCTOR WHERE EID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': eid}))
    
    def get_be_occupied(eid):
        sql ='SELECT * FROM BE_OCCUPIED WHERE BID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': eid}))
    
    def get_vital_sign(pid):
        sql ='SELECT * FROM VITAL_SIGN WHERE PNO = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))
    
    def get_bedId(pid):
        sql ='SELECT * FROM BE_OCCUPIED WHERE PNO = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))

    def get_all_product():
        # sql = 'SELECT * FROM PRODUCT'
        sql = 'SELECT * FROM PATIENT'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_all_vital_sign():
        # sql = 'SELECT * FROM PRODUCT'
        sql = 'SELECT * FROM VITAL_SIGN'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_all_doctor():
        sql = 'SELECT * FROM DOCTOR'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_all_be_occupied():
        sql = 'SELECT * FROM BE_OCCUPIED'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_name(pid):
        # sql = 'SELECT PNAME FROM PRODUCT WHERE PID = :id'
        sql = 'SELECT NAME FROM PATIENT WHERE PNO = :id'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':pid}))[0]

    def add_product(input):
        # sql = 'INSERT INTO PRODUCT VALUES (:pid, :name, :price, :category, :description)'
        sql = 'INSERT INTO PATIENT VALUES (:pid, :name, :category, :price, :description,null,null,null,''91102'')'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def add_vital_sign(input):
        sql = 'INSERT INTO VITAL_SIGN VALUES (:seqtime, :rr, :bp, :spo2, :bt, :score, :risk, :pid, :pulse)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def add_doctor(input):
        sql = 'INSERT INTO DOCTOR VALUES (:eid, :name, :department)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def addbe_occupied(input):
        sql = 'INSERT INTO BE_OCCUPIED VALUES (:bid, :pno, :starttime, :endtime)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def delete_vital_sign(pid):
        sql = 'DELETE FROM VITAL_SIGN WHERE SEQTIME = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()
    
    def delete_product(pid):
        # sql = 'DELETE FROM PRODUCT WHERE PID = :id '
        sql = 'DELETE FROM PATIENT WHERE PNO = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()

    def delete_doctor(pid):
        sql = 'DELETE FROM DOCTOR WHERE EID = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()

    def delete_be_occupied(pid):
        sql = 'DELETE FROM BE_OCCUPIED WHERE EID = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()

    def update_product(input):
        # sql = 'UPDATE PRODUCT SET PNAME=:name, PRICE=:price, CATEGORY=:category, PDESC=:description WHERE PID=:pid'
        sql = 'UPDATE PATIENT SET NAME=:name, SEX=:category, BIRTH=:price, DIAGNOSIS=:description WHERE PNO=:pid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def update_vital_sign(input):
        # sql = 'UPDATE PRODUCT SET PNAME=:name, PRICE=:price, CATEGORY=:category, PDESC=:description WHERE PID=:pid'
        sql = 'UPDATE VITAL_SIGN SET PNO=:pid, RR=:rr, BP=:bp, SPO2=:spo2, BT=:bt, SCORE=:score, RISK=:risk, PULSE=:pulse WHERE SEQTIME=:septime'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def update_doctor(input):
        sql = 'UPDATE DOCTOR SET NAME=:name, DEPARTMENT=:department WHERE EID=:eid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def update_be_occupied(input):
        sql = 'UPDATE BE_OCCUPIED SET PNO=:pno, STARTTIME=:starttime,ENDTIME=:endtime WHERE BID=:bid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

class Surgery():
    def count():
        sql = 'SELECT COUNT(*) FROM UNDERGOES'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    
    def get_undergoes(pid):
        sql ='SELECT * FROM UNDERGOES WHERE PNO = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))

    def get_all_undergoes():
        sql = 'SELECT * FROM UNDERGOES'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_name(pid):
        sql = 'SELECT SURGEON FROM UNDERGOES WHERE PNO = :id'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':pid}))[0]

    # def add_product(input):
    #     sql = 'INSERT INTO PRODUCT VALUES (:pid, :name, :price, :category, :description)'

    #     DB.execute_input(DB.prepare(sql), input)
    #     DB.commit()
    
    # def delete_product(pid):
    #     sql = 'DELETE FROM PRODUCT WHERE PID = :id '
    #     DB.execute_input(DB.prepare(sql), {'id': pid})
    #     DB.commit()

    # def update_product(input):
    #     sql = 'UPDATE PRODUCT SET PNAME=:name, PRICE=:price, CATEGORY=:category, PDESC=:description WHERE PID=:pid'
    #     DB.execute_input(DB.prepare(sql), input)
    #     DB.commit()
    
class Record():
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'tno': tno}))[0]

    def check_product(pid, tno):
        sql = 'SELECT * FROM RECORD WHERE PID = :id and TNO = :tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid, 'tno':tno}))

    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))[0]

    def add_product(input):
        sql = 'INSERT INTO RECORD VALUES (:id, :tno, 1, :price, :total)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = :id'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'id': tno}))

    def get_amount(tno, pid):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = :id and PID=:pid'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'id': tno, 'pid':pid}) )[0]
    
    def update_product(input):
        sql = 'UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE PID=:pid and TNO=:tno'
        DB.execute_input(DB.prepare(sql), input)

    def delete_check(pid):
        sql = 'SELECT * FROM RECORD WHERE PID=:pid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pid':pid}))

    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':tno}))[0]
    

class Order_List():
    def add_order(input):
        sql = 'INSERT INTO ORDER_LIST VALUES (null, :mid, TO_DATE(:time, :format ), :total, :tno)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_order():
        sql = 'SELECT OID, NAME, PRICE, ORDERTIME FROM ORDER_LIST NATURAL JOIN MEMBER ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_orderdetail():
        sql = 'SELECT O.OID, P.PNAME, R.SALEPRICE, R.AMOUNT FROM ORDER_LIST O, RECORD R, PRODUCT P WHERE O.TNO = R.TNO AND R.PID = P.PID'
        return DB.fetchall(DB.execute(DB.connect(), sql))


class Analysis():
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), SUM(PRICE) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i}))

    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), COUNT(OID) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i}))
    
    def category_discharge():
        # sql = 'SELECT SUM(TOTAL), CATEGORY FROM(SELECT * FROM PRODUCT,RECORD WHERE PRODUCT.PID = RECORD.PID) GROUP BY CATEGORY'
        sql = 'SELECT COUNT(*), DISCHARGE FROM PATIENT GROUP BY DISCHARGE'
        return DB.fetchall( DB.execute( DB.connect(), sql))
    
    def category_sex():
        # sql = 'SELECT SUM(TOTAL), CATEGORY FROM(SELECT * FROM PRODUCT,RECORD WHERE PRODUCT.PID = RECORD.PID) GROUP BY CATEGORY'
        sql = 'SELECT COUNT(*), SEX FROM PATIENT GROUP BY SEX'
        return DB.fetchall( DB.execute( DB.connect(), sql))

    def member_sale():
        sql = 'SELECT SUM(PRICE), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY SUM(PRICE) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))

    def member_sale_count():
        sql = 'SELECT COUNT(*), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY COUNT(*) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))