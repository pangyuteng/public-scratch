import os
import datetime
import json

json_file = 'static/expiration-dates.json'

with open('tmp/vix-expiration-usethis.txt','r') as f:
    line_list = [x for x in f.read().split("\n") if len(x)>0]
mylist = []
for x in line_list:
    try:
        tstamp = datetime.datetime.strptime(x,"%d %B %Y")
        tstamp_str = tstamp.strftime("%Y-%m-%d")
        # if tstamp.month in [3,6,9,12]:
        #     if tstamp.day > 20:
        #         print(tstamp_str)
        mylist.append(tstamp_str)
    except:
        print(x)

if not os.path.exists(json_file):
    with open(json_file,'w') as f:
        f.write(json.dumps(mylist))
    print('done')
else:
    print("skip")