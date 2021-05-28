from flask import Flask, request, render_template
import os
from math import radians, degrees, cos, sin, asin, sqrt
import csv, base64, time
import pymysql
import random
import time
import hashlib
import pickle
from datetime import datetime
from json import loads, dumps
from timeit import default_timer as timer
from time import *
import time


application = Flask(__name__)

db = pymysql.connect(user='',
                     password='',
                     host='',
                     database='',
                     cursorclass=pymysql.cursors.DictCursor)
# Enter user, password and host. Deleted for security purposes
cursor = db.cursor()

@application.route("/")
def home():
    return render_template('home.html')

@application.route("/volcanocheck", methods=["POST", "GET"])
def volcanocheck():

    vno = int(request.form['vno'])

    start_time = time.time()

    sql1 = "SELECT VolcanoName, Latitude, Longitude FROM volcano WHERE Num= '" + str(vno) +"'"
    cursor.execute(sql1)
    rows = cursor.fetchall()

    if rows is not None:
        pass

    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template("volcanocheck.html", rows=rows,rowcount=len(rows),elapsed_time=elapsed_time)

@application.route("/volcanoupdate", methods=["POST", "GET"])
def volcanoupdate():
    vno = int(request.form['vno'])
    vname = request.form['newname']

 

    sql1 = "update volcano set VolcanoName='" + str(vname) + "' WHERE Num= '" + str(vno) + "'"
    cursor.execute(sql1)
    sql3 = "COMMIT"
    cursor.execute(sql3)
    sql2 = "SELECT VolcanoName, Latitude,Longitude FROM volcano WHERE Num= '" + str(vno) + "'"
    cursor.execute(sql2)
    rows = cursor.fetchall()

 

    return render_template("volcanoupdate.html", rows=rows,rowcount=len(rows))


@application.route('/box', methods=['POST'])
def box():
    latitude1 = request.form['latitude1']
    longitude1 = request.form['longitude1']
    latitude2 = request.form['latitude2']
    longitude2 = request.form['longitude2']
    start_time = time.time()
    query1 = "SELECT * from volcano where Latitude BETWEEN '"+ latitude1 + "' AND  '"+ latitude2 + "' AND Longitude BETWEEN '"+ longitude1 +"' AND '"+ longitude2 + "'"
    cursor.execute(query1)
    rows = cursor.fetchall()
    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template('box.html',rows=rows, rowcount=len(rows),elapsed_time=elapsed_time)

@application.route("/timer", methods=["POST", "GET"])
def timer():


    return render_template("timer.html")

@application.route("/set", methods=["POST", "GET"])
def set():


    return render_template("set.html")


@application.route("/elevrange", methods=["POST", "GET"])
def elevrange():
    elevStart = float(request.form['elevStart'])
    elevEnd = float(request.form['elevEnd'])
    net  = float(request.form['increment'])
    start = elevStart
    counts = []
    starts = []
    ends = []
    end = start + net
    start_time = time.time()
    while end <= elevEnd:
        query1 = "SELECT * from volcano where Elev >= '"+ str(start) +"' AND Elev <= '" + str(end)+"'"
        cursor.execute(query1)
        result = cursor.fetchall()
        rows = []
        count = 0
        starts.append(start)
        ends.append(end)
        counts.append(len(result))
        start = end
        end = start + net
    length = len(starts)
    end_time = time.time()
    elapsed_time = end_time-start_time
    return render_template('elevrange.html', starts=starts,ends=ends,counts=counts,length=length)

@application.route("/crwise", methods=["POST", "GET"])
def crwise():
    region = request.form['region']
    country = request.form['country']

    start_time = time.time()

    sql1 = "SELECT Country,count(*) as noofvolcanoes FROM volcano WHERE Country = '" + str(country) + "' group by Country"
    cursor.execute(sql1)
    rows = cursor.fetchall()
    sql2 = "SELECT Region,count(*) as noofvolcanoes FROM volcano WHERE Region like '%"+str(region)+"%' group by Region"
    cursor.execute(sql2)
    rows1 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template("crwise.html", rows=rows,rows1=rows1,elapsed_time=elapsed_time)
# @application.route('/register', methods=["POST","GET"])
# def register():

#     crlist=[]
#     cid = int(request.form.get('id'))
#     sec = int(request.form.get('sec'))
#     idnum = int(request.form.get('idnum'))
#     fn = request.form.get('fname')
#     ln = request.form.get('lname')
#     age = int(request.form.get('age'))
#     val = (idnum, fn, ln, age)

#     query000 = "SELECT idnum FROM students WHERE idnum = '" + str(idnum) + "'"
#     cursor.execute(query000)
#     t000 = cursor.fetchone()

#     if t000 is None:
#         query6 = "INSERT INTO students (idnum,fname,lname,age,credit,NoOfClasses) VALUES (%s,%s,%s,%s,20,0)"
#         cursor.execute(query6,val)
#         print('executed')
#         sql8 = "COMMIT"
#         cursor.execute(sql8)
#         query7 = "SELECT * FROM students WHERE idnum = '" + str(idnum) + "'"
#         cursor.execute(query7)
#         t7 = cursor.fetchall()
#     else:
#         query7 = "SELECT * FROM students WHERE idnum = '" + str(idnum) + "'"
#         cursor.execute(query7)
#         t7 = cursor.fetchall()

#     query8 = "SELECT * FROM courses where Course='" + str(cid) + "'"
#     cursor.execute(query8)
#     t8 = cursor.fetchall()

#     query01 = "SELECT credit FROM students where idnum='" + str(idnum) + "'"
#     cursor.execute(query01)
#     t01 = cursor.fetchone()
#     cre = t01.get('credit')


#     query02 = "SELECT NoOfClasses FROM students where idnum='" + str(idnum) + "'"
#     cursor.execute(query02)
#     t02 = cursor.fetchone()
#     noc = t02.get('NoOfClasses')


#     query1 = "SELECT max FROM courses WHERE course = '" + str(cid) + "' AND section='" + str(sec) + "' AND max!=0"
#     cursor.execute(query1)
#     t1 = cursor.fetchone()
#     print(t1)


#     if t1 is not None and age >= 60 and noc < 10 and cre >= 10:
#         query2 = "UPDATE courses SET max = max-1 WHERE course = '" + str(cid) + "' AND section='" + str(sec) + "'"
#         cursor.execute(query2)
#         sql9 = "COMMIT"
#         cursor.execute(sql9)
#         query3 = "UPDATE students SET NoOfClasses = NoOfClasses+1,credit= credit-10 WHERE idnum = '" + str(idnum) + "'"
#         cursor.execute(query3)
#         sql10 = "COMMIT"
#         cursor.execute(sql10)
#         crlist.append(cid)
#         sql4 = "INSERT INTO studentcourse VALUES ('" + str(idnum) + "', '" + str(cid) + "', '" + str(sec) + "')"
#         cursor.execute(sql4)
#         sql9 = "COMMIT"
#         cursor.execute(sql9)
#     elif t1 is not None and age < 60 and noc < 10 and cre >= 20:
#         query8 = "UPDATE courses SET max = max-1 WHERE course = '" + str(cid) + "' AND section='" + str(sec) + "'"
#         cursor.execute(query8)
#         sql11 = "COMMIT"
#         cursor.execute(sql11)
#         query9 = "UPDATE students SET NoOfClasses = NoOfClasses+1,credit= credit-20 WHERE idnum = '" + str(idnum) + "'"
#         cursor.execute(query9)
#         sql12 = "COMMIT"
#         cursor.execute(sql12)
#         crlist.append(cid)
#         sql14 = "INSERT INTO studentcourse VALUES ('" + str(idnum) + "', '" + str(cid) + "', '" + str(sec) + "')"
#         cursor.execute(sql14)
#         sql19 = "COMMIT"
#         cursor.execute(sql19)
#     else :
#         print("")

