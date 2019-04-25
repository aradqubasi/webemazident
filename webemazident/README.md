#Webemazident
====

It is a fun-app which is providing simple web access to sentiment analysis services via external translation and sentiment analysis APIs. 

#Technology
====

##Current

- Python 3.6
- Flask app in its core
- Mongo db as a persistance layer 
- Janja templates for rendering of dynamic content
- CDN version of bootstrap for styling
- CDN version of fontawesome
- Google translation API
- GMOTION sentiment analysis API

##Optional

- Digital Ocean cloud hosting - Ubuntu droplets
- Gunicorn 
- Nginx

##Planned

- Redis
- RQ workers
- Google authorization
- More API options
- My own sentiment analysis... maybe

#Installation
====

Original setup depends heavily on Digital Ocean droplets.

##Useful links

- [Initial Server Setup with Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04)
- [How to Install MongoDB on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-18-04)
- [How to Install and Secure MongoDB on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-mongodb-on-ubuntu-16-04#part-two-securing-mongodb)
- [How To Install Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)
- [How To Set Up Nginx Server Blocks (Virtual Hosts) on Ubuntu 14.04 LTS](https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-14-04-lts)
- [How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04#step-3-—-setting-up-a-flask-application)

##Command line walkthrough 

###Parameters

Installation depends on number of user-defined entities, like system user name, passwords, database names, instances name etc. Below is a list such entities. Each time you see %%ENTITY NAME%% in command line - replace it with your value.

###Initial Server Setup