import os
import time
import uuid
import logging
import subprocess
from distutils.spawn import find_executable
from colors import bcolors


logger = logging.getLogger(__name__)


class NgrokTunnel:

    def __init__(self, tunnel, port, auth_token=None, subdomain_base="pineapplepen", gen_random=False):
        """Initalize Ngrok tunnel.

        :param auth_token: Your auth token string you get after logging into ngrok.com

        :param port: int, localhost port forwarded through tunnel

        :parma subdomain_base: Each new tunnel gets a generated subdomain. This is the prefix used for a random string.
        """
        assert find_executable("ngrok"), "ngrok command must be installed, see https://ngrok.com/"
        self.port = port
        self.auth_token = auth_token
        self.tunnel = tunnel
        if gen_random or subdomain_base == "pineapplepen":
            self.subdomain = "{}-{}".format(subdomain_base, str(uuid.uuid4()))
        else:
            self.subdomain = "{}".format(subdomain_base)

    def start(self, ngrok_die_check_delay=0.5):
        """Starts the thread on the background and blocks until we get a tunnel URL.

        :return: the tunnel URL which is now publicly open for your localhost port
        """

        logger.debug("Starting ngrok tunnel %s for port %d", self.subdomain, self.port)
        f = open(os.devnull, 'w')

        if self.auth_token:
            self.ngrok = subprocess.Popen(["ngrok",
                                        str(self.tunnel), 
                                        "-authtoken={}".format(self.auth_token), 
                                        "-log=stdout", 
                                        "-subdomain={}".format(self.subdomain), 
                                        str(self.port)], stdout=f)
        else:
            self.ngrok = subprocess.Popen(["ngrok",
                                    str(self.tunnel), 
                                    "-log=stdout", 
                                    "-subdomain={}".format(self.subdomain), 
                                    str(self.port)], stdout=f)

        # See that we don't instantly die
        time.sleep(ngrok_die_check_delay)
        assert self.ngrok.poll() is None, bcolors.get_fail_string("ngrok terminated abrutly due to an error")
        url = "https://{}.ngrok.io".format(self.subdomain)
        return url

    def stop(self):
        """Tell ngrok to tear down the tunnel.

        Stop the background tunneling process.
        """
        self.ngrok.terminate()