# extract-json-ecoop.py: converts JSON files (as exported from ECOOP) into .csv format
#   - used for checking for simultaneous submission to ECOOP & PLDI.
# Author: Emery Berger <emery.berger@gmail.com>
# Released into the public domain.

import json
import sys

s = sys.stdin.read()

q = json.loads(s)

print "paper,title,email"
for i in range(0,len(q)):
    w = q[i]
    for e in w['authors']:
        if 'email' in e.keys():
            print '{2},"{0}",{1}'.format(w['title'].encode('ascii','ignore'),
                                         e['email'],
                                         w['id'])


# print json.dumps(q, sort_keys=True, indent=4, separators=(',', ': '))

# print q

