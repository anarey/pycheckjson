import json


def proccess_msg(blacklist, expected_values, message):
    result = 0
    cleaned_message =  "".join(message.split(" "))

    ## No puede haber elememtos de blacklist.
    for elem in blacklist:
        if elem in cleaned_message:
            return -1

    for key in expected_values.keys():
        value = expected_values[key]
        ##import ipdb; ipdb.set_trace();
        msg_search = "\"%s\":\"%s\"" % (key, value)
        print "Campo que buscamos: %s" % (msg_search)
        print "Texto: %s" % (cleaned_message)
        if (cleaned_message.find(msg_search) == -1):
            print ("No lo encuentro")
            return -1    

    return result

def main():
	print "Recorro la plantilla"

	theme_file = open('themes/theme-example.json')
	json_dic = json.load(theme_file)
	message_json = "{\"bytes\": \"10\", \"pkts\": \"5\", \"type\": \"netflowv9\", \"l4_proto\": \"17\", \"tcp_flags\": \"0\", \"output_snmp\":\"2222\"}"

	for msj_theme in json_dic:
	    msg = json_dic[msj_theme][0]
	    if len(msg.keys()) == 2 and "blacklist" in msg.keys() and "expected_values" in msg.keys():
	        blacklist = msg[u'blacklist']
	        expected_values = msg[u'expected_values']
	        result = proccess_msg(blacklist, expected_values, message_json)

	        if result == 0:
	            print "message found"
	            break
	        else:
	            print "sigo buscando con la siguiente plantilla"

	        for elem in blacklist:
	        	print elem
	##        for elem in blacklist:
	 ##       	print elem

	        print  expected_values

	if result != 0:
		print "We do not found the message"
	print "fin"


	theme_file.close()

if __name__ == '__main__':
    main()

## message_json = "{\"bytes\": 10, \"pkts\": 5, \"type\": \"netflowv9\", \"l4_proto\": 17, \"tcp_flags\": 0}"