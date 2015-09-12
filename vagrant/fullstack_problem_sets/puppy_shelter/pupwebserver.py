from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppy_db_setup import Base, Shelter, Puppy, Adoptor, AdoptorAndPuppy
from pup_test import * 
# Create session and connect to DB


# Create session and connect to DB
engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



class webServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/pups/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a new</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newPupName' type = 'text' placeholder = 'Pups Name' > "
                output += "<input type='radio' name='sex' value='male'> Male"
                output += "<input type='radio' name='sex' value='female'> Female"
                output += "<input type='submit' value='Add Pup'>"
                output += "</form></html></body>"
                self.wfile.write(output)
                return					


			if self.path.endswith("/pups"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body><h1>Welcome to Pup City</h1>"
				output += "<ul><li><a href='pups/available'>View All Pups</a></li><li>View Shelter Status</li><li>Adopt a Pup</li><li><a href ='pups/change'>Edit Pups</li><li><a href= 'pups/add'>Add a Pup</a></li></ul>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/pups/available"):
				gotPups = getPupsAtoZ()
				if gotPups:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body><h1>Pups In Shelters</h1>"
					output += "<ul>"
					for pup in gotPups:
						output += "<li>"
						output += pup.name
						output += "<br><a href='pups/adopt'>Adopt<a>" 
						output += "</li>"
					output += "</ul>"
					output += "<br>"
					output += "</body></html>"
					self.wfile.write(output)
					print output
					return


			if self.path.endswith("/pups/change"):
				gotPups = getPupsAtoZ()
				if gotPups:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body><h1>Pups In Shelters</h1>"
					output += "<ul>"
					for pup in gotPups:
						output += "<li>"
						output += pup.name
						output += "<br><a href='pups/edit'>Edit</a>"
						output += "<br><a href='pups/delete'>Delete</a>"
						output += "</li>"
						output += "<bt>"
					output += "</ul>"
					output += "</body></html>"
					self.wfile.write(output)
					print output
					return



		except IOError:
			self.send_error(404, "File not found %s" % self.path)

	def do_post(self):
		if self.path.endswith('/pups/add'):
            ctype, pdict = cgi.parse_header(
            	self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]			




		
	

def main():
    try:
    	port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print 'Web server running...open localhost:8080/pups in your browser'
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()


if __name__ == '__main__':
    main()