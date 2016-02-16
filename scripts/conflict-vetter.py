# conflict-vetter.py: finds all stated conflicts from authors and mails them for vetting to reviewers
#   - used for checking for bogus conflicts / conflict engineering.
# Author: Emery Berger <emery.berger@gmail.com>
# Released into the public domain.

import csv
import random
import smtplib

# Change to True to really send mail
reallySendMail = False

senderFirstName = "Me"
senderName = "Your Name <your.mail.goes.here@gmail.com>"
sender = "your.mail.goes.here@gmail.com"
password = "your-onetime-password-goes-here"

# A map of e-mail to names
# names[e-mail] = name

names = {}
with open('pldi16-pcinfo.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        key = row['email'].lower()
        value = row['first'] + " " + row['last']
        names[key] = value


# Now we build a list of authors for each paper.
# allAuthors[paper number] = list of authors (by e-mail)

allAuthors = {}
with open('pldi16-authors.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        key = row['paper']
        value = row['email']
        if key in allAuthors:
            allAuthors[key].append(value)
        else:
            allAuthors[key] = [value]

#
# Now read in the conflicts.
# conflicts[e-mail] = everyone who is on a paper with a stated conflict with e-mail
#

conflicts = {}

with open('pldi16-pcconflicts.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        key = row['PC email']
        value = list(set(allAuthors[row['paper']]))
        if (key in conflicts):
            conflicts[key].append(value)
        else:
            conflicts[key] = [value]

# Shuffle paper order.
for k in conflicts:
    random.shuffle(conflicts[k])

# Now, we read in all authors.
# We will use this to add noise to the potential conflicts.

authorsList = []
with open('pldi16-authors.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for row in reader:
        key = row['name']
        value = row['email']
        authorsList.append(value)


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)

if (True):
    s = sorted(conflicts.keys())
    msg = ""
    for recipient in s:
        msg = "From: " + senderName + "\nSubject: Conflicts to vet: "
        if (recipient.lower() in names):
            msg += names[recipient.lower()]
        else:
            msg += recipient
        msg += "\n\nHi,\n\n"
        msg += "This mail contains a list of all papers for which you have been marked\nas a conflict. The paper numbers are not given, and they are shuffled.\nPlease check each author list to verify that at least one of the authors for\neach paper looks like a legitimate conflict. If not, please send me\na mail.\n\n"
        # Not actually sampling from random authors right now.
        # r = random.sample(authorsList,5)
        c = conflicts[recipient]
        ind = 1
        for l in c:
            msg += "Paper " + str(ind) + " : "
            i = 0
            for k in l:
                msg += str(k)
                i += 1
                if (i != len(l)):
                    msg += ", "
                else:
                    msg += "."
            msg += "\n"
            ind += 1
        msg += "\n\nThanks,\n" + senderFirstName + "\n"
        print "Sending mail to " + recipient + "..."
        if (reallySendMail):
            server.sendmail(sender, recipient, msg)
        else:
            print "NOT REALLY SENDING IT."
            print msg

server.quit()
