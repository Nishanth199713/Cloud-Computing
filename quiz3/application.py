import pypyodbc
from flask import Flask, request, render_template
from random import randint
import random
import time
import redis
import hashlib
import pickle
from datetime import datetime
from json import loads, dumps

app = Flask(__name__)

cache = 'c1'

r = redis.StrictRedis(
    host='',
    port=,
    password='', ssl=True) 
# Enter Server, host and password. Deleted for security purposes

list1 = []
list2 = []

conn = pypyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        'SERVER=;'
                        'PORT=;'
                        'DATABASE=;'
                        'UID=;'
                        'PWD=')
# Enter Server, UID and PWD. Deleted for security purposes
cursor = conn.cursor()


@app.route('/')
def my_form():
    query = "SELECT MIN(MAG) FROM EARTHQ"
    cursor.execute(query)
    rows = cursor.fetchall()
    return render_template('my-form.html', single=rows[0])


# @app.route("/display", methods=["POST", "GET"])
# def display():
#     range1 = float(request.form.get('m1', ''))
#     range2 = float(request.form.get('m2', ''))
#     query1 = "SELECT * FROM qi WHERE mag = '" + str(range1) + "'"
#     start_time = time.time()
#     cursor.execute(query1)
#     rows = cursor.fetchall()
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     return render_template('display.html', table=rows, rowcount=len(rows), elapsed_time=elapsed_time)

#Quiz 7
@app.route("/display", methods=["POST", "GET"])
def display():
    range1 = float(request.form.get('m1', ''))
    range2 = float(request.form.get('m2', ''))
    query1 = "SELECT qm.latitude, qm.longitude,qm.id FROM qm, qi WHERE qi.mag BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND qm.id=qi.id"
    start_time = time.time()
    cursor.execute(query1)
    rows = cursor.fetchall()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template('display.html', table=rows, rowcount=len(rows), elapsed_time=elapsed_time)

#quiz 8
@app.route("/randomdepthloop", methods=["POST", "GET"])
def randomdepthloop():
    num = int(request.form.get('num', ''))
    range1 = float(request.form.get('depthrange1', ''))
    range2 = float(request.form.get('depthrange2', ''))
    elapsed_time2 =  0
    rand1=[]
    rand2=[]
    timediff=[]
    itrCount=[]
    count=[]


    start_time = time.time()
    start_time2 = time.time()

    for i in range(0, int(num)):
        range1 = round(range1,2)
        rand1.append(range1)
        itrCount.append(i)
        range2 = range1 + 0.1
        range2 = round(range2,2)
        rand2.append(range2)
        query1 = "SELECT * FROM qi WHERE mag BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
        cursor.execute(query1)
        rows = cursor.fetchall()
        count.append(len(rows))
        end_time = time.time()
        elapsed_time = end_time - start_time
        timediff.append(elapsed_time)
        range1 = range1 + 0.1
        range1 = range2
    end_time2 =time.time()
    for i in range(0, int(num)):
        elapsed_time2 = elapsed_time2+timediff[i]


    return render_template('randomdepthloop.html', times=itrCount, timediff=timediff,
                           rand1=rand1, rand2=rand2, count=count, cum=sum(timediff))
    
#quiz 9
@app.route('/restquery', methods=['POST', 'GET'])
def restquery():
    range1 = float(request.form.get('m1', ''))
    range2 = float(request.form.get('m2', ''))
    rows1 = []
    totaltime = 0
    timediff = []

    start2 = time.time()
    query1 = "SELECT qm.latitude, qm.longitude,qm.id FROM qm, qi WHERE qi.mag BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND qm.id=qi.id"
    hash1 = hashlib.sha256(query1.encode()).hexdigest()
    start = time.time()
    if r.get(hash1):
       print("This was return from redis")
    else:
        cursor.execute(query1)
        t1 = cursor.fetchall()
        rows1 = []
        for x in t1:
            rows1.append(str(x))
            r.set(hash1, pickle.dumps(list(rows1)))
            r.expire(hash1, 36)
    end = time.time()
    totaltime = (end - start)
    timediff.append(totaltime)

    query1 = "SELECT qm.latitude, qm.longitude,qm.id FROM qm, qi WHERE qi.mag BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND qm.id=qi.id"
    cursor.execute(query1)
    rows = cursor.fetchall()

    # end2 = time.time()
    # totaltime2 = (end2 - start2)

    return render_template('displaying.html', elapsed_time=timediff, table=rows, rowcount=len(rows))

