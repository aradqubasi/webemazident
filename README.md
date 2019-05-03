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
%%NON_ROOT_USER%%

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

### Serve Flask Applications with Gunicorn

### Systemctl

```
sudo systemctl status %%SERVICE_NAME%%
sudo systemctl start %%SERVICE_NAME%%
sudo systemctl stop %%SERVICE_NAME%%
sudo systemctl restart %%SERVICE_NAME%%
```

### Mongo shell

```
use %%DATABASE_NAME%%
db.auth('%%LOGIN%%', '%%PASSWORD%%')
show dbs
show users
```