#     query4 = "SELECT * FROM courses WHERE course = '" + str(cid) + "' AND section='" + str(sec) + "'"
#     cursor.execute(query4)
#     t2 = cursor.fetchone()
#     print('old max', t2)
#     query5 = "SELECT * FROM students WHERE idnum = '" + str(idnum) + "' AND fname='" + str(fn) + "' AND lname = '" + str(ln) + "'"
#     cursor.execute(query5)
#     t3 = cursor.fetchall()
#     print('stud', t3)
#     query40 = "SELECT * FROM studentcourse WHERE IdNum = '" + str(idnum) + "'"
#     cursor.execute(query40)
#     t20 = cursor.fetchall()
#     return render_template('p1.html', res1=t1, res2=t2, res3=t3, res7=t7, table=t20, table1=t3)

# @application.route("/update", methods=["POST", "GET"])
# def update():
#     idnum = int(request.form['idnum'])
#     course = int(request.form['course'])
#     section = int(request.form['section'])

#     start_time = time.time()

#     sql1 = "SELECT idnum FROM students WHERE idnum = '" + str(idnum) + "'"
#     cursor.execute(sql1)
#     rows1 = cursor.fetchall()

#     sql2 = "SELECT max FROM courses WHERE course = '" + str(course) + "' AND section = '" + str(section) + "' AND max <> 0"
#     cursor.execute(sql2)
#     rows2 = cursor.fetchall()

#     if rows1 and rows2 is not None:
#         sql3 = "UPDATE courses SET max = max-1 WHERE course = '" + str(course) + "' AND section = '" + str(section) + "'"
#         cursor.execute(sql3)
#         sql8 = "COMMIT"
#         cursor.execute(sql8)
#         sql4 = "INSERT INTO cloud.studentcourse VALUES ('" + str(idnum) + "', '" + str(course) + "', '" + str(section) + "')"
#         cursor.execute(sql4)
#         sql9 = "COMMIT"
#         cursor.execute(sql9)

#     sql5 = "SELECT max FROM courses WHERE course = '" + str(course) + "' AND section = '" + str(section) + "'"
#     cursor.execute(sql5)
#     rows5 = cursor.fetchall()

#     sql6 = "SELECT * FROM studentcourse"
#     cursor.execute(sql6)
#     rows6 = cursor.fetchall()

#     sql7 = "SELECT sc.idnum, sc.course, sc.section, c.max FROM students as s, courses as c, studentcourse as sc WHERE sc.idnum=s.idnum AND sc.course=c.course AND sc.section=c.section"
#     cursor.execute(sql7)
#     rows7 = cursor.fetchall()

#     end_time = time.time()
#     elapsed_time = end_time-start_time

#     return render_template("studentcourse.html", rows1=rows1, rows2=rows2, rows5=rows5,rows6=rows6, rows7=rows7, elapsed_time=elapsed_time)

# @application.route('/')
# def index():

#     #query = "select min(mag) from earth"
#     #query = "CREATE TABLE dbo.earth101(time DATETIME,latitude FLOAT,longitude FLOAT,depth FLOAT,mag FLOAT,magType TEXT,nst INT,gap INT,dmin FLOAT,rms FLOAT,net TEXT,id TEXT,updated DATETIME,place TEXT,type TEXT,horontalError FLOAT,depthError FLOAT,magError FLOAT,magNst INT,status TEXT,locationSource TEXT,magSource TEXT)"

#     s11=timer()
#     query111 = "SELECT yr2010 FROM population WHERE state='Texas' or state='Texas'"
#     cursor.execute(query111)
#     r11 = cursor.fetchall()
#     e11=timer()
#     ep1 = e11-s11
#     s12 = timer()
#     query112 = "SELECT yr2010 FROM population WHERE state='Texas' or state='Louisiana'"
#     cursor.execute(query112)
#     r12 = cursor.fetchall()
#     e12 = timer()
#     ep2 = e12-s12

#     s13 = timer()
#     query113 = "SELECT yr2010 FROM population WHERE state='Texas' or state='Oklahoma'"
#     cursor.execute(query113)
#     r13 = cursor.fetchall()
#     e13 = timer()
#     ep3 = e13-s13

#     return render_template('index.html', ep1=ep1, ep2=ep2, ep3=ep3, res11=r11, s11=s11, e11=e11, res12=r12, s12=s12,e12=e12, res13=r13,s13=s13,e13=e13)

# @application.route('/p2', methods=['POST', 'GET'])
# def p2():
#     s11 = timer()
#     query121 = "SELECT yr2011 FROM population WHERE state='Texas' or state='Texas'"
#     cursor.execute(query121)
#     r11 = cursor.fetchall()
#     e11 = timer()
#     s12 = timer()
#     query122 = "SELECT yr2011 FROM population WHERE state='Texas' or state='Louisiana'"
#     cursor.execute(query122)
#     r12 = cursor.fetchall()
#     e12 = timer()

#     s13 = timer()
#     query123 = "SELECT yr2011 FROM population WHERE state='Texas' or state='Oklahoma'"
#     cursor.execute(query123)
#     r13 = cursor.fetchall()
#     e13 = timer()

#     return render_template('p2.html', res11=r11, s11=s11, e11=e11, res12=r12, s12=s12, e12=e12, res13=r13, s13=s13,e13=e13)

# @application.route('/p3', methods=['POST', 'GET'])
# def p3():
#     s11 = timer()
#     query131 = "SELECT yr2012 FROM population WHERE state='Texas' or state='Texas'"
#     cursor.execute(query131)
#     r11 = cursor.fetchall()
#     e11 = timer()

#     s12 = timer()
#     query132 = "SELECT yr2012 FROM population WHERE state='Texas' or state='Louisiana'"
#     cursor.execute(query132)
#     r12 = cursor.fetchall()
#     e12 = timer()

#     s13 = timer()
#     query133 = "SELECT yr2012 FROM population WHERE state='Texas' or state='Oklahoma'"
#     cursor.execute(query133)
#     r13 = cursor.fetchall()
#     e13 = timer()
#     return render_template('p3.html', res11=r11, s11=s11, e11=e11, res12=r12, s12=s12, e12=e12, res13=r13, s13=s13,e13=e13)

# @application.route('/p4', methods=['POST', 'GET'])
# def p4():
#     s11 = timer()
#     query141 = "SELECT yr2013 FROM population WHERE state='Texas' or state='Texas'"
#     cursor.execute(query141)
#     r11 = cursor.fetchall()
#     e11 = timer()
#     s12 = timer()
#     query142 = "SELECT yr2013 FROM population WHERE state='Texas' or state='Louisiana'"
#     cursor.execute(query142)
#     r12 = cursor.fetchall()
#     e12 = timer()

#     s13 = timer()
#     query143 = "SELECT yr2013 FROM population WHERE state='Texas' or state='Oklahoma'"
#     cursor.execute(query143)
#     r13 = cursor.fetchall()
#     e13 = timer()
#     return render_template('p4.html', res11=r11, s11=s11, e11=e11, res12=r12, s12=s12, e12=e12, res13=r13, s13=s13,e13=e13)

# @application.route('/p5', methods=['POST', 'GET'])
# def p5():
#     s11 = timer()
#     query151 = "SELECT yr2014 FROM population WHERE state='Texas' or state='Texas'"
#     cursor.execute(query151)
#     r11 = cursor.fetchall()
#     e11 = timer()
#     s12 = timer()
#     query152 = "SELECT yr2014 FROM population WHERE state='Texas' or state='Louisiana'"
#     cursor.execute(query152)
#     r12 = cursor.fetchall()
#     e12 = timer()

#     s13 = timer()
#     query153 = "SELECT yr2014 FROM population WHERE state='Texas' or state='Oklahoma'"
#     cursor.execute(query153)
#     r13 = cursor.fetchall()
#     e13 = timer()
#     return render_template('p5.html', res11=r11, s11=s11, e11=e11, res12=r12, s12=s12, e12=e12, res13=r13, s13=s13, e13=e13)

