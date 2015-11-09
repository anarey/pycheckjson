import json
from types import *

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
                print "message found"
                return msg_theme
    return ""



def main():
    print "Check all themes"

    json_dic = {}
    theme_file = open('themes/theme-example.json')
    json_dic = json.load(theme_file)
##    message_json = "{\"bytes\": \"10\", \"pkts\": \"5\", \"type\": \"netflowv9\", \"l4_proto\": \"17\", \"tcp_flags\": \"0\", \"output_snmp\":\"2222\"}"
    theme_file.close()

    message_json = "{\"bytes\": 10, \"pkts\": 5, \"type\": \"netflowv9\", \"l4_proto\": 17, \"tcp_flags\": 0,}"
    key_delete = ""
    result = 0
    tofound = len(json_dic)
    error = 0
    key_delete = lookfor_msg(json_dic, message_json)


    if len(key_delete) > 0:
        print "We delete the message of the batch of themes:  %s" % (json_dic[key_delete])
        del(json_dic[key_delete])
        tofound = tofound - 1
    else:
        error = 0
        print("Mensaje no encontrado")


    if len(json_dic) > 0:
        print "Themes are not deleted: \n %s" % (json_dic)

    if len(json_dic) > 0 or error > 0 or tofound > 0:
        print "Test no pasted"
        result = -1
    else:
        print "Test passed"

    return result

if __name__ == '__main__':
    main()

## message_json = "{\"bytes\": 10, \"pkts\": 5, \"type\": \"netflowv9\", \"l4_proto\": 17, \"tcp_flags\": 0}"