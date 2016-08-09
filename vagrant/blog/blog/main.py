#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import re

import string
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

# Used by the SignUp class to  validate the user inputs using pythons Re
# library
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	''' Returns a user name if it includes letters a-z, A-Z or any number or _
	and is longer than 3 characters but not longer than 20.'''
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
	''' Returns an email it when it has an @ and . '''
	return not email or EMAIL_RE.match(email)

class Handler(webapp2.RequestHandler):
	'''This is a helper class it has several helper methods it inherits
	webapp2.RequestHandler.'''
	def write(self, *a, **kw):
		''' A simple helper function that prints a string.'''
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		''' This method takes a file name and paramaters added, then 
		calls get_template and gives it a file name. Then renders the jinja
		template. It returns a sting.'''
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		''' This takes a templates calls render_str and wraps it in self.write
		and is sent back to the browser.'''
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	''' This is the main web application it inherits Handler in order to be 
	able to use its helper functions.'''
	def get(self):
		'''This method handels all get requests.'''
		self.render("shopping_list.html")

class FizzBuzzHandler(Handler):
	''' Is an application that takes a value and returns its FizzBuzz value
	in an ordered list.'''
	def get(self):
		n = self.request.get('n', 0)
		n = n and int(n)
		self.render('fizzbuzz.html', n = n)


class RoT13(Handler):
	''' This class takes a string input value from a URL and returns its 
	Rot 13 equal. The string library is used to translate the given text.'''
	
	text = 'Enter Some Text to Rott'

	def get(self):
		self.render('rotted.html')


	def post(self):
		rot13 = ''
		text = self.request.get('text')
		if text:
			rot13 = text.encode('rot13')

		self.render('rotted.html', text = rot13)


class SignUp(Handler):
	''' This class takes user inpput from a URL and validates that it was 
	filled out, if any fields are left blank a notice is displayed.'''
	error = ''
	
	def get(self):
		self.render('signup.html')

	def post(self):
		has_error = False
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		params = dict(username = username,
					email = email)

		if not valid_username(username):
			params['error_username'] = "User name not valid"
			has_error = True

		if not valid_password(password):
			params['error_password'] = "Your password needs help! Please check it!"
			has_error = True
		elif password != verify:
			params['error_verify'] = "Yo you need to use matching passwords"
			has_error = True

		if not valid_email(email):
			params['verify'] = "Yo this email aint right! CHECK IT."
			has_error = True

		if has_error:
			error= 'Yo check your inputs'
			self.render('signup.html', **params)
		else:
			self.redirect('/welcome?username=' + username)

class Welcome(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/signup')	

app = webapp2.WSGIApplication([('/', MainPage),
								('/fizzbuzz', FizzBuzzHandler),
								('/rotted', RoT13),
								('/signup', SignUp),
								('/welcome', Welcome),
								],
								debug=True)
