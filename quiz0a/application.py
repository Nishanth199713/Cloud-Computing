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


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/disp", methods=["POST", "GET"])
def disp():
	m1 = int(request.form.get('num', ''))
	m2 = m1+69

	return render_template('disp.html', row = m2, col = m1)

@app.route("/category", methods=["POST", "GET"])
def category():
	category = str(request.form.get('category', ''))
	query1 = "SELECT item,quantity FROM grocery WHERE category = '" + str(category) + "'"
	cursor.execute(query1)
	r1 = cursor.fetchall()

	return render_template('category.html', rows1=r1, category=category)

@app.route("/showpie", methods=["POST", "GET"])
def showpie():
	query1 = "SELECT count(*) FROM grocery WHERE category = 'veg'"
	cursor.execute(query1)
	r1 = cursor.fetchall()

	query2 = "SELECT count(*) FROM grocery WHERE category = 'notveg'"
	cursor.execute(query2)
	r2 = cursor.fetchall()

	rows = ([
		['Category', 'Count'],
		['Veg', r1[0][0]],
		['NonVeg', r2[0][0]]
		])

	return render_template('showpie.html', rows=rows)

# #5
# @app.route("/basic", methods=["POST", "GET"])
# def basic():
#     query1 = "select StateName from voting where totalpop between 2000 and 8000"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()

#     query2 = "select StateName from voting where totalpop between 8000 and 40000"
#     cursor.execute(query2)
#     r2 = cursor.fetchall()

#     return render_template('basic.html', rows1=r1, rows2=r2)

# #6
# @app.route('/regscatter', methods=['POST', 'GET'])
# def regscatter():
#     m1 = int(request.form.get('m1', ''))
#     m2 = int(request.form.get('m2', ''))
#     m1 = m1 * 1000
#     m2 = m2 * 1000


#     query1 = "SELECT sum(Registered) FROM voting WHERE TotalPop BETWEEN '"+str(m1)+"' AND '"+str(m2)+"'"
#     cursor.execute(query1)
#     s1 = cursor.fetchall()


#     rows = ([['reg', 'pop'],[str(m1)+'-'+str(m2), s1[0][0]]])
#     return render_template('regscatter.html', rows1=rows)

# #7
# @app.route("/quizpie", methods=["POST", "GET"])
# def quizpie():

#     range1 = 0
#     range2 = int(request.form.get('range2', ''))

#     query1 = "SELECT max(totalpop) FROM voting"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()

#     totrange = 0
#     count = 0
#     range11 = []
#     range22 = []


#     for i in range(range2):
#         if (totrange <= r1[0][0]):
#             totrange += range2
#         if totrange> r1[0][0]:
#             break

#         query2 = "SELECT count(*) FROM voting WHERE TotalPop between '" + str(range1) + "' AND '" + str(range2) + "'"
#         cursor.execute(query2)
#         r2 = cursor.fetchall()
#         range1 = range2
#         range2 = range2 + totrange
#         count = count + 1
#         range11.append(range1)

#     range11.append(range2)



#     rows = ([
#         ['State', 'Number of population'],
#         [str(range11[0][0]) + '-' + str(range1[0][1]), r2[0][0]],
#         [str(range11[0][2]) + '-' + str(range1[0][3]), r2[0][0]],
#         [str(range11[0][4]) + '-' + str(range1[0][5]), r2[0][0]],
#         [str(range11[0][6]) + '-' + str(range1[0][7]), r2[0][0]],
#         [str(range11[0][8]) + '-' + str(range1[0][9]), r2[0][0]]

#     ])

#     return render_template('quizpie.html', rows=rows)

# @app.route("/list", methods=["POST", "GET"])
# def list():
#     # depthrange1 = float(request.form.get('depthrange1', ''))
#     # query1="SELECT * FROM earthq WHERE latitude >= '" + str(latitude1) + "' AND latitude <= '" + str(latitude2) + "' AND longitude >= '" + str(longitude1) + "' AND longitude <= '" + str(longitude2) + "'"
#     locationSource = str(request.form.get('locationSource', ''))
#     range1 = float(request.form.get('range1', ''))
#     range2 = float(request.form.get('range2', ''))
#     range3 = float(request.form.get('range3', ''))
#     range4 = float(request.form.get('range4', ''))
#     range5 = float(request.form.get('range5', ''))
#     range6 = float(request.form.get('range6', ''))

#     query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()

#     query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range3) + "' AND '" + str(range4) + "'"
#     cursor.execute(query2)
#     r2 = cursor.fetchall()

#     query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range5) + "' AND '" + str(range6) + "'"
#     cursor.execute(query3)
#     r3 = cursor.fetchall()
#     return render_template('list.html', rows1=r1, rows2=r2, rows3=r3)


# @app.route("/showpie", methods=["POST", "GET"])
# def showpie():
#     locationSource = str(request.form.get('locationSource', ''))
#     range1 = float(request.form.get('range1', ''))
#     range2 = float(request.form.get('range2', ''))
#     range3 = float(request.form.get('range3', ''))
#     range4 = float(request.form.get('range4', ''))
#     range5 = float(request.form.get('range5', ''))
#     range6 = float(request.form.get('range6', ''))

#     query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()

#     query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range3) + "' AND '" + str(range4) + "'"
#     cursor.execute(query2)
#     r2 = cursor.fetchall()

#     query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range5) + "' AND '" + str(range6) + "'"
#     cursor.execute(query3)
#     r3 = cursor.fetchall()

