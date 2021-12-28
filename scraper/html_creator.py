import mysql.connector
import credsPASSWORDS
import pymysql
import webbrowser, os

from sqlalchemy import engine, types

mode='mysql'#pass this in somehow
creds={
	'host':"",
	'user':"",
	'password':"",
	'port':""
}

if mode=='mysql':
	creds=credsPASSWORDS.mySql
elif mode=='digitalOcean':
	creds=credsPASSWORDS.digitalOcean
else:
	raise Exception("Don't support database: "+mode)

host=creds['host']
user=creds['user']
password=creds['password']
port=creds['port']

mysql_engine=''

if mode=='mysql':
	#mysql_engine=mysql.connector.connect(user=user, password=password,host=host,database='scraper')
	connectionString = "mysql+pymysql://" + user + ":" + password + "@" + host + ":" + port
	mysql_engine = engine.create_engine(connectionString)
elif mode=='digitalOcean':
	connectionString="mysql+mysqlconnector://"+user+":"+password+"@"+host+":"+port
	mysql_engine = engine.create_engine(connectionString) #mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
else:
	raise Exception("Don't support database: "+mode)

sqlSelect = "SELECT `Date`, `Company`, `Title`, `Location`, `Description`, `Link`, `Seniority level`, `Employment type`, `Job function`, `Industries` FROM `scraper`.`jobs`;"

connection = mysql_engine.connect()
result = connection.execute(sqlSelect).fetchall()

p = []

tbl = "<tr><td>ID</td><td>Name</td><td>Email</td><td>Phone</td></tr>"
p.append(tbl)

for row in result:
    a = "<tr><td>%s</td>"%row[0]
    p.append(a)
    b = "<td>%s</td>"%row[1]
    p.append(b)
    c = "<td>%s</td>"%row[2]
    p.append(c)
    d = "<td>%s</td></tr>"%row[3]
    p.append(d)

contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta content="text/html; charset=ISO-8859-1"
http-equiv="content-type">
<title>Python Webbrowser</title>
</head>
<body>
<table>
%s
</table>
</body>
</html>
'''%(p)

filename = 'webbrowser.html'

def main(contents, filename):
    output = open(filename,"w")
    output.write(contents)
    output.close()

main(contents, filename)

webbrowser.open('file://' + os.path.realpath(filename))