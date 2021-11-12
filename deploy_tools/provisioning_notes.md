### New site requirements:
`python`==3.8 <br>
`Django`==3.2.9 <br>
`python-dotenv`==0.19.1 <br>
`gunicorn`==20.1.0

Additonally had to install `pip` and `python3-venv` on AWS instance.
> $ sudo apt update <br>
$ sudo apt upgrade <br>
$ sudo apt install python3-pip <br>
$ sudo apt install python3-venv

Selenium needed for development only, so no use to install it on AWS instance.

### Some useful commands and tips:

When toggling debug to False and setting allowed hosts - add `www.` as well.
Furthermore, if after:
>$ sudo systemctl daemon-reload <br>
$ sudo systemctl enable gunicorn-$SITENAME <br>
$ sudo systemctl start gunicorn-$SITENAME <br>

If the response is `502 BAD GATEWAY`, try:
> $ sudo systemctl reload nginx <br>
> $ sudo systemctl restart (the service here)

The pattern of a working tree on AWS instance is available in nginx.template.conf. <br>

#### To auto-amend patterns with stream editor use:
For nginx:
> $ sed "s/SITENAME/app.paul-michelle.art/g" /home/ubuntu/sites/app.paul-michelle.art/source/deploy_tools/nginx.template.conf
> | sudo tee /etc/nginx/sites-available/app.paul-michelle.art

Then to create a link in enabled-sites:
> $ sudo ln -s /etc/nginx/sites-available/app.paul-michelle.art /etc/nginx/sites-enabled/app.paul-michelle.art

For gunicorn system settings:
> $ sed "s/SITENAME/app.paul-michelle.art/g" /home/ubuntu/sites/app.paul-michelle.art/source/deploy_tools/gunicorn-systemd.template.service 
> | sudo tee /etc/systemd/system/gunicorn-app.paul-michelle.art.service

#### Set of commands to launch gunicorn:

> $ sudo systemctl daemon-reload <br>
> $ sudo systemctl reload nginx <br>
> $ sudo systemctl enable sudo gunicorn-app.paul-michelle.art 
> (put the exact service name from above)<br>
> $ sudo systemctl start gunicorn-app.paul-michelle.art <br>

Again, if the response is `502 BAD GATEWAY`, restart both services:
> $ sudo systemctl restart (the service here)