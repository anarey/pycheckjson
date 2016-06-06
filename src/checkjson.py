import json
from types import *
import argparse
import signal
import sys
import fileinput
import os.path
import logging
import logging.handlers

signal_received = 0


def print_use():
    print ""
    print "checkjson.py [-h] [-t path/to/file.t] [-j path/to/file.t]"
    print "positional arguments:"
    print "    -t path/to/file.t, --template path/to/file.t"
    print "        Use this template json file."
    print "    -j path/to/file.t, --json_file path/to/file.t"
    print "        Check this json message with this template."
    print "optional arguments:"
    print "  -d, --debug     Enable debugging mode"
    print "  -h, --help      show this help message and exit"

def exist_msg(blacklist, expected_values, message, tmp_log):
    result = 0
    cleaned_message = "".join(message.split(" "))

    for elem in blacklist:
        if elem in cleaned_message:
            print "Looking for backlist element into cleaned_message"
            return -1

    for key in expected_values.keys():
        value = expected_values[key]
        msg_search = ""

        if type(value) is IntType or type(value) is LongType:
            msg_search = "\"%s\":%d" % (key, value)
        elif type(value) is StringType or type(value) is UnicodeType:
            value = "".join(value.split(" "))
            msg_search = "\"%s\":\"%s\"" % (key, value)
        elif type(value) is BooleanType:
            msg_search = "\"%s\":%s" % (key, value)

        if debug_option:
            print "Exist_msg: El mensaje es: " + str(msg_search)

        if (cleaned_message.find(msg_search) == -1):
            tmp_log = tmp_log + msg_search
            return -1

    return 0


def lookfor_msg(json_dic, message_json):
    log_tmp = ""
    for msg_template in json_dic:
        msg = json_dic[msg_template][0]
        if len(msg.keys()) == 2 and "blacklist" in msg.keys() and "expected_values" in msg.keys():
            blacklist = msg[u'blacklist']
            expected_values = msg[u'expected_values']
            result = exist_msg(blacklist, expected_values, message_json, log_tmp)
            if result == 0:
                if debug_option:
                    print "Hay una plantilla que cumple con ese mensaje. Elimino el elemento de la plantilla."
                ##del json_dic["msg_template"]
                return msg_template

    logging.debug(log_tmp)
    print "No hay plantilla que haga maching con " + str(message_json)
    return ""


def init_logger(log_file, log_path, log_name):
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    log_size = 2097152
    handler = logging.handlers.RotatingFileHandler(filename=log_path+log_file,
                                                   mode='a',
                                                   maxBytes=log_size,
                                                   backupCount=5)

    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.debug('Creating the log file.')
    return logger


def preexec():
    os.setpgrp()  # Don't forward signals.


def signal_handler(signal, frame):
    global signal_received
    signal_received = 1


def main():

    parser = argparse.ArgumentParser(description='Check json file.')
    parser.add_argument('-t', '--template',
                        metavar='path/to/file.t',
                        help='Use this template json file.')
    parser.add_argument('-j', '--json_file',
                        metavar='path/to/file.t',
                        help='Check this json message with this template.')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug',
                        help='Enable debugging mode')

    args = parser.parse_args()

    if args.template:
        try:
            template_file = open(args.template)
        except EOFError:
            print "Cannot open log file %s" % (args.template)
            return
    else:
        print("Error: No template files to run.")
        print_use()
        return

    if args.json_file:
        if os.path.isfile(args.json_file):
            json_file = args.json_file
        else:
            print "Error: %s is not an existing json file." % (args.json_file)
            print_use()
            return
    else:
        print("Error: No json files to run. You have to add a json file to check")
        print_use()
        return

    PATH = os.path.abspath(os.path.dirname(__file__))
    LOG_CHANGES = "diffences_json.log"
    logger = init_logger(LOG_CHANGES, "./", "diff")

    global debug_option
    debug_option = args.debug


    json_dic = {}
    json_dic = json.load(template_file)
    template_file.close()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    key_delete = ""
    result = 0
    tofound = len(json_dic)
    error = 0

    i = 0
    for line in fileinput.input(json_file):
        i = i + 1
        message_json = line
        if signal_received == 1:
            result = -1
            print "\nSignal received. Cleaning up and Exitting..."
            break
        if len(json_dic) is 0:
            error = error + 1
            print "Error: Number of json messages > Number of template files."
            break
        logger.debug("Analysing this mensaje into template: " + str(message_json))
        logger.debug("This is the template json: " + str(json_dic))

        key_delete = lookfor_msg(json_dic, message_json)

        if len(key_delete) > 0:
            logger.debug("Delete this entry " + str(key_delete))
            if debug_option:
                print "key_delete " + str(key_delete)
            del(json_dic[key_delete])
            key_delete = ""
        else:
            logger.debug("We did not find a template for the json message")
            logger.debug("json_message: " + str(message_json))
            error = error + 1

    if signal_received == 1:
        print "Test failed."
        sys.exit(result)

    if len(json_dic) > 0 or error > 0:
        print "Test failed."
        if error > 0:
            print "There are %d errors." % (error)
        else:
            print "Error: There is a problem."
            result = -1

        if len(json_dic) > 0:
            print "The following message are not received:"
            print json_dic
        result = -1
    else:
        print "Test passed."

    sys.exit(result)

if __name__ == '__main__':
    main()
