import os
from flask import Flask, redirect, render_template, request
import json
import ibm_db
from math import radians, cos, sin, asin, sqrt, atan2
import math

# from flask_db2 import DB2

app = Flask(__name__, static_url_path='')

conn = ibm_db.connect("DATABASE=;HOSTNAME=;PORT=;PROTOCOL=;UID=;PWD=;", "", "")
print("Connected to db")    # Enter the host name userid and password---deleted for security purposes
# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
	db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
	db2cred = db2info["credentials"]

else:
	raise ValueError('Expected cloud environment')

@app.route("/", methods=["POST", "GET"])
def getdata():
	listofdata = []
	query1 = "SELECT * FROM EARTHQ LIMIT 5"
	stmt = ibm_db.exec_immediate(conn, query1)
	result = ibm_db.fetch_both(stmt)
	while result:
		listofdata.append(result)
		result = ibm_db.fetch_both(stmt)

	return render_template('main.html', table=listofdata)


@app.route("/countrycode", methods=["POST", "GET"])
def countrycode():
	countrycode = request.form.get("countrycode")
	listofdata = []

	query2 = "SELECT LATITUDE,LONGITUDE,NAME FROM LATLONG WHERE COUNTRY = '"+str(countrycode)+"'"
	stmt2 = ibm_db.exec_immediate(conn, query2)
	result2 = ibm_db.fetch_both(stmt2)
	while result2:
		listofdata.append(result2)
		result2 = ibm_db.fetch_both(stmt2)

	return render_template('countrycode.html', table=listofdata, title='Countrycode')

@app.route('/box', methods=['POST'])
def box():
    latitude1 = request.form['latitude1']
    longitude1 = request.form['longitude1']
    latitude2 = request.form['latitude2']
    longitude2 = request.form['longitude2']
    listofdata = []
    query1 = "SELECT COUNTRY, NAME from LATLONG where LATITUDE BETWEEN '"+ latitude1 + "' AND  '"+ latitude2 + "' AND LONGITUDE BETWEEN '"+ longitude1 +"' AND '"+ longitude2 + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
    	listofdata.append(result)
    	result = ibm_db.fetch_both(stmt1)

    return render_template('box.html',table=listofdata, rowcount=len(listofdata))

@app.route('/boundingbox', methods=['POST'])
def boundingbox():
    latitude3 = request.form['latitude1']
    longitude3 = request.form['longitude1']
    latitude2 = request.form['latitude2']
    longitude2 = request.form['longitude2']
    magnitude = request.form['magnitude']
    latitude1 = float(latitude3)+float(latitude2)
    longitude1 = float(longitude3)+float(longitude2)
    listofdata = []
    query1 = "SELECT * from EARTHQ where LATITUDE BETWEEN '"+ str(latitude1) + "' AND  '"+ latitude2 + "' AND LONGITUDE BETWEEN '"+ str(longitude1) +"' AND '"+ longitude2 + "' AND MAG >= '"+ magnitude +"'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
    	listofdata.append(result)
    	result = ibm_db.fetch_both(stmt1)

    return render_template('boundingbox.html',table= listofdata, rowcount=len(listofdata), newlat=latitude1, newlong =longitude1)

@app.route("/nstmagrange", methods=["POST", "GET"])
def nstmagrange():
    type = "earthquake"
    latitude1 = request.form['latitude1']
    longitude1 = request.form['longitude1']
    latitude2 = request.form['latitude2']
    longitude2 = request.form['longitude2']
    magStart = float(request.form['magStart'])
    magEnd = float(request.form['magEnd'])
    nstrange1  = request.form['nstrange1']
    nstrange2  = request.form['nstrange2']
    start = magStart
    counts = []
    starts = []
    ends = []
    end = start + 1
    while end <= magEnd:
        end = start + 1
        selectQuery = "SELECT * from EARTHQ where LATITUDE BETWEEN '"+ latitude1 + "' AND  '"+ latitude2 + "' AND LONGITUDE BETWEEN '"+ longitude1 +"' AND '"+ longitude2 + "' and MAG >= '"+ str(start) +"' AND MAG <= '" + str(end)+"' AND NST BETWEEN '"+ nstrange1 +"' AND '"+ nstrange2 + "'"
        selectStmt = ibm_db.exec_immediate(conn, selectQuery)
        rows = []
        count = 0
        result = ibm_db.fetch_assoc(selectStmt)
        starts.append(start)
        ends.append(end)
        while result != False:
            count = count + 1
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(selectStmt)
        counts.append(count)
        start = end
    length = len(starts)
    return render_template('nstmagrange.html', starts=starts,ends=ends,counts=counts,length=length)

