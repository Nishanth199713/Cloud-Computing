import pyodbc
from flask import Flask, request, render_template
import json
from json import loads, dumps

app = Flask(__name__)

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:shanmug12345.database.windows.net,1433;Database=shanmug1234;Uid=shanmug123456;Pwd=shanmug@1969S;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
                
# Enter Server, UID and PWD. Deleted for security purposes
cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('home.html')

# @app.route("/showpie", methods=["POST", "GET"])
# def showpie():
#     category = str(request.form.get('category', ''))
#     query1 = "SELECT * FROM groc WHERE category = '" + str(category) + "'"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()
#     return render_template('showpie.html',category=category,rows=r1)

#user enter category veg or nonveg and display all results of that category - pie chart
#quiz 0a
'''@app.route("/showpiechart", methods=["POST", "GET"])
def showpiechart():
    query1 = "SELECT * FROM grocery WHERE category = 'veg'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT * FROM grocery WHERE category = 'notveg'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    rows1 = ([
        ['Item','Quantity'],
        [r1[0][0],r1[0][2]],
        [r1[1][0],r1[1][2]],
        [r1[2][0],r1[2][2]]
        ])
        
    rows2 = ([
        ['Item','Quantity'],
        [r2[0][0],r2[0][2]],
        [r2[1][0],r2[1][2]]
        ])

    return render_template('showpie.html', rows1=rows1, rows2=rows2)

#5
@app.route("/basic", methods=["POST", "GET"])
def basic():
    query1 = "select StateName from voting where totalpop between 2000 and 8000"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "select StateName from voting where totalpop between 8000 and 40000"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    return render_template('basic.html', rows1=r1, rows2=r2)

#6
@app.route('/regscatter', methods=['POST', 'GET'])
def regscatter():
    m1 = int(request.form.get('m1', ''))
    m2 = int(request.form.get('m2', ''))
    m1 = m1 * 1000
    m2 = m2 * 1000


    query1 = "SELECT sum(Registered) FROM voting WHERE TotalPop BETWEEN '"+str(m1)+"' AND '"+str(m2)+"'"
    cursor.execute(query1)
    s1 = cursor.fetchall()


    rows = ([
        ['reg', 'pop'],
        [str(m1)+'-'+str(m2), s1[0][0]]
        ])
    return render_template('regscatter.html', rows1=rows)

#7
@app.route("/quiz7", methods=["POST", "GET"])
def quiz7():
    range1 = int(request.form.get('range',''))
    rangeStart = 0
    rangeEnd = range1
    maxQuery = "Select max(totalpop) from voting"
    cursor.execute(maxQuery)
    maxResult = cursor.fetchall()
    maxPopulation = maxResult[0][0]
    storeResult = []
    start = []
    end = []
    counter = 0
    while rangeStart < maxPopulation:
        query = "Select count(statename) from voting where totalpop between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
        cursor.execute(query)
        resultSet = cursor.fetchall()
        countResult = resultSet[0][0]
        storeResult.append(countResult)
        start.append(rangeStart)
        end.append(rangeEnd)
        rangeStart = rangeEnd
        rangeEnd = rangeEnd + range1
        counter = counter + 1
    list_a = []
    list_a.append(['Population Range','Number of States'])
    for i in range(0,counter):
        list_a.append([str(start[i]) + '-' + str(end[i]),storeResult[i]])
    return render_template('quizpie.html',rows=list_a)

# 8
# horizontal bar graph show number on each digit generated
@app.route("/horizontalbar", methods=["POST", "GET"])
def horizontalbar():

 

    r1 = []
    range1 = int(request.form.get('range', ''))
    range1 = range1+1
    for i in range(range1):
        modulo = (i**3)%10
        r1.append(modulo)
    
    r2=[]
    
    for i in range(range1):
        count=r1.count(r1[i])
        r2.append(count)
    
    rows = []
    rows.append(['Range Value', 'Number of Times'])
    
    for i in range(0,range1):
        rows.append([r1[i],r2[i]])
    
    return render_template('bar.html', rows=rows)
@app.route("/list", methods=["POST", "GET"])
def list():
    # depthrange1 = float(request.form.get('depthrange1', ''))
    # query1="SELECT * FROM Quakes04 WHERE latitude >= '" + str(latitude1) + "' AND latitude <= '" + str(latitude2) + "' AND longitude >= '" + str(longitude1) + "' AND longitude <= '" + str(longitude2) + "'"
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()
    return render_template('list.html', rows1=r1, rows2=r2, rows3=r3)


@app.route("/showpie", methods=["POST", "GET"])
def showpie():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of quakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]

    ])

    return render_template('quizpie.html', rows=rows)


@app.route("/pie", methods=["POST", "GET"])
def pie():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows1 = ([
        ['Magnitude', 'Number of Quakes04uakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    query8 = "select count(*) from Quakes04 where mag > 5.0 and deptherror > 5"
    cursor.execute(query8)
    r8 = cursor.fetchall()
    query9 = "select count(*) from Quakes04 where mag > 5.0 and deptherror < 5"
    cursor.execute(query9)
    r9 = cursor.fetchall()

    rows2 = ([
        ['Magnitude and Depth Error', 'Number of Quakes04uakes'],
        ['Depth Error > 5', r8[0][0]],
        ['Depth Error < 5', r9[0][0]]

    ])

    return render_template('pie.html', rows=[rows1, rows2])


@app.route("/bar", methods=["POST", "GET"])
def bar():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of Quakes04uakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    return render_template('bar.html', rows=rows)
'''
@app.route("/scatter", methods=["POST", "GET"])
def scatter():
   rows = []
   range1 = int(request.form.get('range1', ''))
   range2 = int(request.form.get('range2', ''))
   query1 = "SELECT number, elev FROM volcano WHERE Number BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
   cursor.execute(query1)
   r1 = cursor.fetchall()
   s1 = [item for t in r1 for item in t]
   s = len(s1)
   print(s1)
   print("\n",s)
   rows.append(["Volcanonumber","range"])
   i = 0
   while i < s:
       if i+1 < s:
           rows.append([s1[i],s1[i+1]])
           i=i+2
       else:
           break
   print("\n",len(rows))
   # rows = ([
   #     ['reg', 'pop'],
   #     [s1[0][0], s1[0][1]]
   #     ])
   print(rows)
 
 
   return render_template('scatter.html', rows=rows)

