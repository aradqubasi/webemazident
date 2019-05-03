# Webemazident

It is a fun-app which is providing simple web access to sentiment analysis services via external translation and sentiment analysis APIs. 

# Technology

## Current

- Python 3.6
- Flask app in its core
- Mongo db as a persistance layer 
- Janja templates for rendering of dynamic content
- CDN version of bootstrap for styling
- CDN version of fontawesome
- Google translation API
- GMOTION sentiment analysis API

## Optional

- Digital Ocean cloud hosting - Ubuntu droplets
- Gunicorn 
- Nginx

## Planned

- Pytest coverage
- Redis
- RQ workers
- Google authorization
- More API options
- My own sentiment analysis... maybe

# Installation

Original setup depends heavily on Digital Ocean droplets.

## Useful links

- [Initial Server Setup with Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04)
- [How to Install MongoDB on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-18-04)
- [How to Install and Secure MongoDB on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-mongodb-on-ubuntu-16-04#part-two-securing-mongodb)
- [How To Install Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)
- [How To Set Up Nginx Server Blocks (Virtual Hosts) on Ubuntu 14.04 LTS](https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-14-04-lts)
- [How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04#step-3-—-setting-up-a-flask-application)

## Command line walkthrough 

### Parameters

Installation depends on number of user-defined entities, like system user name, passwords, database names, instances name etc. Below is a list such entities. Each time you see %%ENTITY_NAME%% in command line - replace it with your value.

%%YOUR_SERVER_IP%%
IP address of your droplet like 134.205.223.50

%%NON_ROOT_USER%%
Any valid username, like subroot

%%PROJECT_FOLDER%%
Any valid folder name, like webemazident

%%PYTHON_VIRTUAL_ENVIRONMENT_NAME%%
Alphanumeric without spaces, like dev-1-env

%%NAME_OF_PROJECT%%
Alphanumeric without spaces, like webemazident

%%DATABASE_CONNECTION_STRING%%
Mongobd connection string, without database, like mongodb://username:userpwd@165.227.154.157:27017

%%DATABASE_NAME%%
Any valid mongodb database name, like dev-1

%%GOOGLE_API_KEY%%
Valid Google-API key, authorized to perform translation calls

%%GEMOTION_RAPID_API_KEY%%
%%GEMOTION_AUTH_TOKEN%%

%%FLASK_START_UP%%
Flask app start command, like webemazident:create_app()

%%DOMAIN_NAME%%
Any valid domain you have registered for your server, without protocol and www. like ghfj.ml

### Initial Server Setup

Connecting to your droplet, creating of non-root user, granting privileges to run commands as administrator, initial set up of firewall

```
ssh root@%%YOUR_SERVER_IP%%
adduser %%NON_ROOT_USER%%
usermod -aG sudo %%NON_ROOT_USER%%
ufw app list
ufw allow OpenSSH
ufw enable
ufw status
```

Now you can connect using non-root user

```
ssh %%NON_ROOT_USER%%@%%YOUR_SERVER_IP%%
```

### Install MongoDB

```
sudo apt update
sudo apt install -y mongodb
sudo systemctl status mongodb
mongo --eval 'db.runCommand({ connectionStatus: 1 })'
sudo nano /etc/mongodb.conf
```

Modify configuration file in nano text editor

```
...
bind_ip = 127.0.0.1,%%YOUR_SERVER_IP%%
...
```

Back at  the command prompt check status of mongodb service and enter mongo shell

```
sudo systemctl restart mongodb
mongo
```

At mongo shell create admin user

```
use admin
db.createUser({
    user : "%%DATABASE_ADMIN_USER_NAME%%",
    pwd : "%%DATABASE_ADMIN_USER_PASSWORD%%",
    roles: [{
        role : "readWriteAnyDatabase",
        db : "admin"
    }, {
        role : "userAdminAnyDatabase",
        db : "admin"
    }, {
        role : "dbAdminAnyDatabase",
        db : "admin"
    }]
})
```

Back at command prompt, open configuration file to enable authentication

```
sudo nano /etc/mongodb.conf
```

Modify configuration file in nano text editor

```
...
#noauth = true
auth = true
...
```

Back at command prompt, restart mongodb service

```
sudo systemctl restart mongodb
sudo systemctl status mongodb
```

### Install Nginx

```
sudo apt update
sudo apt install nginx
sudo ufw app list
sudo ufw allow 'Nginx HTTP'
sudo ufw status
sudo systemctl status nginx
```

### Prepare Python environment

```
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv
mkdir ~/%%PROJECT_FOLDER%%
cd ~/%%PROJECT_FOLDER%%
python3.6 -m venv %%PYTHON_VIRTUAL_ENVIRONMENT_NAME%%
source %%PYTHON_VIRTUAL_ENVIRONMENT_NAME%%/bin/activate
pip install wheel
pip install gunicorn flask
...
deactivate
```

### Configuring Gunicorn

```
sudo nano /etc/systemd/system/%%NAME_OF_PROJECT%%
```

Insert next text and save

```
[Unit]
Description=Gunicorn instance to serve dev-1 environment
After=network.target

[Service]
User=%%NON_ROOT_USER%%
Group=www-data
WorkingDirectory=/home/%%NON_ROOT_USER%%/%%NON_ROOT_USER%%/%%NAME_OF_PROJECT%%
Environment="PATH=/home/%%NON_ROOT_USER%%/%%NON_ROOT_USER%%/%%NAME_OF_PROJECT%%/%%PYTHON_VIRTUAL_ENVIRONMENT_NAME%%/bin"
Environment="CONNECTION_STRING=%%DATABASE_CONNECTION_STRING%%"
Environment="DATABASE=%%DATABASE_NAME%%"
Environment="GOOGLE_API_KEY=%%GOOGLE_API_KEY%%"
Environment="RAPID_API_KEY=%%GEMOTION_RAPID_API_KEY%%"
Environment="GEMOTION_AUTH_TOKEN=Token token=\"%%GEMOTION_AUTH_TOKEN%%\""
ExecStart=/home/%%NON_ROOT_USER%%/%%NAME_OF_PROJECT%%/%%PYTHON_VIRTUAL_ENVIRONMENT_NAME%%/bin/gunicorn --workers 3 --bind unix:%%NAME_OF_PROJECT%%.sock -m 007 %%FLASK_START_UP%%

[Install]
WantedBy=multi-user.target
```
Save and return to command prompt
```
sudo systemctl start %%NAME_OF_PROJECT%%
sudo systemctl enable %%NAME_OF_PROJECT%%
sudo systemctl status %%NAME_OF_PROJECT%%
sudo nano /etc/nginx/sites-available/%%NAME_OF_PROJECT%%
```

Insert next text and save

```
server {
    listen 80;
    server_name %%DOMAIN_NAME%% www.%%DOMAIN_NAME%%;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/%%NON_ROOT_USER%%/%%NAME_OF_PROJECT%%.sock;
    }
}
```

Back at the command prompt

```
sudo ln -s /etc/nginx/sites-available/%%NAME_OF_PROJECT%% /etc/nginx/sites-available/
sudo nginx -t
sudo systemctl restart nginx
```

### Checking logs

```
sudo less /etc/log/nginx/error.log
sudo less /etc/log/nginx/access.log
sudo journalctl -u nginx
sudo journalctl -u %%NAME_OF_PROJECT%%
```

### Systemctl

Useful commands

Current status

```
sudo systemctl status %%SERVICE_NAME%%
sudo systemctl start %%SERVICE_NAME%%
sudo systemctl stop %%SERVICE_NAME%%
sudo systemctl restart %%SERVICE_NAME%%
```

Manage auto-start

```
sudo systemctl enable %%SERVICE_NAME%%
sudo systemctl disable %%SERVICE_NAME%%
```

### Mongo shell

Useful commands

```
use %%DATABASE_NAME%%
db.auth('%%LOGIN%%', '%%PASSWORD%%')
show dbs
show users
```