# @application.route('/p6', methods=['POST', 'GET'])
# def p6():
#     s11 = timer()
#     query161 = "SELECT yr2015 FROM population WHERE state='Texas' or state='Texas'"
#     cursor.execute(query161)
#     r11 = cursor.fetchall()
#     e11 = timer()
#     s12 = timer()
#     query162 = "SELECT yr2015 FROM population WHERE state='Texas' or state='Louisiana'"
#     cursor.execute(query162)
#     r12 = cursor.fetchall()
#     e12 = timer()

#     s13 = timer()
#     query163 = "SELECT yr2015 FROM population WHERE state='Texas' or state='Oklahoma'"
#     cursor.execute(query163)
#     r13 = cursor.fetchall()
#     e13 = timer()
#     return render_template('p6.html', res11=r11, s11=s11, e11=e11, res12=r12, s12=s12, e12=e12, res13=r13, s13=s13, e13=e13)

# @application.route('/p7', methods=['POST', 'GET'])
# def p7():
#     s11 = timer()
#     query171 = "SELECT yr2016 FROM population WHERE state='Texas' or state='Texas'"
#     cursor.execute(query171)
#     r11 = cursor.fetchall()
#     e11 = timer()
#     s12 = timer()
#     query172 = "SELECT yr2016 FROM population WHERE state='Texas' or state='Louisiana'"
#     cursor.execute(query172)
#     r12 = cursor.fetchall()
#     e12 = timer()

#     s13 = timer()
#     query173 = "SELECT yr2016 FROM population WHERE state='Texas' or state='Oklahoma'"
#     cursor.execute(query173)
#     r13 = cursor.fetchall()
#     e13 = timer()
#     return render_template('p7.html', res11=r11, s11=s11, e11=e11, res12=r12, s12=s12, e12=e12, res13=r13, s13=s13, e13=e13)

# @application.route('/p8', methods=['POST', 'GET'])
# def p8():
#     s11 = timer()
#     query181 = "SELECT yr2017 FROM population WHERE state='Texas' or state='Texas'"
#     cursor.execute(query181)
#     r11 = cursor.fetchall()
#     e11 = timer()
#     s12 = timer()
#     query182 = "SELECT yr2017 FROM population WHERE state='Texas' or state='Louisiana'"
#     cursor.execute(query182)
#     r12 = cursor.fetchall()
#     e12 = timer()

#     s13 = timer()
#     query138 = "SELECT yr2017 FROM population WHERE state='Texas' or state='Oklahoma'"
#     cursor.execute(query138)
#     r13 = cursor.fetchall()
#     e13 = timer()
#     return render_template('p8.html', res11=r11, s11=s11, e11=e11, res12=r12, s12=s12, e12=e12, res13=r13, s13=s13,e13=e13)

# @application.route('/p9', methods=['POST', 'GET'])
# def p9():
#     s11 = timer()
#     query119 = "SELECT yr2018 FROM population WHERE state='Texas' or state='Texas'"
#     cursor.execute(query119)
#     r11 = cursor.fetchall()
#     e11 = timer()
#     s12 = timer()
#     query129 = "SELECT yr2018 FROM population WHERE state='Texas' or state='Louisiana'"
#     cursor.execute(query129)
#     r12 = cursor.fetchall()
#     e12 = timer()

#     s13 = timer()
#     query139 = "SELECT yr2018 FROM population WHERE state='Texas' or state='Oklahoma'"
#     cursor.execute(query139)
#     r13 = cursor.fetchall()
#     e13 = timer()
#     return render_template('p9.html', res11=r11, s11=s11, e11=e11, res12=r12, s12=s12, e12=e12, res13=r13, s13=s13,e13=e13)




# @application.route('/noqueries', methods=['POST', 'GET'])
# def noqueries():

#     total2 = 0
#     total22 = 0
#     NoOfClasses = int(request.form.get('NoOfClasses', ''))
#     query2 = "SELECT * FROM quake WHERE mag>3"

