#!/usr/bin/env python

"""
original:
https://github.com/mikewilks/simple-pastebin-monitor/blob/master/simple-pb-monitor.py

Ewald 20190721
added pushover support
"""

import requests, time, sys, os

from pushover import Client
# specify Pushover api_token and user_key in ~/.pushoverrc
po = Client()

# Check for command line parameters for the keywords file and output directory
# Start with defaults of ./keywords.txt and .

# Start with defaults
keyword_file = './keywords.txt'
output_path = './FOUND'
check_ip = True

# keywords file as the first argument after the python file
if len(sys.argv) > 1 :
    keyword_file = (sys.argv)[1]

# output directory as the second parameter after the python file
if len(sys.argv) > 2 :
    output_path = (sys.argv)[2]

# Turn on the check for non-authed IP
if len(sys.argv) > 3 :
    if 'True' in (sys.argv)[3] :
        check_ip = True

# Load the keywords
with open(keyword_file) as f:
    keywords = f.read().splitlines()

mess = "scanning for: %s " % (keywords)
#print ("scanning for:",keywords)
print (mess)
po.send_message(mess, title="Pastebin", priority=0)

check_index = 0
check_list = []

while True :

    # get the jsons from the scraping api, limit can be up to 250 items
    r = requests.get("https://scrape.pastebin.com/api_scraping.php?limit=100")

    # Added a debug statement if the API is not authed, it has to be enabled through the params though to stop
    # pastes containing the text causing false positives (especially as the response code is 200 regardless)
    if check_ip :
        if ("DOES NOT HAVE ACCESS")  in (str)(r.content) :
           print (r.content)
           exit (-1)

    # if it was successful parse
    if r.status_code == 200 :

        # get json from the response
        parsed_json = r.json()

        # loop through the entries
        for individual in parsed_json :
            # Now get the actual pastes if it is not in the last 1000 check_list
            if individual['key'] not in check_list :
                p = requests.get (individual['scrape_url'])
                if p.status_code == 200 :
                    text = p.text
                    # loop through the keywords to see if they are in the post
                    for word in keywords :
                        if word.lower() in text.lower() :
                            mess = 'Matched keyword \'{}\' and will save {}'.format(word, individual['key'])
                            print (mess)
                            po.send_message(mess, title="Pastebin Hit", priority=1)

                            # Check whether the directory with the name of the keyword exists and create it if not
                            if not os.path.isdir (output_path+'/'+word) :
                                # Create the directory
                                os.mkdir (output_path+'/'+word)

                            # Save to current dir using the key as the filename
                            file_object = open(output_path+'/'+word+'/'+individual['key'], 'w')
                            file_object.write(text)
                            file_object.close()

                         # Removed the break because we do want to save multiple times if multiple keywords are
                         # matched because we now have a directory per key word '''

                    # Add to the checklist of the last 1000 so we don't fetch unnecessarily
                    if check_index == 999:
                        print("Reseting the checklist counter")
                        check_index = 0
                    # at the key to the last 1000 check_list and increment the counter
                    check_list.insert(check_index,individual['key'])
                    check_index = check_index + 1
            # enable the next two lines if you want debug info
            # else :
                # print ("Skipping {}, already processed".format(individual['key']))

    else :
        print ("There was an error calling the url")

    # wait a minute
    # print ("Sleeping a minute")
    time.sleep(60)
