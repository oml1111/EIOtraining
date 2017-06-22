import string
import random
import hashlib

"""
For storing passwords we use sha256 hashing with salts.
It's not great, but for our purposes it's sufficient.
If the site gets popular, then this approach needs
to be changed
"""

def generate_salt(len):
	return ''.join([random.choice(string.hexdigits) for i in range(len)])
	
def get_password_hash(password, salt):
	return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()