#quiz 10
@app.route("/randomdepthloopcache", methods=["POST", "GET"])
def randomdepthloopcache():
    num = int(request.form.get('num', ''))
    range1 = float(request.form.get('depthrange1', ''))
    range2 = float(request.form.get('depthrange2', ''))
    elapsed_time2 =  0
    rand1=[]
    rand2=[]
    timediff=[]
    itrCount=[]

    for i in range(0, int(num)):
        itrCount.append(i)
        range1 = round(range1,2)
        rand1.append(range1)
        range2 = range1 + 0.1
        range2 = round(range2,2)
        rand2.append(range2)
        query1 = "SELECT * FROM qi WHERE mag BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
        hash1 = hashlib.sha256(query1.encode()).hexdigest()
        start = time.time()
        if r.get(hash1):
           print("This was return from redis")
        else:
            cursor.execute(query1)
            t1 = cursor.fetchall()
            rows1 = []
            for x in t1:
                rows1.append(str(x))
                r.set(hash1, pickle.dumps(list(rows1)))
                r.expire(hash1, 36)
        end = time.time()
        totaltime = (end - start)
        timediff.append(totaltime)
        range1 = range1 + 0.1
        range1 = range2


    return render_template('randomdepthloopcache.html', times=itrCount, timediff=timediff,
                           rand1=rand1, rand2=rand2, cum=sum(timediff))

#quiz 11
@app.route("/listofqueries", methods=["POST", "GET"])
def listofqueries():
    lat = float(request.form.get('lat', ''))
    longi = float(request.form.get('long', ''))
    range1 = float(request.form.get('magrange1', ''))
    range2 = float(request.form.get('magrange2', ''))
    query1 = "SELECT qm.gmttime, qi.mag, qi.place, qi.id FROM qi,qm WHERE qi.mag BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND qm.latitude='" + str(lat) + "' AND qm.longitude='" +   str(longi) + "' AND qm.id=qi.id"
    start_time = time.time()
    cursor.execute(query1)
    rows = cursor.fetchall()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template('listofqueries.html', table=rows, rowcount=len(rows), elapsed_time=elapsed_time)





# @app.route("/listofqueries", methods=["POST", "GET"])
# def listofqueries():
#     lat = float(request.form.get('lat', ''))
#     longi = float(request.form.get('long', ''))
#     magrange1 = float(request.form.get('magrange1', ''))
#     magrange2 = float(request.form.get('magrange2', ''))
#     query1 = "SELECT * FROM qm WHERE mag BETWEEN '" + str(magrange1) + "' AND '" + str(magrange2) + "' AND latitude='" + str(lat) + "' AND longitude='" + str(longi) + "'"
#     start_time = time.time()
#     cursor.execute(query1)
#     rows = cursor.fetchall()
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     return render_template('listofqueries.html', table=rows, rowcount=len(rows), elapsed_time=elapsed_time)


# @app.route("/queries", methods=["POST", "GET"])
# def queries():
#     # net = request.form.get('net', '')
#     # mag = float(request.form.get('mag', ''))
#     # query1 = "SELECT * FROM EARTHQ WHERE NET LIKE '%" + str(net) + "%'"

#     num = int(request.form.get('num', ''))

#     sql_query_list = []

#     sql1 = "SELECT latitude FROM EARTHQ where locationSource='ak'"
#     sql_query_list.append(sql1)
#     sql2 = "SELECT latitude FROM EARTHQ where locationSource='hv'"
#     sql_query_list.append(sql2)
#     sql3 = "SELECT latitude FROM EARTHQ where locationSource='us'"
#     sql_query_list.append(sql3)
#     lensqllist = len(sql_query_list)

#     start_time = time.time()

#     for i in range(0,int(num)):
#         randid = randint(1, int(lensqllist) - 1)
#         sqlquery = sql_query_list[int(randid)]
#         cursor.execute(sqlquery)
#         rows = cursor.fetchall()

#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     return render_template('queries.html', rowcount=len(rows), elapsed_time=elapsed_time)


# @app.route("/restricted", methods=["POST", "GET"])
# def restricted():
#     num = int(request.form.get('num', ''))
#     start_time = time.time()