# @app.route('/boundingbox', methods=['POST'])
# def boundingbox():
#     latitude1 = request.form['latitude1']
#     longitude1 = request.form['longitude1']
#     latitude2 = request.form['latitude2']
#     longitude2 = request.form['longitude2']
#     magnitude = request.form['magnitude']
#     query = 'select * from EARTHQ where "LATITUDE" >= \'' + latitude2 + '\' and "LATITUDE" <= \'' + latitude1 + '\' and "LONGITUDE" >= \'' + longitude1 + '\' and "LONGITUDE" <= \'' + longitude2 + '\' and "MAG" >= \'' + magnitude + '\''
#     stmt = ibm_db.exec_immediate(conn, query)
#     rows = []
#     count = 0
#     radius = 6373.0
#     result = ibm_db.fetch_assoc(stmt)
#     while result != False:
#         rows.append(result.copy())
#         result = ibm_db.fetch_assoc(stmt)
#     return render_template('boundingbox.html',rows=rows)


@app.route("/magsmallgreat", methods=["POST", "GET"])
def magsmallgreat():
	magnitude = request.form.get("magnitude")
	listofdata = []
	query1 = "SELECT COUNT(*) FROM EARTHQ"
	stmt1 = ibm_db.exec_immediate(conn, query1)
	result1 = ibm_db.fetch_both(stmt1)
	
	query2 = "SELECT MAG, PLACE FROM EARTHQ WHERE MAG = (SELECT MAG FROM  EARTHQ WHERE MAG >'"+str(magnitude)+"' ORDER BY MAG LIMIT 1)"
	stmt2 = ibm_db.exec_immediate(conn, query2)
	result2 = ibm_db.fetch_both(stmt2)
	while result2:
		listofdata.append(result2)
		result2 = ibm_db.fetch_both(stmt2)

	return render_template('magsmallgreat.html', table=listofdata, rowcount=result1[0], title='Magsmallgreat')

# @app.route("/depthrangeincrement", methods=["POST", "GET"])
# def depthrangeincrement():
#     range1 = request.form.get("depthrange1")
#     range2 = request.form.get("depthrange2")
#     increment = request.form.get("increment")
#     range_data = []
#     query2 = "CREATE OR REPLACE VIEW DEPTHDATA AS SELECT DEPTH, CASE WHEN DEPTH >= 2 AND  DEPTH<=4 THEN 'THE DEPTH IS FROM 2 TO 4' WHEN DEPTH >4 AND DEPTH<=6 THEN 'THE DEPTH  MORE THAN 4 TILL 6' WHEN DEPTH >6 AND DEPTH<=8 THEN 'THE DEPTH MORE THAN 6 TILL 8' WHEN DEPTH >8 AND DEPTH<=10 THEN 'THE DEPTH MORE THAN 8 TILL 10' ELSE 'THE DEPTH IS MORE THAN 10' END AS DEPTHCATEGORY FROM EARTHQ"
#     stmt2 = ibm_db.exec_immediate(conn, query2)
#     query1 = "SELECT COUNT(DEPTH) AS NOOFQUAKES,DEPTHCATEGORY FROM DEPTHDATA GROUP BY DEPTHCATEGORY ORDER BY DEPTHCATEGORY"
#     stmt1 = ibm_db.exec_immediate(conn, query1)
#     result = ibm_db.fetch_both(stmt1)
#     while result:
#     	range_data.append(result)
#     	result = ibm_db.fetch_both(stmt1)

#     return render_template('depthrangeincrement.html', table=range_data, title='Depth Range With Increment')

@app.route('/depthrangeincrement', methods=['POST'])
def depthrangeincrement():
    type = "earthquake"
    magStart = float(request.form['depthrange1'])
    magEnd = float(request.form['depthrange2'])
    net  = float(request.form['increment'])
    start = magStart
    counts = []
    starts = []
    ends = []
    end = start + net
    while end <= magEnd:
        query1 = "SELECT * from EARTHQ where DEPTH BETWEEN '"+str(start)+ "' AND  '"+str(end)+ "'"
        stmt1 = ibm_db.exec_immediate(conn, query1)
        result = ibm_db.fetch_both(stmt1)
        rows = []
        count = 0
        starts.append(start)
        ends.append(end)
        while result != False:
            count = count + 1
            rows.append(result.copy())
            result = ibm_db.fetch_both(stmt1)
        counts.append(count)
        start = end
        end = start + net
    length = len(starts)
    return render_template('depthrangeincrement.html', starts=starts,ends=ends,counts=counts,length=length)

