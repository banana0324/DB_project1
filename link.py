import cx_Oracle
# cx_Oracle.init_oracle_client(lib_dir="./instantclient_19_8") # init Oracle instant client 位置
cx_Oracle.init_oracle_client()
connection = cx_Oracle.connect('GROUP5', 'EPAepUAIaB', cx_Oracle.makedsn('140.117.69.60', 1521, service_name='ORCLPDB1'))
cursor = connection.cursor()