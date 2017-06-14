import string
import random
import hashlib

def generate_salt(len):
	return ''.join([random.choice(string.hexdigits) for i in range(len)])
	
def get_password_hash(password, salt):
	return hashlib.sha256(password + salt).hexdigest()