# @app.route("/magrangeincrement", methods=["POST", "GET"])
# def magrangeincrement():
#     range1 = request.form.get("magrange1")
#     range2 = request.form.get("magrange2")
#     increment = request.form.get("increment")
#     netvalue = request.form.get("nett")
#     range_data = []
#     query2 = "CREATE OR REPLACE VIEW MAGDATA AS SELECT MAG, CASE WHEN MAG >= 2 AND  MAG<=4 THEN 'THE MAG IS FROM 2 TO 4' WHEN MAG >4 AND MAG<=6 THEN 'THE MAG  MORE THAN 4 TILL 6' WHEN MAG >6 AND MAG<=8 THEN 'THE MAG MORE THAN 6 TILL 8' WHEN MAG >8 AND MAG<=10 THEN 'THE MAG MORE THAN 8 TILL 10' ELSE 'THE MAG IS MORE THAN 10' END AS MAGCATEGORY FROM EARTHQ WHERE NET= '" + str(netvalue) + "'"
#     stmt2 = ibm_db.exec_immediate(conn, query2)
#     query1 = "SELECT COUNT(MAG) AS NOOFQUAKES,MAGCATEGORY FROM MAGDATA GROUP BY MAGCATEGORY ORDER BY MAGCATEGORY"
#     stmt1 = ibm_db.exec_immediate(conn, query1)
#     result = ibm_db.fetch_both(stmt1)
#     while result:
#     	range_data.append(result)
#     	result = ibm_db.fetch_both(stmt1)

#     return render_template('magrangeincrement.html', table=range_data,netval=netvalue,title='Magnitude Range With Increment')

@app.route('/magrangeincrement', methods=['POST'])
def magrangeincrement():
    type = "earthquake"
    magStart = float(request.form['magrange1'])
    magEnd = float(request.form['magrange2'])
    net  = float(request.form['increment'])
    netvalue = request.form.get("netvalue")
    start = magStart
    counts = []
    starts = []
    ends = []
    end = start + net
    while end <= magEnd:
        query1 = "SELECT * from EARTHQ where MAG BETWEEN '"+str(start)+ "' AND  '"+str(end)+ "' AND NET='"+str(netvalue)+"'"
        stmt1 = ibm_db.exec_immediate(conn, query1)
        result = ibm_db.fetch_both(stmt1)
        rows = []
        count = 0
        starts.append(start)
        ends.append(end)
        while result != False:
            count = count + 1
            rows.append(result.copy())
            result = ibm_db.fetch_both(stmt1)
        counts.append(count)
        start = end
        end = start + net
    length = len(starts)
    return render_template('magrangeincrement.html', starts=starts,ends=ends,counts=counts,length=length)


@app.route("/update", methods=["POST", "GET"])
def update():
    depthrange1 = request.form.get("depthrange1")
    depthrange2 = request.form.get("depthrange2")
    startdate = request.form.get("startdate")
    enddate = request.form.get("enddate")
    magnitude = request.form.get("mag")
    update_data = []
    query1 = "UPDATE EARTHQ SET MAG = 999 WHERE DEPTH BETWEEN '" + str(depthrange1) + "' AND '" + str(depthrange2) + "' AND GMTTIME BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    query2 = "SELECT COUNT(*) FROM EARTHQ  WHERE MAG=999 AND DEPTH BETWEEN '" + str(depthrange1) + "' AND '" + str(depthrange2) + "' AND GMTTIME BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result2 = ibm_db.fetch_both(stmt2)
    # while result2:
        # update_data.append(result2)
        # result2 = ibm_db.fetch_both(stmt2)

    return render_template('update.html', table=update_data, rowcount=result2[0], title='Update Data')


@app.route("/greaterthan", methods=["POST", "GET"])
def greaterthan():
	range1 = request.form.get("range1")
	
	greater_data = []
	query1 = "SELECT * FROM EARTHQ WHERE MAG > '" + str(range1) + "'"
	stmt1 = ibm_db.exec_immediate(conn, query1)
	result = ibm_db.fetch_both(stmt1)
	while result:
		greater_data.append(result)
		result = ibm_db.fetch_both(stmt1)

	return render_template('greaterthan.html', table=greater_data, rowcount=len(greater_data), title='Greater Than')


@app.route("/withinrange", methods=["POST", "GET"])
def withinrange():
	range1 = request.form.get("magrange1")
	range2 = request.form.get("magrange2")
	startdate = request.form.get("startdate")
	enddate = request.form.get("enddate")
	
	range_data = []
	query1 = "SELECT * FROM EARTHQ WHERE MAG BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND GMTTIME BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
	stmt1 = ibm_db.exec_immediate(conn, query1)
	result = ibm_db.fetch_both(stmt1)
	while result:
		range_data.append(result)
		result = ibm_db.fetch_both(stmt1)

	return render_template('withinrange.html', table=range_data, rowcount=len(range_data), title='Within Range')


