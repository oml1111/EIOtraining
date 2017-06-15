Directory contents:

- eiotraining/ - the main project folder
- pymysql/ - the downloaded PyMySQL python library, used for reference
- test/ - a test project folder
- database.pdf - high-level description of the database
- database.png - picture for the pdf file
- database.tex - LATEX file for the pdf
- database.txt - low-level description of the database
- download.sh - script to download the project from the server
- memcache.py - the memcached python library, used for reference
- notes.txt - Some likely important details to remember
- README.MD - this file, folder content description
- setup.txt - description on how the server was set up in the VM
- sshsetup.txt - steps to get ssh working properly
- test.html - a html file for testing html stuff
- upload.sh - script to upload the project to the VM

Techniques:

1. Optimization - Handled in database.py. Every SQL query has been cached. For caching we used the "memcached" library. This automatically ensures that the most popular queries are in cache and won't hit the database, also it makes programming simpler by allowing us to request the same data multiple times without having to hit the DB
2. Database Operations - Handled in database.py. We perform database insertions and queries in multiple places in different ways. We also use a simple "COUNT" aggregated query to get the size of the "users" table.
3. Code Repository - Obviously this has been done
4. Javascript - Handled in main.py and static/psload.js. Functionality visible in "/problemset" url. Used for the navigation tree system.
5. Authorization - Handled in main.py, database.py and accounts.py. Any account can view stuff, but only admin accounts can edit the page.
6. Templating System (not mentioned, but should be) - Handled in main.py. To allow us to place stuff to web pages in a cleaner fashion, we use the jinja2 templating system