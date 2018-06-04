### steps to start
1. create database in mysql according settings in settings.py => DATABASES
2. pipenv install
3. pipenv shell
4. cd recommend && ./manage.py runserver 0:8000

### steps to send news notification
1. locate http://<host>:8000/admin/, test server username/password is patsnap/winterfall
2. in the news tab, click news to enter a list, and add news content with the button on the top right corner.

### query the keyword
http://192.168.5.179:8983/patsnap/#/keyword/query