@app.route("/locationdist", methods=["POST", "GET"])
def locationdist():
	location=request.form['location']
	distance=request.form['distance']
	distance=distance+"km"
	locationdist_data = []
	query1="select * from EARTHQ where PLACE like '%"+location+"%' and PLACE like '"+distance+"%'"
	stmt1 = ibm_db.exec_immediate(conn, query1)
	result = ibm_db.fetch_both(stmt1)
	while result:
		locationdist_data.append(result)
		result = ibm_db.fetch_both(stmt1)

	return render_template('locationdist.html', table=locationdist_data, rowcount=len(locationdist_data), title='Location Distance')

# @app.route('/locationdist', methods=['POST'])
# def locationdist():
#     lat = request.form['lat']
#     long = request.form['long']
#     dist = request.form['dist']
#     selectQuery = 'select * from EARTHQ'
#     selectStmt = ibm_db.exec_immediate(conn, selectQuery)
#     rows = []
#     count = 0
#     radius = 6373.0
#     result = ibm_db.fetch_assoc(selectStmt)
#     while result != False:
#         rows.append(result.copy())
#         result = ibm_db.fetch_assoc(selectStmt)

#     for row in rows:
#         lat1 = math.radians(float(lat))
#         lon1 = math.radians(float(long))
#         lat2 = math.radians(float(row['LATITUDE']))
#         lon2 = math.radians(float(row['LONGITUDE']))

#         dlat = lat2 - lat1
#         dlon = lon2 - lon1
    
#         a = math.sin(dlat / 2)*2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)*2
#         c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#         #print(type(a),a)
#         #print(type(c),c)
#         d = radius * c
#         if(d < float(dist)):
#             count = count + 1
#     return render_template('locationdist.html', count = count,dist=dist)

@app.route('/searchinradius',methods=['GET','POST'])
def searchinradius(latitude=None,longitude=None,radius=None):
	longitude = float(request.form['longitude'])
	latitude = float(request.form['latitude'])
	radius = float(request.form['radius'])
	lat1 = latitude - (radius / 69)
	lat2 = latitude + (radius / 69)
	long1 = longitude - (radius / 69)
	long2 = longitude + (radius / 69)
	query1="SELECT * from EARTHQ where LATITUDE BETWEEN '"+str(lat1)+"' AND '"+str(lat2)+"' AND LONGITUDE BETWEEN '"+str(long1)+"' and '"+str(long2)+"' "
	listofdata=[]
	stmt1 = ibm_db.exec_immediate(conn, query1)
	result = ibm_db.fetch_both(stmt1)
	while result:
		listofdata.append(result)
		result = ibm_db.fetch_both(stmt1)
	return render_template('searchinradius.html', table=listofdata, rowcount=len(lis))


@app.route("/locationmag", methods=["POST", "GET"])
def locationmag():
	range1 = request.form.get("magrange1")
	range2 = request.form.get("magrange2")
	location = request.form.get("location")

	range_data = []
	query1 = "SELECT * FROM EARTHQ WHERE MAG BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND PLACE like '%"+location+"%'"
	stmt1 = ibm_db.exec_immediate(conn, query1)
	result = ibm_db.fetch_both(stmt1)
	while result:
		range_data.append(result)
		result = ibm_db.fetch_both(stmt1)

	return render_template('locationdist.html', table=range_data, rowcount=len(range_data), title='Location magnitude')


