#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgitb
cgitb.enable()

from flask import Flask, render_template, make_response, request, redirect
import database
import re
import variables

app = Flask(__name__)



#---------------------------------------------------------------------------
#Auxilliary functions common across many request handlers

def get_user():
	"""Returns the username of the currently logged in user"""
	user = request.cookies.get('user')
	hash = request.cookies.get('password_hash')
	if(user != None and user != '' and database.check_login(user, hash)):
		return user
	return None


def render_page(file, lang = "en/", **args):
	"""Renders the given page.
	Performs functionality every page needs,
	checks whether an user is logged in and
	if the user is an admin
	"""
	user = get_user()
	admin = False
	if user != None:
		user_data = database.get_user_data(user)
		args['login'] = user
		if(user_data[5] >= variables.admin_privilige):
			args['admin'] = True
			admin = True
		
	resp = make_response(render_template(lang+file, **args) )
	if user == None:
		resp.set_cookie('user', '', expires = 0)
		resp.set_cookie('password_hash', '', expires = 0)
	return resp

def is_admin_logged():
	user = get_user()
	if user == None:
		return False
	
	user_data = database.get_user_data(user)
	if(user_data[5] < variables.admin_privilige):
		return False
	return True


@app.route('/')
def index(lang = "en/"):
	posts = database.get_posts(0, 10)
	posts_and_users = [(post[0:5], post[5]) for post in posts]
	return render_page("index.html", lang, posts_and_users = posts_and_users)

@app.route('/et/')
def et_index():
	return index("et/")
	
	
#---------------------------------------------------------------------------
#User account request handlers


@app.route('/login', methods = ['GET', 'POST'])
def login(lang = "en/"):
	if request.method == 'GET':
		return render_page("login.html", lang)
	else:
		user = request.form['user']
		password = request.form['password']
		hash = database.login(user, password)
		if hash == None:
			lang_errors = {	"en/" : u"Incorrect login information!",
							"et/" : u"Sisselogimine ebaõnnestus!"}
			return render_page("login.html", lang, user=user, error = lang_errors[lang])
			
		resp = make_response(redirect('/' if lang == "en/" else "/et/"))
		resp.set_cookie('user', user)
		resp.set_cookie('password_hash', hash)
		return resp

@app.route('/et/login', methods = ['GET', 'POST'])
def et_login():
	return login("et/")

@app.route('/logout')
def logout(lang=''):
	resp = make_response(redirect(lang+'/'))
	resp.set_cookie('user', '', expires = 0)
	resp.set_cookie('password_hash', '', expires=0)
	return resp
	
@app.route('/et/logout')
def et_logout():
	return logout('/et')

@app.route('/signup', methods = ['GET', 'POST'])
def signup(lang='en/'):
	if request.method == 'GET':
		return render_page("signup.html", lang)
	else:
		user = request.form['user']
		password = request.form['password']
		verify = request.form['verify']
		email = request.form['email']
		
		user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		password_re = re.compile(r"^.{6,50}$")
		email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
		
		invalid_user, invalid_password, invalid_verify, invalid_email = False, False, False, False
		
		if not user_re.match(user):
			invalid_user = True
		if not password_re.match(password):
			invalid_password = True
		if verify != password:
			invalid_verify = True
		if not email_re.match(email):
			invalid_email = True
		
		if invalid_user or invalid_password or invalid_verify or invalid_email:
			return render_page("signup.html", lang, user = user, email = email, invalid_user = invalid_user, invalid_password = invalid_password, invalid_verify = invalid_verify, invalid_email = invalid_email)
		
		hash = database.signup(user, password, email)
		if(hash == None):
			lang_errors = {	"en/" : u"User already exists",
							"et/" : u"Kasutajanimi on juba võetud"}
			return render_page("signup.html", lang, user = user, email = email, error = lang_errors[lang])
			
		resp = make_response(redirect('/' if lang == "en/" else "/et/"))
		resp.set_cookie('user', user)
		resp.set_cookie('password_hash', hash)
		return resp

@app.route('/et/signup', methods = ['GET', 'POST'])
def et_signup():
	return signup('et/')


@app.route('/newpost', methods = ['GET', 'POST'])
def newpost():
	if not is_admin_logged():
		return redirect('/')
	
	if request.method == 'GET':
		return render_page("newpost.html")
	else:
		title = request.form['title']
		content = request.form['content']
		
		user_data = database.get_user_data(get_user() )
		
		if(title == '' or content == ''):
			return render_page("newpost.html", error="Need both title and content", title = title, content = content)
		
		database.create_post(title, content, user_data[3])
		return redirect('/')




#---------------------------------------------------------------------------
#Problemset request handlers


def navevent_dfs(parent, navevents):
	"""Recursive function to create the problemset navigation tree structure"""
	navlinks = database.get_navlinks(parent)
	for navlink in navlinks:
		navevents.append((0, navlink) )
		if navlink[2] == variables.navlink_folder:
			navevent_dfs(navlink[1], navevents)
		navevents.append((1, navlink) )




@app.route('/problemset/<int:page_id>')
def problemset(page_id, lang="en/"):
	navevents = []
	navevent_dfs(0, navevents)
	
	statement = database.get_statement(page_id)
	statement_text = "<div class='errormsg'>Statement doesn't exist. Need to fix this!</div>"
	if page_id == 0:
		statement_text = "<h3>Welcome to the problem set</h3>"
	if statement:
		statement_text = statement[1]
	
	return render_page("problemset.html", lang, navevents = navevents, statement=statement_text)
	

@app.route('/et/problemset/<int:page_id>')
def et_problemset(page_id):
	return problemset(page_id, "et/")


@app.route('/problemset')
def problemset_index():
	return problemset(0)
	
	
@app.route('/et/problemset')
def et_problemset_index():
	return problemset(0, "et/")
	
	
@app.route('/navadd/<int:nav_id>', methods = ['GET', 'POST'])
def navadd(nav_id):
	if not is_admin_logged():
		return redirect('/')
	
	if request.method == 'GET':
		return render_page('navadd.html')
	else:
		type = int(request.form['type'])
		description = request.form['description']
		
		if(description == '' or len(description) > 255):
			return render_page('navadd.html', error="Description must be between 1 and 255 letters")
		
		database.create_navlink(nav_id, type, description)
		return redirect('/problemset')


@app.route('/problemset/delete/<int:nav_id>', methods = ['GET', 'POST'])
def problemset_delete(nav_id):
	"""The navlink deletion is recursive, all descendants get
	deleted as well
	"""
	navlink = database.get_navlink(nav_id)
	if navlink == None:
		return redirect('/problemset')
		
	if not is_admin_logged():
		return redirect('/problemset')
	
	if request.method == 'GET':
		return render_page('psdelete.html', navlink = navlink)
	else:
		navevents = []
		navevent_dfs(nav_id, navevents)
		navevents.append((1, navlink))
		
		for navevent in navevents:
			if navevent[0] == 1:
				database.delete_navlink(navevent[1])
		return redirect('/problemset')


@app.route('/problemset/edit/<int:parent>', methods = ['GET', 'POST'])
def problemset_edit(parent):
	statement = database.get_statement(parent)
	if statement == None:
		return redirect('/problemset')
		
	if not is_admin_logged():
		return redirect('/problemset')
	
	
	if request.method == 'GET':
		return render_page('psedit.html', statement = statement)
	else:
		statement_text = request.form['statement']
		database.edit_statement(parent, statement_text )
		return redirect('/problemset')