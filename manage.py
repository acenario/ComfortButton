from flask_script import Server, Manager, prompt, prompt_bool
from app import app
from colors import bcolors
from ngrok import NgrokTunnel
import ConfigParser
import psutil
import sys
import os
import io

manager = Manager(app)
manager.add_command("runserver", Server())

ngrok_tunnel = None

def loadngrok():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    tunnels = ["http",
                "tls",
                "tcp"
    ]
    tunnel = config.get('ngrok', 'tunnel').lower()
    port = config.get('ngrok', 'port').lower()
    auth = config.get('ngrok', 'auth').lower()
    subdomain = config.get('ngrok', 'subdomain').lower()
    if auth == "none":
        auth = None

    global ngrok_tunnel
    ngrok_tunnel = NgrokTunnel(tunnel,port,auth,subdomain)
    tunnel_url = ngrok_tunnel.start()
    active_ngrok = True

    config.set('ngrok', 'active', True)
    config.set('ngrok', 'current_url', tunnel_url)

    print "\n"
    print bcolors.get_question_string("=== STARTED NGROK ===")
    print bcolors.get_ok_string("Tunneling: " + tunnel + " " + port)
    print bcolors.get_ok_string("To: ") + bcolors.get_ok_string(bcolors.get_underline_string(tunnel_url))
    print bcolors.get_ok_string("View live requests: ") + bcolors.get_ok_string(bcolors.get_underline_string("http://localhost:4040"))
    print bcolors.get_underline_string("Press Ctrl + C to exit")
    print bcolors.get_question_string("=== STARTED NGROK ===")

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    while active_ngrok:
        pass

def askngrok():
    tunnels = ["http",
                "tls",
                "tcp"
    ]
    tunnel = prompt(bcolors.get_question_string("What tunnel you would like to run?"), default="http").lower()
    while tunnel not in tunnels:
        print bcolors.get_fail_string("Incorrect tunnel: " + tunnel)
        tunnel = prompt(bcolors.get_question_string("What tunnel you would like to run?"), default="http").lower()
    
    port = prompt(bcolors.get_question_string("What port you would like to run on?"), default="8000").lower()
    while not port.isdigit():
        print bcolors.get_fail_string("Incorrect port: " + port)
        port = prompt(bcolors.get_question_string("What port you would like to run on?"), default="8000").lower()
    auth = prompt(bcolors.get_question_string("What is your auth token?"), default="None").lower()
    if auth == "none":
        auth = None
    subdomain = prompt(bcolors.get_question_string("What subdomain would you like to run?"), default="pineapplepen").lower()
    global ngrok_tunnel
    ngrok_tunnel = NgrokTunnel(tunnel,port,auth,subdomain)
    tunnel_url = ngrok_tunnel.start()
    active_ngrok = True

    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    #Config
    config.set('ngrok', 'active', True)
    config.set('ngrok', 'current_url', tunnel_url)
    config.set('ngrok', 'tunnel', tunnel)
    config.set('ngrok', 'port', port)
    if not auth:
        config.set('ngrok', 'auth', 'none')
    else:
        config.set('ngrok', 'auth', auth)
    config.set('ngrok', 'subdomain', subdomain)

    print "\n"
    print bcolors.get_question_string("=== STARTED NGROK ===")
    print bcolors.get_ok_string("Tunneling: " + tunnel + " " + port)
    print bcolors.get_ok_string("To: ") + bcolors.get_ok_string(bcolors.get_underline_string(tunnel_url))
    print bcolors.get_ok_string("View live requests: ") + bcolors.get_ok_string(bcolors.get_underline_string("http://localhost:4040"))
    print bcolors.get_underline_string("Press Ctrl + C to exit")
    print bcolors.get_question_string("=== STARTED NGROK ===")

    with open('config.ini', 'w') as configfile:
        config.write(configfile)   

    while active_ngrok:
        pass

@manager.command
def createconfig():
    # Check if there is already a configurtion file
    configfile_name = "config.ini"
    if not os.path.isfile(configfile_name):
        # Create the configuration file as it doesn't exist yet
        cfgfile = open(configfile_name, 'w')

        # Add content to the file
        Config = ConfigParser.ConfigParser()
        Config.add_section('ngrok')
        Config.set('ngrok', 'active', False)
        Config.set('ngrok', 'current_url', 'none')
        Config.set('ngrok', 'use_config', False)
        Config.set('ngrok', 'tunnel', 'http')
        Config.set('ngrok', 'port', '8000')
        Config.set('ngrok', 'auth', 'none')
        Config.set('ngrok', 'subdomain', 'pineapplepen')
        
        Config.add_section('button')
        Config.set('button', 'primary_video', "~/Desktop/IRA_PERF.MOV")

        Config.write(cfgfile)
        cfgfile.close()

        print bcolors.get_ok_string("Config successfully created!")
    else:
        print bcolors.get_fail_string("Config already exists!")

@manager.command
def killngrok():
    for proc in psutil.process_iter():
        if proc.name() == "ngrok":
            proc.kill()
            print bcolors.get_fail_string("Killed existing ngrok process!")

@manager.command
def startngrok():
    killngrok()
    configfile_name = "config.ini"
    if not os.path.isfile(configfile_name):
        createconfig()
        askngrok()
    else:
        config = ConfigParser.ConfigParser()
        config.read('config.ini')

        use_config = config.getboolean("ngrok", "use_config")

        if not use_config:
            if prompt_bool(bcolors.get_question_string("Would you like to load from config?")):
                config.set('ngrok', 'use_config', True)
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                loadngrok()
            else:
                askngrok()
        else:
            loadngrok()
            

    

@manager.command
def startbutton():
    print "\n"
    killngrok()
    app.run()


if __name__ == "__main__":
    try:
        manager.run()
    except KeyboardInterrupt:
        print "\n"
        print bcolors.get_bold_string("=== TERMINATED PROGRAM ===")
        print bcolors.get_underline_string("Interrupted program exit")
        if ngrok_tunnel:
            ngrok_tunnel.stop()
            ngrok_tunnel = None

            config = ConfigParser.ConfigParser()
            config.read('config.ini')

            config.set('ngrok', 'active', False)
            config.set('ngrok', 'current_url', "none")

            with open('config.ini', 'w') as configfile:
                config.write(configfile)


            print bcolors.get_underline_string("Successfully terminated ngrok")
        print bcolors.get_bold_string("===    PROGRAM EXIT    ===")
        print "\n"

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)