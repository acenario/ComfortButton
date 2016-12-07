class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[36m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def get_question_string(str_input):
        return bcolors.OKBLUE + str_input + bcolors.ENDC

    @staticmethod
    def get_ok_string(str_input):
        return bcolors.OKGREEN + str_input + bcolors.ENDC

    @staticmethod
    def get_fail_string(str_input):
        return bcolors.FAIL + str_input + bcolors.ENDC

    @staticmethod
    def get_bold_string(str_input):
        return bcolors.BOLD + str_input + bcolors.ENDC

    @staticmethod
    def get_underline_string(str_input):
        return bcolors.UNDERLINE + str_input + bcolors.ENDC