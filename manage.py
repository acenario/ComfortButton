from flask_script import Server, Manager, prompt
from app import app
from colors import bcolors
from ngrok import NgrokTunnel
import yaml
import sys
import os

manager = Manager(app)
manager.add_command("runserver", Server())

ngrok_tunnel = None

@manager.command
def createconfig():
    with open("config.yml", 'r+') as ymlfile:
        cfg = yaml.load(ymlfile)
        default_dict = {
            "ngrok": [
                {"port" : "8000"},
                {"url": "url"}
            ],
            "button": [
                {"active" : False},
                {"video1" : "~/Desktop/IRA_PERF.MOV"}
            ]
        }
        yaml.dump(default_dict, ymlfile)


@manager.command
def startngrok():
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
    print "\n"
    print bcolors.get_question_string("=== STARTED NGROK ===")
    print bcolors.get_ok_string("Tunneling: " + tunnel + " " + port)
    print bcolors.get_ok_string("To: ") + bcolors.get_ok_string(bcolors.get_underline_string(tunnel_url))
    print bcolors.get_ok_string("View live requests: ") + bcolors.get_ok_string(bcolors.get_underline_string("http://localhost:4040"))
    print bcolors.get_underline_string("Press Ctrl + C to exit")
    print bcolors.get_question_string("=== STARTED NGROK ===")
    while active_ngrok:
        pass

@manager.command
def startbutton():
    print "\n"
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
            print bcolors.get_underline_string("Successfully terminated ngrok")
        print bcolors.get_bold_string("===    PROGRAM EXIT    ===")
        print "\n"

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)