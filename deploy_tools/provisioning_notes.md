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

the response if 502 BAD GATEWAY, try:
> $ sudo systemctl reload nginx

The pattern of a working tree on AWS instance is available in nginx.template.conf. 