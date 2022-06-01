import sqlite3

#Open database
conn = sqlite3.connect('student.db')

#Create table
conn.execute('''CREATE TABLE profile 
		(userId PRIMARY KEY, 
		password TEXT,
		email TEXT,
		name TEXT,
		roll TEXT,
		program TEXT,
		branch TEXT,
		batch TEXT,
		dob TEXT,
		presentaddress TEXT,
		permanentaddress TEXT,
		mobile TEXT,
		parentmobile TEXT,
		bloodgroup TEXT,
		allergic TEXT,
		cgpa TEXT,
		skills TEXT,
		linkedin TEXT,
		photo TEXT
		)''')

conn.execute('''CREATE TABLE help
		(roll TEXT,
		query TEXT,
		date TEXT,
		status TEXT,
		verify TEXT
		email TEXT
		)''')

conn.execute('''CREATE TABLE admin
		(email TEXT,
		password TEXT,
		name TEXT
		)''')

conn.execute('''CREATE TABLE service
		(email TEXT,
		password TEXT,
		serviceType TEXT,
		name TEXT
		)''')


conn.close()