#     res_list1 = []
#     for number in range(0, NoOfClasses):
#         start22 = timer()
#         cursor.execute(query2)
#         t22 = cursor.fetchall()
#         res_list1.append(t22)
#         end22 = timer()
#         total22 = (end22 - start22) + total22
#     avg22 = (total22 / NoOfClasses)
#     print('hi22')

#     return render_template('index.html', times=NoOfClasses, totaltime22=total22, avgtime22=avg22)


# @application.route('/restqueries', methods=['POST', 'GET'])
# def restqueries():

#     n = int(request.form.get('n', ''))
#     mag1 = float(request.form.get('m1', ''))
#     mag2 = float(request.form.get('m2', ''))
#     total3 = 0


#     #for i in range(0, n):
#         #val = random.uniform(mag1, mag2)
#         #magval = round(val, 2)


#     total33 = 0

#     for number in range(0, n):
#         start33 = timer()
#         val = random.uniform(mag1, mag2)
#         magval = round(val, 2)
#         query3 = "SELECT * FROM quake WHERE mag = '" + str(magval) + "'"
#         cursor.execute(query3)
#         t33 = cursor.fetchall()
#         end33 = timer()
#         total33 = (end33 - start33) + total33
#     avg33 = (total33 / n)
#     print('hi22')

#     return render_template('index.html', times3=n, totaltime3=total3, totaltime33=total33, avgtime33=avg33)


# @application.route('/restqueries2', methods=['POST', 'GET'])
# def restqueries2():
#     n2 = int(request.form.get('n2', ''))
#     mg1 = float(request.form.get('mg1', ''))
#     mg2 = float(request.form.get('mg2', ''))
#     total4 = 0

#     start4 = timer()
#     #for i in range(0, n2):
#         #val = random.uniform(mg1, mg2)
#         #magval = round(val, 2)
#         #query4 = "SELECT * FROM asmita820.earth WHERE mag = '"+str(magval)+"' AND locsrc='ak'"


#     total44 = 0
#     for number in range(0, n2):
#         start44 = timer()
#         val = random.uniform(mg1, mg2)
#         magval = round(val, 2)
#         query4 = "SELECT * FROM quake WHERE mag = '"+str(magval)+"' AND net='us'"
#         cursor.execute(query4)
#         t44 = cursor.fetchall()
#         end44 = timer()
#         total44 = (end44-start44)+total44
#     avg44 = (total44/n2)
#     print('hi2')

#     return render_template('index.html', times4=n2, totaltime4=total4, totaltime44=total44, avgtime44=avg44)

# @application.route('/restqueries3', methods=['POST', 'GET'])
# def restqueries3():
#     n2 = int(request.form.get('n2', ''))
#     dp1 = float(request.form.get('mg1', ''))
#     dp2 = float(request.form.get('mg2', ''))
#     vals = []
#     timeq = []


#     #for i in range(0, n):
#         #val = random.uniform(mag1, mag2)
#         #magval = round(val, 2)


#     total55 = 0

#     for number in range(0, n2):
#         val1 = random.uniform(dp1, dp2)
#         vals.append(val1)
#         val2 = random.uniform(dp1, dp2)
#         vals.append(val2)
#         start55 = timer()
#         query5 = "SELECT place, gmttime, depthError FROM quake WHERE deptherr BETWEEN '" + str(val1) + "' AND '" + str(val2) + "'"
#         cursor.execute(query5)
#         t55 = cursor.fetchall()
#         end55 = timer()
#         total55 = (end55 - start55) + total55
#     avg55 = (total55 / n2)
#     print('hi22')

#     return render_template('index.html', times5=n2, totaltime55=total55, avgtime55=avg55)

# @application.route("/")
# def home():
#     return render_template('home.html')


# @application.route("/greaterthan", methods=["POST", "GET"])
# def greaterthan():
#     range1 = float(request.form['range1'])

#     start_time = timer()