#     for i in range(1, int(num)):
#         randid = randint(100, 300)
#         query3 = "SELECT latitude, longitude, depth, mag FROM EARTHQ WHERE latitude = '"+ str(randid) +"'"

#         queryhash = hashlib.sha256(query3.encode()).hexdigest()
#         result = r.get(queryhash)

#         if not result:
#             cursor.execute(query3)
#             result = cursor.fetchall()
#             r.set(queryhash, pickle.dumps(list(result)))

#     end_time = time.time()
#     elapsed_time = end_time - start_time

#     return render_template('restricted.html', elapsed_time=elapsed_time)


# @app.route('/noqueries', methods=['POST', 'GET'])
# def noqueries():
#     totaltime = 0

#     times = int(request.form.get('times', ''))

#     query1 = "SELECT * FROM EARTHQ WHERE mag=3.3"

#     start = time.time()

#     for i in range(0, times):
#         hash1 = hashlib.sha256(query1.encode()).hexdigest()

#         if r.get(hash1):
#             print("This was return from redis")
#         else:
#             cursor.execute(query1)
#             t1 = cursor.fetchall()
#             rows1 = []

#             for x in t1:
#                 rows1.append(str(x))
#                 r.set(hash1, pickle.dumps(list(rows1)))
#                 r.expire(hash1, 36)
#                 print("This is the cached data")

#     end = time.time()
#     totaltime = (end - start)
#     avg = (totaltime / times)

#     elapsed_time = 0

#     for number in range(0, times):
#         start_time = time.time()

#         cursor.execdirect(query1)
#         t12 = cursor.fetchall()

#         end_time = time.time()
#         elapsed_time = (end_time - start_time) + elapsed_time

#     avg_time = (elapsed_time / times)

#     return render_template('noqueries.html', times=times, totaltime=totaltime, avgtime=avg, elapsed_time=elapsed_time,
#                            avg_time=avg_time)


# @app.route('/restrictquery', methods=['POST', 'GET'])
# def restrictquery():

#     times = int(request.form.get('times', ''))
#     mag1 = float(request.form.get('m1', ''))
#     mag2 = float(request.form.get('m2', ''))

#     totaltime = 0

#     start = time.time()

#     for i in range(0, times):
#         val = random.uniform(mag1, mag2)
#         magval = round(val, 2)

#         query1 = "SELECT * FROM EARTHQ WHERE mag = '" + str(magval) + "'"
#         hash1 = hashlib.sha256(query1.encode()).hexdigest()

#         if r.get(hash1):
#             print("This was return from redis")
#         else:
#             cursor.execute(query1)
#             t1 = cursor.fetchall()
#             rows1 = []
#             for x in t1:
#                 rows1.append(str(x))
#                 r.set(hash1, pickle.dumps(list(rows1)))
#                 r.expire(hash1, 36)
#                 print("This is the cached data")

#     end = time.time()
#     totaltime = (end-start)
#     avg = (totaltime/times)

#     elapsed_time = 0

#     for number in range(0, times):
#         start_time = time.time()
#         cursor.execdirect(query1)
#         t12 = cursor.fetchall()
#         end_time = time.time()
#         elapsed_time = (end_time - start_time) + elapsed_time
#     avg_time = (elapsed_time / times)


#     return render_template('restrictquery.html', times=times, totaltime=totaltime, avgtime=avg, elapsed_time=elapsed_time,
#                            avg_time=avg_time)


# @app.route('/restquery', methods=['POST', 'GET'])
# def restquery():
#     times = int(request.form.get('times', ''))
#     mg1 = float(request.form.get('mg1', ''))
#     mg2 = float(request.form.get('mg2', ''))
#     rows1 = []
#     totaltime = 0

#     start = time.time()

#     for i in range(0, times):
#         val = random.uniform(mg1, mg2)
#         magval = round(val, 2)

#         query1 = "SELECT * FROM qm WHERE mag = '"+str(magval)+"'"
#         hash1 = hashlib.sha256(query1.encode()).hexdigest()

#         if r.get(hash1):
#             print("This was return from redis")
#         else:
#             cursor.execute(query1)
#             t1 = cursor.fetchall()
#             rows1 = []
#             for x in t1:
#                 rows1.append(str(x))
#                 r.set(hash1, pickle.dumps(list(rows1)))
#                 r.expire(hash1, 36)
#                 # print("This is the cached data")

