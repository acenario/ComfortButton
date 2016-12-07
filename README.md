# Comfort Button

Made with ♥ by Arjun Bhatnagar

This project is a self-contained flask project that launches ngrok and is able to open a file/url when a page is hit. The goal is to launch a video to calm me down when I have an anxiety or panic attack, or when I am absolutely miserable.

> My fiancé passed away recently and life has been so difficult.
> Every day is so tough and I have lost all joy in life.
> The only times I have smiled for more than a few seconds are when
> I see my love. She was so pure, beautiful, and wonderful.
> --Arjun Bhatnagar

The project accompanies a physical *"comfort button"* created by my friend [Nicholas Francisci] [Nick]. The button contains a "photon" board that sends a web request to the flask server running.

[![N|Solid](http://i.imgur.com/WRHORqam.jpg?1)](https://irajaan.com)    [![N|Solid](http://i.imgur.com/2ij2ZTpm.jpg)](https://irajaan.com)

### Installation

Download the project from Github.

```sh
$ git clone https://github.com/acenario/ComfortButton
```

Comfort Button requires ngrok added to path, or for it to be in your directory. 

Download and extract the [latest version of ngrok][ngrok] and add it to PATH.

Or run these commands (Mac & Linux Users) where you downloaded ngrok.

```sh
$ unzip path/to/ngrok.zip
$ cp ngrok /usr/local/bin/ngrok
```

You can either install in a virtualenv or install globally. You can also checkout the venv branch if you do not want to install virtualenv.

```sh
$ cd ComfortButton
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ python manage.py startbutton
```
You will be asked some configuration details, leave the defaults but change the subdomain to match the configured ComfortButton's url.

#### Interesting Features

This project has some interesting classes that I wrote. I wrote a self-contained ngrok manager and hooked any flask request to open either a file or a url.

I wrote some commands to go along with the classes and can be run independently. 

Running the main project
```sh
$ python manage.py startbutton
```

Running just the flask server
```sh
$ python manage.py runserver
```

Running just ngrok tunnel
```sh
$ python manage.py startngrok
```

Opening the configured video/file
```sh
$ python manage.py openvideo
```

Manually killing existing ngrok processes 
```sh
$ python manage.py killngrok
```

#### Example Config

When you run for the first time, it will generate a config. Here is a sample config.

```sh
[ngrok]
active = False
current_url = none
use_config = False 
tunnel = http
port = 5000 
auth = none 
subdomain = arjunandira 

[button]
primary_video = http://www.yourepeat.com/watch?v=99td8AsSkfQ
```

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [Nick]: <https://github.com/ManickYoj>
   [ngrok]: <https://ngrok.com/download>

