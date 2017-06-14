import accounts
import pymysql
import memcache
import config
import datetime
import variables

mc = memcache.Client(['127.0.0.1:11211'], debug=config.debug_mode)
db = pymysql.connect('localhost', 'root', config.dbpassword, 'eiotraining')

def generate_id():
	while(1):
		id = mc.gets('cur_id')
		if id == None:
			cursor = db.cursor()
			cursor.execute('SELECT value FROM variables WHERE name = "cur_id"')
			mc.set('cur_id', cursor.fetchone()[0])
			
		elif mc.cas('cur_id', id+1):
			#I know memcache has the "incr" function, but I do this to facilitate 64-bit integers
			if(id % 1000 == 0):
				cursor = db.cursor()
				cursor.execute('UPDATE variables SET value = %s WHERE name = "cur_id"', id + 1000)
				db.commit()
			return id


def signup(user, password, email):
	cursor = db.cursor()
	cursor.execute('SELECT COUNT(*) FROM users WHERE user = %s', user)
	if(cursor.fetchone()[0] != 0):
		return None
	
	salt = accounts.generate_salt(20)
	hash = accounts.get_password_hash(password, salt)
	
	id = generate_id()
	cursor.execute('INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s)', (user, hash, salt, id, email, 0) )
	db.commit()
	mc.set('user:'+user, (user, hash, salt, id, email, 0))
	
	return hash

def get_user_data(user):
	data = mc.get('user:'+user)
	if(data == None):
		cursor = db.cursor()
		cnt = cursor.execute('SELECT * FROM users WHERE user = %s', user)
		if cnt == 0:
			return None
		data = cursor.fetchone()
		mc.set('user:'+user, data)
	return data

def get_user_data_by_id(id):
	data = mc.get('user_by_id:' + str(id))
	if(data == None):
		cursor = db.cursor()
		cnt = cursor.execute('SELECT * FROM users WHERE id = %s', id)
		if cnt == 0:
			return None
		data = cursor.fetchone()
		mc.set('user_by_id:' + str(id), data)
	return data


def check_login(user, password_hash):
	data = get_user_data(user)
	if data == None:
		return False
	return password_hash == data[1]


def login(user, password):
	data = get_user_data(user)
	if data == None:
		return None
	if accounts.get_password_hash(password, data[2]) == data[1]:
		return data[1]
	return None


def create_post(title, content, user_id):
	cursor = db.cursor()
	id = generate_id()
	cursor.execute("INSERT INTO news VALUES (%s, %s, %s, %s, %s)", (title, content, id, datetime.datetime.now(), user_id))
	db.commit()
	mc.delete('posts')


def get_num_posts():
	num_posts = mc.get('num_posts')
	if(num_posts == None):
		cursor = db.cursor()
		cursor.execute('SELECT COUNT(*) FROM news')
		num_posts = cursor.fetchone()[0]
		mc.set('num_posts', num_posts)
	return num_posts

def get_posts(off, cnt):
	posts = mc.get('posts')
	if(posts == None):
		cursor = db.cursor()
		cursor.execute('SELECT * FROM news ORDER BY created DESC')
		posts = cursor.fetchall()
		mc.set('posts', posts)
	return posts[off:off+cnt]


def get_navlinks(parent):
	navlinks = mc.get('navlinks:'+str(parent))
	if(navlinks == None):
		cursor = db.cursor()
		cursor.execute('SELECT * FROM navlinks WHERE parent = %s', parent)
		navlinks = cursor.fetchall()
		mc.set('navlinks:'+str(parent), navlinks)
	return navlinks

def get_navlink(id):
	cursor = db.cursor()
	cursor.execute('SELECT * FROM navlinks WHERE id = %s', id)
	return cursor.fetchone()
	

def create_navlink(parent, type, description):
	cursor = db.cursor()
	id = generate_id()
	#Shouldn't happen, but just in case
	while id == 0:
		id = generate_id()
	
	cursor.execute('INSERT INTO navlinks VALUES (%s, %s, %s, %s)', (parent, id, type, description) )
	if(type == variables.navlink_tutorial or type == variables.navlink_problem):
		cursor.execute('INSERT INTO statements VALUES (%s, %s, %s)', (id, "", type))
	db.commit()
	mc.delete('navlinks:'+str(parent))

def delete_navlink(navlink):
	cursor = db.cursor()
	cursor.execute('DELETE FROM navlinks WHERE id = %s', navlink[1])
	if(navlink[2] == variables.navlink_tutorial or navlink[2] == variables.navlink_problem):
		cursor.execute('DELETE FROM statements WHERE parent = %s', navlink[1])
		mc.delete('statement:' + str(navlink[1]))
	db.commit()
	mc.delete('navlinks:'+str(navlink[0]))


def get_statement(parent):
	statement = mc.get('statement:'+str(parent))
	if(statement == None):
		cursor = db.cursor()
		cursor.execute('SELECT * FROM statements WHERE parent = %s', parent)
		statement = cursor.fetchone()
		mc.set('statement:'+str(parent), statement)
	return statement

def edit_statement(parent, statement_text):
	cursor = db.cursor()
	cursor.execute('UPDATE statements SET statement = %s WHERE parent = %s', (statement_text, parent) )
	db.commit()
	mc.delete('statement:'+str(parent))
	