#     end = time.time()
#     totaltime = (end - start)
#     avg = (totaltime / times)

#     elapsed_time = 0

#     for number in range(0, times):
#         start_time = time.time()

#         query1 = "SELECT * FROM qm WHERE mag = '"+str(magval)+"'"
#         cursor.execdirect(query1)
#         t12 = cursor.fetchall()

#         end_time = time.time()
#         elapsed_time = (end_time-start_time)+elapsed_time

#     avg_time = (elapsed_time/times)
#     query1 = "SELECT * FROM qm WHERE mag = '"+str(magval)+"'"
#     val = random.uniform(mg1, mg2)
#     magval = round(val, 2)
#     cursor.execute(query1)
#     rows = cursor.fetchall()

#     return render_template('restquery.html', times=times,
#                            totaltime=totaltime, avgtime=avg, elapsed_time=elapsed_time, avg_time=avg_time, table = rows)


# #Q5
# @app.route("/qdisplay", methods=["POST", "GET"])
# def qdisplay():
#     depthrange1 = float(request.form.get('depthrange1', ''))
#     depthrange2 = float(request.form.get('depthrange2', ''))
#     longitude = float(request.form.get('longitude', ''))

#     query1 = "SELECT latitude, longitude, gmttime, depthError FROM EARTHQ WHERE longitude > '" + str(longitude) + "' AND depthError BETWEEN '" + str(depthrange1) + "' AND '" + str(depthrange2) + "'"
#     start_time = time.time()
#     cursor.execute(query1)
#     rows = cursor.fetchall()
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     return render_template('qdisplay.html', table=rows, rowcount=len(rows), elapsed_time=elapsed_time)


# #Q6
# @app.route("/randomdepthloop", methods=["POST", "GET"])
# def randomdepthloop():
#     num = int(request.form.get('num', ''))
#     range1 = float(request.form.get('depthrange1', ''))
#     range2 = float(request.form.get('depthrange2', ''))

#     rand1=[]
#     rand2=[]
#     timediff=[]
#     times = []
#     rowcount = []

#     start_time = time.time()

#     for i in range(0, int(num)):
#         times.append(i)
#         randid1 = random.randrange(range1,range2)
#         rand1.append(randid1)
#         randid2 = random.randrange(range1,range2)
#         rand2.append(randid2)
#         query1 = "SELECT latitude, longitude, gmttime, depthError FROM EARTHQ WHERE depthError BETWEEN '" + str(randid1) + "' AND '" + str(randid2) + "'"
#         cursor.execute(query1)
#         rows = cursor.fetchall()
#         rowcount.append(len(rows))
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#         timediff.append(elapsed_time)

#     return render_template('randomdepthloop.html', times=times, rowcount=rowcount, timediff=timediff,
#                            rand1=rand1, rand2=rand2)


# #Q7
# @app.route('/inmemorycacheornone', methods=['POST', 'GET'])
# def inmemorycacheornone():
#     range1 = float(request.form.get('depthrange1', ''))
#     range2 = float(request.form.get('depthrange2', ''))
#     rand1 = []
#     rand2 = []
#     total2 = 0
#     totaliter = []
#     no = int(request.form.get('num', ''))
#     # query2 = "SELECT latitude, longitude, gmttime, depthError FROM EARTHQ WHERE depthError BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
#     start2 = time.time()

#     for i in range(0, no):
#         totaliter.append(i)
#         randid1 = random.randrange(range1,range2)
#         rand1.append(randid1)
#         randid2 = random.randrange(range1,range2)
#         rand2.append(randid2)
#         query1 = "SELECT latitude, longitude, gmttime, depthError FROM EARTHQ WHERE depthError BETWEEN '" + str(randid1) + "' AND '" + str(randid2) + "'"
#         hash1 = hashlib.sha256(query1.encode()).hexdigest()

#         if r.get(hash1):
#             msg = "Data found in redis cache"
#         else:
#             msg = "Data not found in redis cache"
#     end2 = time.time()
#     total2 = (end2 - start2)
#     avg2 = (total2 / no)

#     return render_template('inmemorycacheornone.html', times=totaliter, rand1=rand1, rand2=rand2, totaltime=total2, avgtime=avg2, msg = msg)

