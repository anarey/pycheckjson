import json
from types import *
import argparse
import signal
import sys
import fileinput

signal_received = 0

def print_use():
    print "usage: checkjson.py [-h] [path/to/file.t]"
    print "positional arguments:"
    print "  path/to/file.t  Check the json message with this theme."
    print "optional arguments:"
    print "  -h, --help      show this help message and exit"

def exist_msg(blacklist, expected_values, message):
    result = 0
    cleaned_message =  "".join(message.split(" "))

    for elem in blacklist:
        if elem in cleaned_message:
            return -1

    for key in expected_values.keys():
        value = expected_values[key]
        msg_search = ""

        if type(value) is IntType or type(value) is LongType:
            msg_search = "\"%s\":%d" % (key, value)
        elif type(value) is StringType or type(value) is UnicodeType:
            msg_search = "\"%s\":\"%s\"" % (key, value)
        elif type(value) is BooleanType:
            msg_search = "\"%s\":\"%s\"" % (key, value)

        if (cleaned_message.find(msg_search) == -1):
            return -1

    return 0


def lookfor_msg(json_dic, message_json):
    for msg_theme in json_dic:
        msg = json_dic[msg_theme][0]
        if len(msg.keys()) == 2 and "blacklist" in msg.keys() and "expected_values" in msg.keys():
            blacklist = msg[u'blacklist']
            expected_values = msg[u'expected_values']
            result = exist_msg(blacklist, expected_values, message_json)

            if result == 0:
                return msg_theme
    return ""


def preexec():
    os.setpgrp()  # Don't forward signals.


def signal_handler(signal, frame):
    global signal_received
    signal_received = 1


def main():

    parser = argparse.ArgumentParser(description='Check json file.')
    parser.add_argument('filename', nargs='?',
                        metavar='path/to/file.t',
                        help='Check the json message with this theme.')
    args, unk = parser.parse_known_args()

    if args.filename:
        try:
            theme_file = open(args.filename)
        except EOFError:
            print "Cannot open log file %s" % (args.filename)
            return
    else:
        print("Error: No template files to run.")
        print_use()
        return

    json_dic = {}
    json_dic = json.load(theme_file)
##    message_json = "{\"bytes\": \"10\", \"pkts\": \"5\", \"type\": \"netflowv9\", \"l4_proto\": \"17\", \"tcp_flags\": \"0\", \"output_snmp\":\"2222\"}"
    theme_file.close()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    key_delete = ""
    result = 0
    tofound = len(json_dic)
    error = 0
    final = False

    i =0
    ##while (signal_handler != 1 or final == False): ## TODO: Or not more messages
    for line in fileinput.input(unk):
        i = i +1
        message_json = line
        if signal_received == 1:
            print "\nSignal received. Cleaning up and Exitting..."
            ##cleanup_on_exit()
            ##return result
            sys.exit(-1)
        if len(json_dic) == 0:
            error = error + 1
            print "Error: Number of json messages > Number of template files."
            break

        key_delete = lookfor_msg(json_dic, message_json)

        if len(key_delete) > 0:
            del(json_dic[key_delete])
            key_delete = ""
        else:
            error = error + 1

    if len(json_dic) > 0 or error > 0:
        print "Test failed."
        if error > 0:
            print "There are %d errores." % (error)
        else:
            print "Error: There is a problem."
            result = -1

        if len(json_dic) > 0:
            print "The following message are not received:"
            print json_dic
        result = -1
    else:
        print "Test passed."
      ##  final = True

    return result

if __name__ == '__main__':
    main()

## message_json = "{\"bytes\": 10, \"pkts\": 5, \"type\": \"netflowv9\", \"l4_proto\": 17, \"tcp_flags\": 0}"