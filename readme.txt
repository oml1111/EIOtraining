Directory contents:

eiotraining/	- the main project folder
test/			- a test project folder
download.sh		- script to download the project from the server
readme.txt		- this file, folder content description + notes
setup.txt		- description on how the server was set up in the VM
sshsetup.txt	- steps to get ssh working properly
upload.sh		- script to get

Some important notes about the project:
1. I opted to keep MySQL anonymous user. Should remove it later
2. I disallowed remote root login in MySQL
3. I opted to keep the 'test' MySQL database
4. The "#!/usr/bin/python" line in scripts is IMPORTANT!
5. I opted not to use virtualenv