import ConfigParser
import os 

def get_current_primary_path():
    configfile_name = "config.ini"
    if not os.path.isfile(configfile_name):
        return "~/Desktop/IRA_PERF.MOV"
    else:
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        path = config.get('button', 'primary_video')
        return path
        
    