# #Q8
# @app.route('/inmemcachedb', methods=['POST', 'GET'])
# def inmemcachedb():
#     range1 = float(request.form.get('depthrange1', ''))
#     range2 = float(request.form.get('depthrange2', ''))
#     no = int(request.form.get('num', ''))
#     total2 = 0
#     start2 = time.time()
#     rand1=[]
#     rand2=[]
    
#     for i in range(0, no):
#         randid1 = random.randrange(range1,range2)
#         rand1.append(randid1)
#         randid2 = random.randrange(range1,range2)
#         rand2.append(randid2)
#         query2 = "SELECT latitude, longitude, gmttime, depthError FROM earthq WHERE depthError BETWEEN '" + str(randid1) + "' AND '" + str(randid2) + "'"
#         hash1 = hashlib.sha256(query2.encode()).hexdigest()
        
#         if r.get(hash1):
#             print("This was return from redis")
#             msg = "Data found in Redis Cache"
#         else:
#             msg = "Data Not found in Redis Cache"
#             cursor.execute(query2)
#             t2 = cursor.fetchall()
#             rows1 = []
#             for x in t2:
#                 rows1.append(str(x))
#                 r.set(hash1, pickle.dumps(list(rows1)))
#                 r.expire(hash1, 36)
#                 print("This is the cached data")
    
#     end2 = time.time()
#     total2 = (end2 - start2)
#     avg2 = (total2 / no)
#     print('hi2')
    
#     total22 = 0
#     start22 = time.time()
    
#     for number in range(0, no):
#         randid1 = random.randrange(range1,range2)
#         rand1.append(randid1)
#         randid2 = random.randrange(range1,range2)
#         rand2.append(randid2)
#         query2 = "SELECT latitude, longitude, gmttime, depthError FROM earthq WHERE depthError BETWEEN '" + str(randid1) + "' AND '" + str(randid2) + "'"
#         cursor.execdirect(query2)
#         t22 = cursor.fetchall()
#     end22 = time.time()
#     total22 = (end22 - start22)
#     avg22 = (total22 / no)
    
#     return render_template('inmemcachedb.html', times=no, totaltime=total2, avgtime=avg2, totaltime22=total22,avgtime22=avg22, msg = msg, table=rows1) 

# # @app.route('/inmemcachedb', methods=['POST', 'GET'])
# # def inmemcachedb():
# #     range1 = float(request.form.get('depthrange1', ''))
# #     range2 = float(request.form.get('depthrange2', ''))
# #     no = int(request.form.get('num', ''))
# #     total2 = 0
# #     start2 = time.time()
# #     rand1=[]
# #     rand2=[]
    
# #     for i in range(0, no):
# #         randid1 = random.randrange(range1,range2)
# #         rand1.append(randid1)
# #         randid2 = random.randrange(range1,range2)
# #         rand2.append(randid2)
# #         query2 = "SELECT latitude, longitude, gmttime, depthError FROM earthq WHERE depthError BETWEEN '" + str(randid1) + "' AND '" + str(randid2) + "'"
# #         hash1 = hashlib.sha256(query2.encode()).hexdigest()
        
# #         if r.get(hash1):
# #             print("This was return from redis")
# #             msg = "Data found in Redis Cache"
# #         else:
# #             msg = "Data Not found in Redis Cache"
# #             cursor.execute(query2)
# #             t2 = cursor.fetchall()
# #             rows1 = []
# #             for x in t2:
# #                 rows1.append(str(x))
# #                 r.set(hash1, pickle.dumps(list(rows1)))
# #                 r.expire(hash1, 36)
# #                 print("This is the cached data")
    
# #     end2 = time.time()
# #     total2 = (end2 - start2)
# #     avg2 = (total2 / no)
# #     print('hi2')
    
# #     total22 = 0
# #     start22 = time.time()
    
# #     for number in range(0, no):
# #         randid1 = random.randrange(range1,range2)
# #         rand1.append(randid1)
# #         randid2 = random.randrange(range1,range2)
# #         rand2.append(randid2)
# #         query2 = "SELECT latitude, longitude, gmttime, depthError FROM earthq WHERE depthError BETWEEN '" + str(randid1) + "' AND '" + str(randid2) + "'"
# #         cursor.execdirect(query2)
# #         t22 = cursor.fetchall()
# #     end22 = time.time()
# #     total22 = (end22 - start22)
# #     avg22 = (total22 / no)
    