#     sql1 = "SELECT * FROM quake WHERE mag > '" + str(range1) + "'"
#     cursor.execute(sql1)
#     rows1 = cursor.fetchall()

#     end_time = timer()
#     elapsed_time = end_time-start_time

#     return render_template("greaterthan.html", rows=rows1, rowcount=len(rows1), elapsed_time=elapsed_time)


# @application.route("/withinrange", methods=["POST", "GET"])
# def withinrange():
#     range1 = float(request.form['range1'])
#     range2 = float(request.form['range2'])

#     start_time = timer()

#     sql1 = "SELECT * FROM quake WHERE mag between '" + str(range1) + "' AND '" + str(range2) + "'"
#     cursor.execute(sql1)
#     rows1 = cursor.fetchall()

#     end_time = timer()
#     elapsed_time = end_time-start_time

#     return render_template("withinrange.html", rows=rows1, rowcount=len(rows1), elapsed_time=elapsed_time)


# @application.route("/update", methods=["POST", "GET"])
# def update():
#     range1 = float(request.form['range1'])
#     range2 = float(request.form['range2'])
#     startdate = (request.form['startdate'])
#     enddate = (request.form['enddate'])
#     mag = float(request.form['mag'])

#     start_time = timer()

#     sql1 = "UPDATE quake SET MAG = '" + str(mag) + "'  WHERE DEPTH BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND GMTTIME BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
#     cursor.execute(sql1)

#     # sql2 = "SELECT * FROM dbo.quake WHERE depth between '" + str(range1) + "' AND '" + str(range2) + "' AND GMTTIME BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
#     # cursor.execute(sql2)
#     # rows2 = cursor.fetchall()

#     end_time = timer()
#     elapsed_time = end_time-start_time

#     return render_template("update.html", elapsed_time=elapsed_time)
#     # return render_template("update.html", rows=rows2, rowcount=len(rows2), elapsed_time=elapsed_time)


# def haversine(lon1, lat1, lon2, lat2):
#     # """
#     # Calculate the great circle distance between two points
#     # on the earth (specified in decimal degrees)
#     # """
#     # convert decimal degrees to radians
#     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

#     # haversine formula
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     c = 2 * asin(sqrt(a))
#     r = 6371 # Radius of earth in kilometers. Use 3956 for miles
#     return c * r


# def bounding_box(lat, lon, distance):
#     # Input and output lats/longs are in degrees.
#     # Distance arg must be in same units as RADIUS.
#     # Returns (dlat, dlon) such that
#     # NoOfClasses points outside lat +/- dlat or outside lon +/- dlon
#     # are <= "distance" from the (lat, lon) point.
#     # Derived from: http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
#     # WARNING: problems if North/South Pole is in circle of interest
#     # WARNING: problems if longitude meridian +/-180 degrees intersects circle of interest
#     # See quoted article for how to detect and overcome the above problems.
#     # Note: the result is independent of the longitude of the central point, so the
#     # "lon" arg is not used.
#     r = 6371  # Radius of earth in kilometers. Use 3956 for miles
#     dlat = distance / r
#     dlon = asin(sin(dlat) / cos(radians(lat)))
#     return degrees(dlat), degrees(dlon)


# @application.route("/latlon", methods=["POST", "GET"])
# def latlon():
#     lat = float(request.form['latitude'])
#     lon = float(request.form['longitude'])
#     distance = float(request.form['distance'])

#     start_time = timer()

#     newlat, newlon = bounding_box(lat, lon, distance)

#     sql1 = "SELECT * FROM quake WHERE latitude between '" + str(lat) + "' AND '" + str(newlat) + "' AND longitude between '" + str(lon) + "' and '" + str(newlon) + "'"
#     cursor.execute(sql1)
#     rows1 = cursor.fetchall()

#     end_time = timer()
#     elapsed_time = end_time-start_time

#     return render_template("latlon.html", rows=rows1, rowcount=len(rows1), elapsed_time=elapsed_time)


if __name__ == "__main__":
    application.debug = True
    application.run()