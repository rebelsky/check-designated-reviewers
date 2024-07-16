import sys
import csv
import re
import os
import urllib.parse

# +------+-----------------------------------------------------------
# | Main |
# +------+

# Sanity check
if (len(sys.argv) != 3):
    sys.exit(f"Invalid number of arguments; two required (missing reviewers file, template file). e.g.\n  python3 {sys.argv[0]} missing.tsv letters/designated-reviewer.txt")

# Grab the template
templateFile = open(sys.argv[2])
template = templateFile.read()
templateFile.close()

# Prepare to process the reviewers info
reviewersFile = open(sys.argv[1])
reviewers = csv.reader(reviewersFile, delimiter='\t')

# Grab the indices of important submission columns
reviewersHeaders = reviewers.__next__()
REVIEWERS_NUMBER_COLUMN = reviewersHeaders.index("#")
REVIEWERS_TITLE_COLUMN = reviewersHeaders.index("Title")
REVIEWERS_NAME_COLUMN = reviewersHeaders.index("Name")
REVIEWERS_EMAIL_COLUMN = reviewersHeaders.index("Email")

# Process all the reviewers
for entry in reviewers:
    number = entry[REVIEWERS_NUMBER_COLUMN]
    title = entry[REVIEWERS_TITLE_COLUMN]
    name = entry[REVIEWERS_NAME_COLUMN]
    email = entry[REVIEWERS_EMAIL_COLUMN]

    letter = template
    letter = re.sub("NUMBER", number, letter)
    letter = re.sub("TITLE", title, letter)
    letter = re.sub("NAME", name, letter)

    subject = f"[SIGCSE TS 2025] Please sign up to review ({name})"

    print(f"<a href='mailto:{email}?cc=rebelsky@grinnell.edu&subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(letter)}'>{number} - {name}</a><br/>")

# Time to clean up
reviewersFile.close()