@app.route("/quizpie", methods=["POST", "GET"])
def quizpie():
    countryname = request.form.get('countryname','')
    range1 = 500
    rangeStart = 0
    rangeEnd = range1
    maxQuery = "Select max(Elev) from volcano"
    #maxQuery = maxQuery * 100
    cursor.execute(maxQuery)
    maxResult = cursor.fetchall()
    maxPopulation = maxResult[0][0]
    storeResult = []
    start = []
    end = []
    counter = 0
    while rangeStart < maxPopulation:
        query = "Select count(Number) from volcano where  Elev between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
        cursor.execute(query)
        resultSet = cursor.fetchall()
        countResult = resultSet[0][0]
        storeResult.append(countResult)
        start.append(rangeStart)
        end.append(rangeEnd)
        rangeStart = rangeEnd
        rangeEnd = rangeEnd + range1
        counter = counter + 1
    list_a = []
    list_a.append(['Population Range','Number of States'])
    for i in range(0,counter):
        list_a.append([str(start[i]) + '-' + str(end[i]),storeResult[i]])

    return render_template('quizpie.html', rows=list_a)
@app.route("/bar", methods=["POST", "GET"])
def bar():
   rows = []
   range1 = request.form.get('Country', '')
   # query1 = "SELECT Volcano_Name,Elev FROM volcano WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
   #     range1) + "' AND '" + str(range2) + "'"
   query = "select Volcano_Name,Elev from volcano where Country like '%"+range1+"%'"
   cursor.execute(query)
   r1 = cursor.fetchall()
   s1 = [item for t in r1 for item in t]
   s = len(s1)
   print(s1)
   print("\n",s)
   rows.append(["name","elevation"])
   i = 0
   while i < s:
       if i+1 < s:
           rows.append([s1[i],s1[i+1]])
           i=i+2
       else:
           break
   print("\n",len(rows))
   # rows = ([
   #     ['reg', 'pop'],
   #     [s1[0][0], s1[0][1]]
   #     ])
   print(rows)
   return render_template('bar.html', rows1=rows)
@app.route('/quiz7',methods=['GET','POST'])
def quiz7():
       lowElev = int(request.form.get('range1', ''))
       highElev = int(request.form.get('range2', ''))
       N = int(request.form.get('N', ''))
       data =[]
       data.append(['Elevation Range','No of Volcanos'])
       part = round((highElev - lowElev) / N)
       for i in range(N):
           query = "select count(*) from volcano where elev between "+str(lowElev)+" and "+str(lowElev+part)
           print(query)
           cursor.execute(query)
           rows = cursor.fetchall()
           print(rows)
           for row in rows:
               data.append([str(lowElev)+' - '+str(lowElev+part), row[0]])
           print(data)
           lowElev += part
       return render_template('showpie.html',rows=data)
'''

@app.route("/line", methods=["POST", "GET"])
def line():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM Quakes04 WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    return render_template('line.html', rows=rows)
'''

if __name__ == '__main__':
    app.run()
