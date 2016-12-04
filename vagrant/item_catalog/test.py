import sqlite3

def Main():

	try:	
		con = sqlite3.connect('test.db')
		cur = con.cursor()
		cur.execute('CREATE TABLE Pets(id INT, name TEXT, price INT)')
		cur.execute('INSERT INTO Pets VALUES(1, "Dog", 500)')
		cur.execute('INSERT INTO Pets VALUES(2, "Cat", 500)')
		con.commit()
		cur.execute('SELECT * FROM Pets')
		data = cur.fetchall()
		for row in data:
			print row

	except sqlite3.Error, e:
		if con:
			con.rollback()
			print 'SQL Error: Check your statement and try again.'
	finally:
		if con:
			con.close()
		

		con.close()

if __name__ == '__main__':
	Main()

