import ConfigParser
import os 
import threading
from colors import bcolors

def get_current_primary_path():
    configfile_name = "config.ini"
    if not os.path.isfile(configfile_name):
        return "/Users/Arjun/Desktop/IRA_PERF.MOV"
    else:
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        path = config.get('button', 'primary_video')
        return path

def open_file(file_or_url):
    import webbrowser
    if (not file_or_url.startswith(('http'))):
        file_or_url = "file:" + file_or_url
    webbrowser.open_new_tab(file_or_url)       


def load_primary_video():
    path = get_current_primary_path()
    print bcolors.get_ok_string("\nCurrent primary video: " + bcolors.get_underline_string(path))
    
    #opens files or urls
    open_file(path) 
    