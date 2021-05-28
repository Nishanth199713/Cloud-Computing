import pypyodbc
from flask import Flask, request, render_template
import json
from json import loads, dumps

app = Flask(__name__)

conn = pypyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        'SERVER=;'
                        'PORT=;'
                        'DATABASE=;'
                        'UID=;'
                        'PWD=')
# Enter Server, UID and PWD. Deleted for security purposes
cursor = conn.cursor()

#7
@app.route("/latrangeincrequakes", methods=["POST", "GET"])
def latrangeincrequakes():
    incrementvalue = float(request.form.get('incrementvalue', ''))
    net = request.form.get('net', '')
    latStart = float(request.form.get('latStart', ''))
    latEnd = float(request.form.get('latEnd', ''))
    rangeStart = latStart
    if latStart == 0:
        rangeEnd = incrementvalue
    else :
        rangeEnd = latStart+incrementvalue
    storeResult = []
    start = []
    end = []
    counter = 0
    while rangeStart < latEnd:
        #query = "Select count(*) from earthq where latitude between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
        query = "Select count(*) from earthq where mag between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"' and net='" +str(net)+"' "
        cursor.execute(query)
        resultSet = cursor.fetchall()
        countResult = resultSet[0][0]
        storeResult.append(countResult)
        start.append(rangeStart)
        end.append(rangeEnd)
        rangeStart = rangeEnd
        rangeEnd = rangeEnd + incrementvalue
        counter = counter + 1
    list_a = []
    list_a.append(['Magnitude Range','Number of Quakes'])
    for i in range(0,counter):
        list_a.append([str(start[i]) + '-' + str(end[i]),storeResult[i]])
    return render_template('latrangeincrequakes.html',start=start,end=end,storeResult=storeResult,rows=list_a)

#9
@app.route("/latrangeincrequakes3", methods=["POST", "GET"])
def latrangeincrequakes3():
    incrementvalue = float(request.form.get('incrementvalue', ''))
    net = request.form.get('net', '')
    latStart = float(request.form.get('latStart', ''))
    latEnd = float(request.form.get('latEnd', ''))
    rangeStart = latStart
    if latStart == 0:
        rangeEnd = incrementvalue
    else :
        rangeEnd = latStart+incrementvalue
    storeResult = []
    start = []
    end = []
    counter = 0
    while rangeStart < latEnd:
        #query = "Select count(*) from earthq where latitude between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
        query = "Select count(*) from earthq where mag between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"' and net='" +str(net)+"' "
        cursor.execute(query)
        resultSet = cursor.fetchall()
        countResult = resultSet[0][0]
        storeResult.append(countResult)
        start.append(rangeStart)
        end.append(rangeEnd)
        rangeStart = rangeEnd
        rangeEnd = rangeEnd + incrementvalue
        counter = counter + 1
    list_a = []
    list_a.append(['Magnitude Range','Number of Quakes'])
    for i in range(0,counter):
        list_a.append([str(start[i]) + '-' + str(end[i]),storeResult[i]])
    return render_template('quizpie.html',start=start,end=end,storeResult=storeResult,rows=list_a)

#8
@app.route("/latrangeincrequakes2", methods=["POST", "GET"])
def latrangeincrequakes2():
    incrementvalue = float(request.form.get('incrementvalue', ''))
    net = request.form.get('net', '')
    latStart = float(request.form.get('latStart', ''))
    latEnd = float(request.form.get('latEnd', ''))
    rangeStart = latStart
    if latStart == 0:
        rangeEnd = incrementvalue
    else :
        rangeEnd = latStart+incrementvalue
    storeResult = []
    start = []
    end = []
    counter = 0
    while rangeStart < latEnd:
        #query = "Select count(*) from earthq where latitude between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
        query = "Select count(*) from earthq where mag between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"' and net='" +str(net)+"' "
        cursor.execute(query)
        resultSet = cursor.fetchall()
        countResult = resultSet[0][0]
        storeResult.append(countResult)
        start.append(rangeStart)
        end.append(rangeEnd)
        rangeStart = rangeEnd
        rangeEnd = rangeEnd + incrementvalue
        counter = counter + 1
    list_a = []
    list_a.append(['Magnitude Range','Number of Quakes'])
    for i in range(0,counter):
        list_a.append([str(start[i]) + '-' + str(end[i]),storeResult[i]])
    return render_template('quizbar.html',start=start,end=end,storeResult=storeResult,rows=list_a)

@app.route('/')
def home():
    return render_template('home.html')


