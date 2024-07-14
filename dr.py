import sys
import csv
import re

# +-----------+------------------------------------------------------
# | Algorithm |
# +-----------+

#   For each entry in the submissions
#     Grab the "Designated Reviewer" column
#     Split into lines (I think)
#     For each line
#       If it contains an ORCID
#         Check to see if it's in the list of reviewer applications
#       If it contains an email address
#         Check to see if it's in the list of reviewer applications
#       If it contains "None" (or some variant)
#         Tag it as a "None"
#       If it contains text
#         Look for the name

# +----------+-------------------------------------------------------
# | Settings |
# +----------+

DR_NUMBER_COLUMN = 0
DR_TITLE_COLUMN = 2
DR_DR_COLUMN = 11

VOL_ORCID_COLUMN = 4

ORCID_PATTERN = "\d\d\d\d-\d\d\d\d-\d\d\d\d-\d\d\d[0-9Xx]"
EMAIL_PATTERN = "[0-9A-Za-z._+-]*@[0-9A-Za-z._-]*\.[A-Za-z0-9]*"

# +-----------+------------------------------------------------------
# | Utilities |
# +-----------+

def validORCID(orcid):
    return orcid.lower() in volunteers
    # TO DO: Search the ORCID column, rather than use this technique

def validEmail(email):
    return email.lower() in volunteers
    # TO DO: Search the Email column

def validName(name):
    return name.replace(" ", "\t").lower() in volunteers

# +------+-----------------------------------------------------------
# | Main |
# +------+

if (len(sys.argv) != 4):
    sys.exit("Invalid number of arguments; two required (designated reviewers file, volunteers file, file prefix)")

volunteersFile = open(sys.argv[2])
volunteers = volunteersFile.read().lower()
volunteersFile.close()

matched = open(sys.argv[3] + "-matched.tsv", "w")
missing = open(sys.argv[3] + "-missing.tsv", "w")
none = open(sys.argv[3] + "-none.tsv", "w")

drFile = open(sys.argv[1])
designatedReviewers = csv.reader(drFile, delimiter='\t')
for entry in designatedReviewers:
    number = entry[DR_NUMBER_COLUMN]
    title = entry[DR_TITLE_COLUMN]
    dr = entry[DR_DR_COLUMN]
    for reviewer in dr.split("\n"):
        foundMatch = False
        if reviewer.lower() == "none":
            none.write(number + "\t" + title + "\n")
        else:
            info = number + "\t" + title + "\t" + reviewer + "\n"
            orcids = re.findall(ORCID_PATTERN, reviewer)
            for orcid in orcids:
                if validORCID(orcid):
                    foundMatch = True
            emails = re.findall(EMAIL_PATTERN, reviewer)
            for email in emails:
                if validEmail(email):
                    foundMatch = True
            for name in reviewer.split(","):
                if validName(name):
                    foundMatch = True
            if foundMatch:
                matched.write(info)
            else:
                missing.write(info)

# Time to clean up
drFile.close()
matched.close()
missing.close()
none.close()

