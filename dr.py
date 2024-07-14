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

# Sanity check
if (len(sys.argv) != 4):
    sys.exit("Invalid number of arguments; two required (designated reviewers file, volunteers file, file prefix)")

# Grab all the info on volunteers
volunteersFile = open(sys.argv[2])
volunteers = volunteersFile.read().lower()
volunteersFile.close()

# Grab the indices of important volunteer columns
volunteersFile = open(sys.argv[2])
volunteersHeaders = volunteersFile.readline().split("\t")
volunteersFile.close()
VOLUNTEERS_EMAIL_COLUMN = volunteersHeaders.index("Email Address")
VOLUNTEERS_ORCID_COLUMN = volunteersHeaders.index("ORCid")

# Prepare output files
matched = open(sys.argv[3] + "-matched.tsv", "w")
missing = open(sys.argv[3] + "-missing.tsv", "w")
none = open(sys.argv[3] + "-none.tsv", "w")

matched.write("#\tTitle\tName\tEmail\tORCid\n")
missing.write("#\tTitle\tName\tEmail\tORCid\n")
none.write("#\tTitle\n")

# Prepare to process the submission info
submissionsFile = open(sys.argv[1])
submissions = csv.reader(submissionsFile, delimiter='\t')

# Grab the indices of important submission columns
submissionsHeaders = submissions.__next__()
SUBMISSIONS_NUMBER_COLUMN = submissionsHeaders.index("#")
SUBMISSIONS_TITLE_COLUMN = submissionsHeaders.index("Title")
SUBMISSIONS_DR_COLUMN = submissionsHeaders.index("Designated Reviewer")

# Process all the submissions
for entry in submissions:
    number = entry[SUBMISSIONS_NUMBER_COLUMN]
    title = entry[SUBMISSIONS_TITLE_COLUMN]
    designatedReviewers = entry[SUBMISSIONS_DR_COLUMN]
    for reviewer in designatedReviewers.split("\n"):
        foundMatch = False
        name = "???"
        orcid = "???"
        email = "???"
        if reviewer.lower() == "none":
            none.write(number + "\t" + title + "\n")
        else:
            orcids = re.findall(ORCID_PATTERN, reviewer)
            for orcid in orcids:
                if validORCID(orcid):
                    foundMatch = True
            emails = re.findall(EMAIL_PATTERN, reviewer)
            for email in emails:
                if validEmail(email):
                    foundMatch = True
            if orcid == "???" and email == "???":
                for name in reviewer.split(","):
                    if validName(name):
                        foundMatch = True
                name = reviewer
            info = f'{number}\t{title}\t{name}\t{email}\t{orcid}\n'
            if foundMatch:
                matched.write(info)
            else:
                missing.write(info)

# Time to clean up
submissionsFile.close()
matched.close()
missing.close()
none.close()

