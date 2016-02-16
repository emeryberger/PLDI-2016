# prefs-checker.py: prints sorted list of # of bids (prefs) placed per reviewer
# Author: Emery Berger <emery.berger@gmail.com>
# Released into the public domain.

count = {}

import csv
with open('pldi16-allprefs.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        # print row['paper'],' ',row['email'],':',row['preference'],row['expertise']
        score = row['preference']+row['expertise']
        # print score
        key = row['email']
        if (score != ''):
            if key in count:
                count[key] += 1
            else:
                count[key] = 1

z = sorted(count.items(), key=lambda x:x[1])
for i in z:
    print i[0], ":", i[1]


