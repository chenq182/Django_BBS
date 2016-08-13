#!/bin/bash
sudo apt-get install git
git clone https://github.com/chenq182/Django_BBS

sudo -i

mv Django_BBS/django /
mv Django_BBS/vimrc ~/.vimrc

# install apache
apt-get install apache2
mkdir /var/www/static
mkdir /var/www/upload
chown www-data /var/www/upload
chgrp www-data /var/www/upload

apt-get install apache2-dev python2.7-dev
    apt-get install libpython2.7-dev=2.7.9-2ubuntu3
    ...

# https://github.com/GrahamDumpleton/mod_wsgi/releases
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.5.3.tar.gz
tar zxvf 4.5.3.tar.gz
cd mod_wsgi-4.5.3/
./configure
make
make install

cd ..
rm -rf mod_wsgi-4.5.3/ 4.5.3.tar.gz

cat Django_BBS/apache2.conf >> /etc/apache2/apache2.conf

# install mysql
apt-get install mysql-server
apt-get install libapache2-mod-auth-mysql
vi /etc/mysql/mysql.conf.d/mysqld.cnf
    #[mysqld]
    #character_set_server = utf8
    #collation-server = utf8_general_ci
/etc/init.d/mysql restart
mysql -uroot -p
    #source /root/Django_BBS/django.sql
    #show variables like '%character%';
    #exit;

# install Django
apt-get install python-pip
pip install Django
apt-get install libmysqlclient-dev
pip install mysql-python
/etc/init.d/apache2 restart

# django
cd /django
python manage.py collectstatic
python manage.py makemigrations bbs
python manage.py migrate
python manage.py createsuperuser


