from os import stat
from flask import Flask, render_template, request, redirect, url_for, flash, Request
import textwrap
import pyodbc

app = Flask(__name__)
app.secret_key="ABCDEF"


#######---------------------Databese Connection--------------------------------######

#specify the driver
driver = '{ODBC Driver 17 for SQL Server}'

#specify the server name and database name
server_name = 'assignment1-adithya'
database_name = 'assignment-1'

#create server URL
server = '{server_name}.database.windows.net,1433'.format(server_name=server_name)

#define username and Password
username = 'adithya'
password = 'Constallation123'


#create full connection string
connection_string = textwrap.dedent(''' 
    Driver={driver};
    Server={server};
    Database={database};
    Uid={username};
    Pwd={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
'''.format(
    driver=driver,
    server=server,
    database=database_name,
    username=username,
    password=password
))

cnxn: pyodbc.Connection = pyodbc.connect(connection_string)
crsr: pyodbc.Cursor = cnxn.cursor()




#-------------------------------------------------End of Database Connection-----------------------------------------------------------------#

@app.route('/', methods=["POST","GET"])
def start():
    return render_template('index.html')

@app.route('/Query1', methods=["POST","GET"])
def q1():   
    mag_5_sql="Select * from [all_month] where mag>5.0"
    crsr.execute(mag_5_sql)
    mag_5_list=crsr.fetchall()
    count=len(mag_5_list)
    return render_template('magnitude5.html', list1=mag_5_list, count=count)


@app.route('/Query2', methods=["POST","GET"])
def q2():
    frmag=str(request.form.get("frmag"))
    tomag=str(request.form.get("tomag"))
    frdate=str(request.form.get("frdate"))
    print(frdate)
    todate=str(request.form.get("todate"))
    print(todate)
    crsr.execute("Select * from [all_month] where mag>="+frmag+" and mag<="+tomag+" and time>='"+frdate+"' and time<='"+todate+"'")
    magrange=crsr.fetchall()
    return render_template('magandtime.html', data=magrange)

@app.route('/Query3', methods=["POST","GET"])
def q3():
    latitude=str(request.form.get("latitude"))
    longitude=str(request.form.get("longitude"))
    distance=str(request.form.get("distance"))

    ## Coverting KMS to Degrees  ##

    neglatitude=float(latitude)-float(distance)/111
    neglongitude=float(longitude)-float(distance)/111
    poslatitude=float(latitude)+float(distance)/111
    poslongitude=float(longitude)+float(distance)/111

    loaction_sql="Select * from [all_month] where latitude>="+str(neglatitude)+" and latitude<="+str(poslatitude)+" and longitude>="+str(neglongitude)+" and longitude<="+str(poslongitude)
    crsr.execute(loaction_sql)
    loactiondata=crsr.fetchall()
    return render_template('locationwise.html', data=loactiondata)


@app.route('/Query4', methods=["POST","GET"])
def q4():
    mag=request.form.get("mag")
    cluster_sql="Select * from [all_month] where mag="+mag
    crsr.execute(cluster_sql)
    cluster_list=crsr.fetchall()
    count=len(cluster_list)
    return render_template('cluster.html', data=cluster_list, count=count)

@app.route('/Query5', methods=["POST","GET"])
def q5():
    magnitude=request.form.get("nightmag")
    nightquakes_sql="SELECT * from [all_month] WHERE MAG > "+magnitude+"  AND (DATEADD(day, -DATEDIFF(day, 0, time), time) > '00:10:10.000' and DATEADD(day, -DATEDIFF(day, 0, time), time) < '05:00:00.000');"
    crsr.execute(nightquakes_sql)
    night_list=crsr.fetchall()
    return render_template('nightquakes.html', data=night_list)


if __name__ == '__main__':
    
  app.run(host='127.0.0.1', port=8080, debug=True)
  app.config['JSON_SORT_KEYS']=False