# #     return render_template('inmemcachedb.html', times=no, totaltime=total2, avgtime=avg2, totaltime22=total22,avgtime22=avg22, msg = msg) 


# @app.route('/timerange', methods=['POST', 'GET'])
# def timerange():
#     range1 = request.form.get('timerange1', '')
#     range2 = request.form.get('timerange2', '')
#     times = int(request.form.get('num', ''))

#     totaltime = 0

#     start = time.time()

#     for i in range(0, times):
#         query1 = "SELECT * FROM EARTHQ WHERE gmttime BETWEEN '" + str(range1) + "%' AND '" + str(range2) + "%'"
#         hash1 = hashlib.sha256(query1.encode()).hexdigest()

#         if r.get(hash1):
#             print("This was return from redis")
#         else:
#             cursor.execute(query1)
#             t1 = cursor.fetchall()
#             rows1 = []
#             for x in t1:
#                 rows1.append(str(x))
#                 r.set(hash1, pickle.dumps(list(rows1)))
#                 r.expire(hash1, 36)

#     end = time.time()
#     totaltime = (end - start)
#     avg = (totaltime / times)

#     elapsed_time = 0

#     for number in range(0, times):
#         start_time = time.time()

#         query1 = "SELECT * FROM EARTHQ WHERE gmttime BETWEEN '" + str(range1) + "%' AND '" + str(range2) + "%'"
#         cursor.execdirect(query1)
#         t12 = cursor.fetchall()

#         end_time = time.time()
#         elapsed_time = (end_time-start_time)+elapsed_time

#     avg_time = (elapsed_time/times)

#     return render_template('timerange.html', times=times,
#                            totaltime=totaltime, avgtime=avg, elapsed_time=elapsed_time, avg_time=avg_time, num= len(t12))


# @app.route("/depthErrorRandom", methods=["POST", "GET"])
# def depthErrorRandom():
#     num = int(request.form.get('num', ''))
#     range1 = float(request.form.get('depthrange1', ''))
#     range2 = float(request.form.get('depthrange2', ''))

#     rand1=[]
#     rand2=[]
#     timediff=[]
#     itrCount=[]
#     count=[]


#     start_time = time.time()
#     start_time2 = time.time()

#     for i in range(0, int(num)):
#         itrCount.append(i)
#         #randid1 = random.randrange(range1,range2)
#         #rand1.append(randid1)
#         #randid2 = random.randrange(range1,range2)
#         #rand2.append(randid2)
#         query1 = "SELECT * FROM QI WHERE MAG BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
#         cursor.execute(query1)
#         rows = cursor.fetchall()
#         count.append(len(rows))
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#         timediff.append(elapsed_time)
#         range1 = range1 + 0.1
#         rand1.append(range1)
#         range2 = range2 + 0.1
#         rand2.append(range2) 
#     return render_template('randomdepthloop.html', times=itrCount, timediff=timediff,
#                            rand1=rand1, rand2=rand2, count=count)

@app.route("/depthErrorRandom", methods=["POST", "GET"])
def depthErrorRandom():
    num = int(request.form.get('num', ''))
    range1 = float(request.form.get('depthrange1', ''))
    range2 = float(request.form.get('depthrange2', ''))

    rand1=[]
    rand2=[]
    timediff=[]
    itrCount=[]
    count=[]


    start_time = time.time()
    start_time2 = time.time()

    for i in range(0, int(num)):
        itrCount.append(i)
        #randid1 = random.randrange(range1,range2)
        #rand1.append(randid1)
        #randid2 = random.randrange(range1,range2)
        #rand2.append(randid2)
        query1 = "SELECT * FROM QI WHERE MAG BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
        cursor.execute(query1)
        rows = cursor.fetchall()
        count.append(len(rows))
        end_time = time.time()
        elapsed_time = end_time - start_time
        timediff.append(elapsed_time)
        range1 = range1 + 0.1
        rand1.append(range1)
        range2 = range2 + 0.1
        rand2.append(range2)
    end_time2 = time.time()
    return render_template('randomdepthloop.html', times=itrCount, timediff=timediff,
                           rand1=rand1, rand2=rand2, count=count)

if __name__ == '__main__':
  app.run()
