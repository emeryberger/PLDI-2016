# conflict-pcprefs.py:
#   - used to generate file for David Walker's scripts, which were not used
# Author: Emery Berger <emery.berger@gmail.com>
# Released into the public domain.

import csv
import random
import sys

# A map of e-mail to names
# names[e-mail] = name

names = {}
with open('pldi16-users.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        key = row['email'].lower()
        value = row['first'] + " " + row['last']
        names[key] = value

with open('pldi16-authors.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        key = row['email'].lower()
        if (not (key in names)):
            value = row['name']
            names[key] = value

# Find (heavy) PC members.

heavypc = {}

with open('pldi16-pcinfo.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        email = row['email'].lower()
        tags = row['tags'].lower()
        if ("heavy" in tags):
            heavypc[email] = 1 # add to map


# Now we build a list of authors for each paper.
# allAuthors[paper number] = list of authors (by e-mail)

allAuthors = {}
with open('pldi16-authors.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        key = row['paper']
        value = row['email'].lower()
#        value = names[value]
        if key in allAuthors:
            allAuthors[key].append(value)
        else:
            allAuthors[key] = [value]

#
# Now read in the conflicts.
# conflicts[e-mail] = everyone who is on a paper with a stated conflict with e-mail
#

conflicts = {}
conflictPapers = {}

with open('pldi16-pcconflicts.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        key = row['PC email']
        value = list(set(allAuthors[row['paper']]))
        # print row['paper'], key, value
        # print key, value
        if (key in conflicts):
            conflicts[key].append(value)
        else:
            conflicts[key] = [value]
        if (key in conflictPapers):
            conflictPapers[key].append(row['paper'])
        else:
            conflictPapers[key] = [row['paper']]


# Now read in prefs, which we will output with conflicts as -100.
# If ...

with open('pldi16-allprefs.csv','rb') as csvfile:
    heavypc_set = set(heavypc.keys())
    reader = csv.DictReader(csvfile,delimiter=',')
    with open('/dev/stdout','wb') as output:
        fieldnames = ['paper','title','name','email','preference','conflict']
        writer = csv.DictWriter(output,delimiter=',',fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            paper       = row['paper']
            title       = row['title']
            name        = row['name']
            email       = row['email'].lower()
            preference  = row['preference']
            if (preference == ''):
                preference = '0'
            expertise   = row['expertise']
            if (expertise == ''):
                expertise = 'Z'
            preference = preference + expertise
            # topic_score = row['topic_score']
            conflict    = row['conflict']
            # If this paper was written by a heavy PC member,
            # and the person in question is a heavy PC member,
            # add a conflict.
            conflict = 'nobody@nowhere.nowhow'
            if (set(allAuthors[paper]) & heavypc_set):
                if (email in heavypc_set):
                    # preference = -100
                    # expertise = 'Z'
                    conflict = email
            writer.writerow({ 'paper' : paper,
                              'title' : title,
                              'name' : name,
                              'email' : email,
                              'preference' : preference,
                              'conflict' : conflict })

