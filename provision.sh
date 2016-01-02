#!/usr/bin/env bash

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
locale-gen en_US.UTF-8
dpkg-reconfigure locales

apt-get update
apt-get install -y git 
apt-get install -y python-pip 
apt-get install -y libpq-dev
apt-get install -y python-dev
apt-get install -y python-virtualenv
apt-get install -y postgresql
apt-get install -y postgresql-contrib
apt-get install -y libffi-dev
apt-get install -y libssl-dev
# Specific requirements for PIL. Comment if not necessary.
apt-get install -y libpng-dev libgif-dev libjpeg-dev libtiff-dev
apt-get install -y memcached

apt-get install -y vim
apt-get install -y g++
apt-get install -y ruby1.9.1

# Configure PostgreSQL
# Check if database exsits
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -w network; then
sudo -u postgres psql << EOF
    CREATE DATABASE network;
    CREATE USER network WITH PASSWORD 'network';
    ALTER USER network CREATEDB;
    GRANT ALL PRIVILEGES ON DATABASE network TO network;
EOF
fi

if ! [ -L /home/vagrant/NetWork_Practice ]; then
  ln -fs /vagrant /home/vagrant/NetWork_Practice
fi

cd /home/vagrant/NetWork_Practice
pip install -r requirements.txt

# cd /home/vagrant/NetWork_Practice
# psql -h localhost -p '' -U network< network_test.sql <<EOF
# network
# EOF

# sync database, please exec them in vm
# python manage.py syncdb
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver
