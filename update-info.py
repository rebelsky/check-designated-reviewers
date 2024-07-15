import sys
import csv
import re
import os

# +-------+----------------------------------------------------------
# | Usage |
# +-------+

# python3 update-names.py missing.tsv authors.tsv

# missing.tsv comes from dr.py and is supposed to contain the missing
# reviewers.

# authors.tsv is downloaded from EasyChair
#   Conference -> Conference data download 

# +-----------+------------------------------------------------------
# | Utilities |
# +-----------+

def log(str):
    print(str, file=sys.stderr)

def lookupName(authors, number, email):
    for author in authors:
        authorInfo = author.split("\t")
        if number == authorInfo[0]:
            if email.lower() == authorInfo[3].lower():
                return f"{authorInfo[1]} {authorInfo[2]}"
    return "NAME"

def lookupEmail(authors, number, name):
    name = name.lower()
    for author in authors:
        authorInfo = author.split("\t")
        if number == authorInfo[0]:
            currentName = f"{authorInfo[1]} {authorInfo[2]}".lower()
            log(f"Comparing {name} to {currentName}")
            if name == currentName:
                log("  Matched")
                return authorInfo[3]
            else:
                log("  Did not match")
    return "EMAIL"

# +------+-----------------------------------------------------------
# | Main |
# +------+

# Sanity check
if (len(sys.argv) != 3):
    sys.exit(f"Invalid number of arguments; two required (missing reviewers file, authors file). e.g.\n  python3 {sys.argv[0]} missing.tsv authors.tsv")

# Authors
authorsFile = open(sys.argv[2])
authors = authorsFile.read().split("\n")
authorsFile.close()

# Grab the indices of important author columns
reviewersHeaders = authors[0].split("\t")
REVIEWERS_NUMBER_COLUMN = reviewersHeaders.index("submission #")
REVIEWERS_FNAME_COLUMN = reviewersHeaders.index("first name")
REVIEWERS_LNAME_COLUMN = reviewersHeaders.index("last name")
REVIEWERS_EMAIL_COLUMN = reviewersHeaders.index("email")

# Prepare to process the reviewers info
reviewersFile = open(sys.argv[1])
reviewers = csv.reader(reviewersFile, delimiter='\t')

# Grab the indices of important submission columns
reviewersHeaders = reviewers.__next__()
REVIEWERS_NUMBER_COLUMN = reviewersHeaders.index("#")
REVIEWERS_TITLE_COLUMN = reviewersHeaders.index("Title")
REVIEWERS_NAME_COLUMN = reviewersHeaders.index("Name")
REVIEWERS_EMAIL_COLUMN = reviewersHeaders.index("Email")
REVIEWERS_ORCID_COLUMN = reviewersHeaders.index("ORCid")
REVIEWERS_NOTES_COLUMN = reviewersHeaders.index("Notes")

print("#\tTitle\tName\tEmail\tORCid\tNotes")

# Process all the reviewers
for entry in reviewers:
    number = entry[REVIEWERS_NUMBER_COLUMN]
    title = entry[REVIEWERS_TITLE_COLUMN]
    name = entry[REVIEWERS_NAME_COLUMN]
    email = entry[REVIEWERS_EMAIL_COLUMN]
    orcid = entry[REVIEWERS_ORCID_COLUMN]
    notes = entry[REVIEWERS_NOTES_COLUMN]

    if (name == "???") or (name == "NAME"):
        name = lookupName(authors, number,email)
    if (email == "???") or (email == "EMAIL"):
        email = lookupEmail(authors, number, name)

    print(f"{number}\t{title}\t{name}\t{email}\t{orcid}\t{notes}");

reviewersFile.close()
