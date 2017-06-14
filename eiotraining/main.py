#!/usr/bin/python
import cgitb
cgitb.enable()

from flask import Flask, render_template, make_response, request, redirect
import database
import re
import variables

app = Flask(__name__)



def get_user():
	user = request.cookies.get('user')
	hash = request.cookies.get('password_hash')
	if(user != None and user != '' and database.check_login(user, hash)):
		return user
	return None


def render_page(file, **args):
	user = get_user()
	admin = False
	if user != None:
		user_data = database.get_user_data(user)
		args['login'] = user
		if(user_data[5] >= variables.admin_privilige):
			args['admin'] = True
			admin = True
		
	resp = make_response(render_template(file, **args) )
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
def index():
	posts = database.get_posts(0, 10)
	posts_and_users = [(post, database.get_user_data_by_id(post[4])[0]) for post in posts]
	return render_page("index.html", posts_and_users = posts_and_users)
	
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_page("login.html")
	else:
		user = request.form['user']
		password = request.form['password']
		hash = database.login(user, password)
		if hash == None:
			return render_page("login.html", user=user, error = "Incorrect login information!")
			
		resp = make_response(redirect('/'))
		resp.set_cookie('user', user)
		resp.set_cookie('password_hash', hash)
		return resp


@app.route('/logout')
def logout():
	resp = make_response(redirect('/'))
	resp.set_cookie('user', '', expires = 0)
	resp.set_cookie('password_hash', '', expires=0)
	return resp

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_page("signup.html")
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
			return render_page("signup.html", user = user, email = email, invalid_user = invalid_user, invalid_password = invalid_password, invalid_verify = invalid_verify, invalid_email = invalid_email)
		
		hash = database.signup(user, password, email)
		if(hash == None):
			return render_page("signup.html", user = user, email = email, error = "User already exists")
			
		resp = make_response(redirect('/'))
		resp.set_cookie('user', user)
		resp.set_cookie('password_hash', hash)
		return resp


@app.route('/newpost', methods = ['GET', 'POST'])
def newpost():
	if not is_admin_logged():
		return redirect('/')
	
	if request.method == 'GET':
		return render_page("newpost.html")
	else:
		title = request.form['title']
		content = request.form['content']
		
		if(title == '' or content == ''):
			return render_page("newpost.html", error="Need both title and content", title = title, content = content)
		
		database.create_post(title, content, user_data[3])
		return redirect('/')



def navevent_dfs(parent, navevents):
	navlinks = database.get_navlinks(parent)
	for navlink in navlinks:
		navevents.append((0, navlink) )
		if navlink[2] == variables.navlink_folder:
			navevent_dfs(navlink[1], navevents)
		navevents.append((1, navlink) )




@app.route('/problemset/<int:page_id>')
def problemset(page_id):
	navevents = []
	navevent_dfs(0, navevents)
	
	statement = database.get_statement(page_id)
	statement_text = "<div style='color:red;'>Statement doesn't exist. Need to fix this!</div>"
	if statement:
		statement_text = statement[1]
	
	return render_page("problemset.html", navevents = navevents, statement=statement_text)


@app.route('/problemset')
def problemset_index():
	return problemset(0)
	
	
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