@app.route("/nightquake", methods=["POST", "GET"])
def nightquake():
	magnitude = request.form.get("magnitude")
	dayquery1= "SELECT COUNT(*) FROM EARTHQ WHERE MAG > '" + str(magnitude) + "' AND (GMTTIME NOT LIKE '%T18%' AND GMTTIME NOT LIKE '%T19%' AND GMTTIME NOT LIKE '%T20%' AND GMTTIME NOT LIKE '%T21%' AND GMTTIME NOT LIKE '%T22%' AND GMTTIME NOT LIKE '%T23%' AND GMTTIME NOT LIKE '%T24%' AND GMTTIME NOT LIKE '%T01%' AND GMTTIME NOT LIKE '%T02%' AND GMTTIME NOT LIKE '%T03%' AND GMTTIME NOT LIKE '%T04%' AND GMTTIME NOT LIKE '%T05%' AND GMTTIME NOT LIKE '%T06%')"
	daystmt1 = ibm_db.exec_immediate(conn, dayquery1)
	dayresult1 = ibm_db.fetch_both(daystmt1)
	nightquery2= "SELECT COUNT(*) FROM EARTHQ WHERE MAG > '" + str(magnitude) + "' AND (GMTTIME LIKE '%T18%' OR GMTTIME LIKE '%T19%' OR GMTTIME LIKE '%T20%' OR GMTTIME LIKE '%T21%' OR GMTTIME LIKE '%T22%' OR GMTTIME LIKE '%T23%' OR GMTTIME LIKE '%T24%' OR GMTTIME LIKE '%T01%' OR GMTTIME LIKE '%T02%' OR GMTTIME LIKE '%T03%' OR GMTTIME LIKE '%T04%' OR GMTTIME LIKE '%T05%' OR GMTTIME LIKE '%T06%')"
	nightstmt2 = ibm_db.exec_immediate(conn, nightquery2)
	nightresult2 = ibm_db.fetch_both(nightstmt2)
	if dayresult1[0] > nightresult2[0]:
		return render_template('nightquakes.html', title='Magnitude During Day is More', daycount='day is more',dayresult=dayresult1[0],nightresult=nightresult2[0])
	elif dayresult1[0] == nightresult2[0]:
		return render_template('nightquakes.html', title='Magnitude During Day & Night are Equal',daycount='Day & Night are Equal',dayresult=dayresult1[0],nightresult=nightresult2[0])
	else:
		return render_template('nightquakes.html', title='Magnitude During Night is More',daycount='night more',dayresult=dayresult1[0],nightresult=nightresult2[0])



@app.route("/totandmaxmag", methods=["POST", "GET"])
def totandmaxmag():
	depthrange1 = request.form.get("depthrange1")
	depthrange2 = request.form.get("depthrange2")
	netvalue = request.form.get("net")
	totmagdata = []
	totquery= "SELECT COUNT(*),MAX(MAG) FROM EARTHQ WHERE DEPTH BETWEEN '" + str(depthrange1) + "' AND '" + str(depthrange2) + "' AND NET = '" + str(netvalue) + "'"
	totstmt = ibm_db.exec_immediate(conn, totquery)
	totresult = ibm_db.fetch_both(totstmt)
	# maxmagquery= "SELECT MAX(MAG) FROM EARTHQ WHERE DEPTH BETWEEN '" + str(depthrange1) + "' AND '" + str(depthrange2) + "' AND NET = '" + str(netvalue) + "' AND MAG >0 and MAG <10"
	# maxmagstmt = ibm_db.exec_immediate(conn, maxmagquery)
	# maxmagresult = ibm_db.fetch_both(maxmagstmt)
	while totresult:
		totmagdata.append(totresult)
		totresult = ibm_db.fetch_both(totstmt)

	return render_template('totandmaxmag.html', table=totmagdata,netval=netvalue,title='For Given Net, Total Quakes and Max Magnitude')

def haversine(lon1, lat1, lon2, lat2):
	# """
	# Calculate the great circle distance between two points 
	# on the earth (specified in decimal degrees)
	# """
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	r = 6371 # Radius of earth in kilometers. Use 3956 for miles
	return c * r


@app.route("/morequakes", methods=["POST", "GET"])
def morequakes():
	latdeg1 = request.form.get("lat1")
	londeg1 = request.form.get("lon1")
	latdeg2 = request.form.get("lat2")
	londeg2 = request.form.get("lon2")
	magnitude = request.form.get("mag")
	
	quake_data = []
	# diff_min = lon1 * 4
	# local = float(gmttime) + float(diff_min)

	lat1 = math.radians(latdeg1)
	lon1 = math.radians(londeg1)
	lat2 = math.radians(latdeg2)
	lon2 = math.radians(londeg2)

	latlon = haversine(lon1, lat1, lon2, lat2)
	query1 = "SELECT PLACE,LATITUDE,LONGITUDE FROM EARTHQ WHERE MAG >= '" + str(magnitude) + "' AND LATITUDE = '" + str(lat1) + "' AND LONGITUDE = '" + str(lon1) + "'"

	stmt1 = ibm_db.exec_immediate(conn, query1)
	result = ibm_db.fetch_both(stmt1)
	while result:
		quake_data.append(result)
		result = ibm_db.fetch_both(stmt1)

	return render_template('morequakes.html', table=quake_data, rowcount=len(quake_data), title='More Earthquakes')




port = os.getenv('PORT', '5000')

if __name__ == '__main__':
	# app.run(host='127.0.0.1', port=int(port))
	app.run(host='0.0.0.0', port=int(port))