#     rows = ([
#         ['Magnitude', 'Number of quakes'],
#         [str(range1) + '-' + str(range2), r1[0][0]],
#         [str(range3) + '-' + str(range4), r2[0][0]],
#         [str(range5) + '-' + str(range6), r3[0][0]]

#     ])

#     return render_template('showpie.html', rows=rows)


# @app.route("/pie", methods=["POST", "GET"])
# def pie():
#     locationSource = str(request.form.get('locationSource', ''))
#     range1 = float(request.form.get('range1', ''))
#     range2 = float(request.form.get('range2', ''))
#     range3 = float(request.form.get('range3', ''))
#     range4 = float(request.form.get('range4', ''))
#     range5 = float(request.form.get('range5', ''))
#     range6 = float(request.form.get('range6', ''))

#     query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range1) + "' AND '" + str(range2) + "'"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()

#     query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range3) + "' AND '" + str(range4) + "'"
#     cursor.execute(query2)
#     r2 = cursor.fetchall()

#     query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range5) + "' AND '" + str(range6) + "'"
#     cursor.execute(query3)
#     r3 = cursor.fetchall()

#     rows1 = ([
#         ['Magnitude', 'Number of Earthquakes'],
#         [str(range1) + '-' + str(range2), r1[0][0]],
#         [str(range3) + '-' + str(range4), r2[0][0]],
#         [str(range5) + '-' + str(range6), r3[0][0]]
#     ])

#     query8 = "select count(*) from earthq where mag > 5.0 and deptherror > 5"
#     cursor.execute(query8)
#     r8 = cursor.fetchall()
#     query9 = "select count(*) from earthq where mag > 5.0 and deptherror < 5"
#     cursor.execute(query9)
#     r9 = cursor.fetchall()

#     rows2 = ([
#         ['Magnitude and Depth Error', 'Number of Earthquakes'],
#         ['Depth Error > 5', r8[0][0]],
#         ['Depth Error < 5', r9[0][0]]

#     ])

#     return render_template('pie.html', rows=[rows1, rows2])


# @app.route("/bar", methods=["POST", "GET"])
# def bar():
#     locationSource = str(request.form.get('locationSource', ''))
#     range1 = float(request.form.get('range1', ''))
#     range2 = float(request.form.get('range2', ''))
#     range3 = float(request.form.get('range3', ''))
#     range4 = float(request.form.get('range4', ''))
#     range5 = float(request.form.get('range5', ''))
#     range6 = float(request.form.get('range6', ''))

#     query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range1) + "' AND '" + str(range2) + "'"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()

#     query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range3) + "' AND '" + str(range4) + "'"
#     cursor.execute(query2)
#     r2 = cursor.fetchall()

#     query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range5) + "' AND '" + str(range6) + "'"
#     cursor.execute(query3)
#     r3 = cursor.fetchall()

#     rows = ([
#         ['Magnitude', 'Number of Earthquakes'],
#         [str(range1) + '-' + str(range2), r1[0][0]],
#         [str(range3) + '-' + str(range4), r2[0][0]],
#         [str(range5) + '-' + str(range6), r3[0][0]]
#     ])

#     return render_template('bar.html', rows=rows)

# @app.route("/scatter", methods=["POST", "GET"])
# def scatter():
#     locationSource = str(request.form.get('locationSource', ''))
#     range1 = float(request.form.get('range1', ''))
#     range2 = float(request.form.get('range2', ''))
#     range3 = float(request.form.get('range3', ''))
#     range4 = float(request.form.get('range4', ''))
#     range5 = float(request.form.get('range5', ''))
#     range6 = float(request.form.get('range6', ''))

#     query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range1) + "' AND '" + str(range2) + "'"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()

#     query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range3) + "' AND '" + str(range4) + "'"
#     cursor.execute(query2)
#     r2 = cursor.fetchall()

#     query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range5) + "' AND '" + str(range6) + "'"
#     cursor.execute(query3)
#     r3 = cursor.fetchall()

#     rows = ([
#         ['Magnitude', 'Number of Earthquakes'],
#         [str(range1) + '-' + str(range2), r1[0][0]],
#         [str(range3) + '-' + str(range4), r2[0][0]],
#         [str(range5) + '-' + str(range6), r3[0][0]]
#     ])

#     return render_template('scatter.html', rows=rows)


# @app.route("/line", methods=["POST", "GET"])
# def line():
#     locationSource = str(request.form.get('locationSource', ''))
#     range1 = float(request.form.get('range1', ''))
#     range2 = float(request.form.get('range2', ''))
#     range3 = float(request.form.get('range3', ''))
#     range4 = float(request.form.get('range4', ''))
#     range5 = float(request.form.get('range5', ''))
#     range6 = float(request.form.get('range6', ''))

#     query1 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range1) + "' AND '" + str(range2) + "'"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()

#     query2 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range3) + "' AND '" + str(range4) + "'"
#     cursor.execute(query2)
#     r2 = cursor.fetchall()

#     query3 = "SELECT count(*) FROM earthq WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
#         range5) + "' AND '" + str(range6) + "'"
#     cursor.execute(query3)
#     r3 = cursor.fetchall()

#     rows = ([
#         ['Magnitude', 'Number of Earthquakes'],
#         [str(range1) + '-' + str(range2), r1[0][0]],
#         [str(range3) + '-' + str(range4), r2[0][0]],
#         [str(range5) + '-' + str(range6), r3[0][0]]
#     ])

#     return render_template('line.html', rows=rows)


if __name__ == '__main__':
    app.run()