#10
@app.route("/practise3", methods=["POST", "GET"])
def practise3():
    rangeStart = int(request.form.get('latStart', ''))
    rangeEnd = int(request.form.get('latEnd', ''))
    net = str(request.form.get('net',''))
    query = "Select nst, gap from earthq where net = '"+str(net)+"' and nst between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
    cursor.execute(query)
    result = cursor.fetchall()
    maxQuery = "Select count(*) from earthq where net = '"+str(net)+"' and nst between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
    cursor.execute(maxQuery)
    countResult = cursor.fetchall()
    count = countResult[0][0]
    list_a = []
    list_a.append(['nst','gap'])
    for i in range(0, int(count)):
        list_a.append([result[i][0], result[i][1]])
    # rows = []
    # rows = [result[0][0], result[0][1],
    #         result[1][0], result[1][1],
    #         result[2][0], result[2][1],
    #         result[3][0], result[3][1],
    #         result[4][0], result[4][1],
    #         result[5][0], result[5][1],
    #         result[6][0], result[6][1],
    #         result[7][0], result[7][1],
    #         result[8][0], result[8][1],
    #         result[9][0], result[9][1],
    #         result[10][0], result[10][1],
    #         result[11][0], result[11][1],
    #         result[12][0], result[12][1]]
    return render_template('practise3.html', rows=list_a, count=count)

# @app.route("/showpie", methods=["POST", "GET"])
# def showpie():
#     category = str(request.form.get('category', ''))
#     query1 = "SELECT * FROM groc WHERE category = '" + str(category) + "'"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()
#     return render_template('showpie.html',category=category,rows=r1)

#user enter category veg or nonveg and display all results of that category - pie chart
#quiz 0a
@app.route("/showpiechart", methods=["POST", "GET"])
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
    #query1 = "select StateName from voting where totalpop between 2000 and 8000"
    query1 = "select * from earthq where mag between 1 and 3"    
    cursor.execute(query1)
    r1 = cursor.fetchall()

    #query2 = "select StateName from voting where totalpop between 8000 and 40000"
    query2 = "select * from earthq where mag between 3 and 7"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    return render_template('basic.html', rows1=r1, rows2=r2)

#6
@app.route('/regscatter', methods=['POST', 'GET'])
def regscatter():
    m1 = int(request.form.get('m1', ''))
    m2 = int(request.form.get('m2', ''))


    query1 = "SELECT count(*) FROM earthq WHERE mag BETWEEN '"+str(m1)+"' AND '"+str(m2)+"'"
    cursor.execute(query1)
    s1 = cursor.fetchall()


    rows = ([
        ['Magnitude range', 'Number of quakes'],
        [str(m1)+'-'+str(m2), s1[0][0]]
        ])
    return render_template('regscatter.html', rows1=rows)

#7
@app.route("/quiz7", methods=["POST", "GET"])
def quiz7():
    range1 = int(request.form.get('range',''))
    rangeStart = 0
    rangeEnd = range1
    maxQuery = "Select max(mag) from earthq"
    cursor.execute(maxQuery)
    maxResult = cursor.fetchall()
    maxPopulation = maxResult[0][0]
    storeResult = []
    start = []
    end = []
    counter = 0
    while rangeStart < maxPopulation:
        query = "Select count(*) from earthq where mag between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
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
    list_a.append(['Magnitude Range','Number of quakes'])
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
    for i in range(1,range1):
        modulo = (i**3)%10
        r1.append(modulo)
    
    r2=[]
    
    for i in range(range1-1):
        count=r1.count(r1[i])
        r2.append(count)
    
    rows = []
    rows.append(['Range Value', 'Number of Times'])
    
    for i in range(range1-1):
        rows.append([r1[i],r2[i]])
    
    return render_template('bar.html', rows=rows)

@app.route("/list", methods=["POST", "GET"])
def list():
    # depthrange1 = float(request.form.get('depthrange1', ''))
    # query1="SELECT * FROM earthq WHERE latitude >= '" + str(latitude1) + "' AND latitude <= '" + str(latitude2) + "' AND longitude >= '" + str(longitude1) + "' AND longitude <= '" + str(longitude2) + "'"
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
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

    query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of quakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]

    ])

    return render_template('showpie.html', rows=rows)


@app.route("/pie", methods=["POST", "GET"])
def pie():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows1 = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    query8 = "select count(*) from earthq where mag > 5.0 and deptherror > 5"
    cursor.execute(query8)
    r8 = cursor.fetchall()
    query9 = "select count(*) from earthq where mag > 5.0 and deptherror < 5"
    cursor.execute(query9)
    r9 = cursor.fetchall()

    rows2 = ([
        ['Magnitude and Depth Error', 'Number of Earthquakes'],
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

    query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    return render_template('bar.html', rows=rows)

@app.route("/scatter", methods=["POST", "GET"])
def scatter():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    return render_template('scatter.html', rows=rows)


@app.route("/line", methods=["POST", "GET"])
def line():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
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


if __name__ == '__main__':
    app.run()
