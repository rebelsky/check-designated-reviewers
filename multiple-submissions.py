# A script to identify people with multiple submissions (useful for
# telling such folks that they need to review).

import sys
import csv
import re

# +----------+-------------------------------------------------------
# | Settings |
# +----------+

EMAIL_PATTERN = "[0-9A-Za-z._+-]*@[0-9A-Za-z._-]*\.[A-Za-z0-9]*"

# +-----------+------------------------------------------------------
# | Utilities |
# +-----------+

def validEmail(volunteers, email):
    return email.lower() in volunteers

def validName(volunteers, name):
    return name.lower() in volunteers

def log(str):
    print(str, file=sys.stderr)

def check(multiple, number, title, name, email):
    info = f"{number}\t{title}\t{name}\t{email}"
    if (0 + number) >= 3:
        multiple.write(info + "\n")

# +------+-----------------------------------------------------------
# | Main |
# +------+

def __main__():
    # Sanity check
    if (len(sys.argv) != 4):
        sys.exit(f"Invalid number of arguments; 3 required (sorted authors file, volunteers file, deleted file). E.g.,\n  python3 {sys.argv[0]} authors.tsv volunteers.tsv deleted.tsv")
    
    # Grab all the info on volunteers
    volunteersFile = open(sys.argv[2])
    volunteers = volunteersFile.read().lower().replace("\t", " ")
    volunteersFile.close()
   
    # Deleted
    deletedPapersFile = open(sys.argv[3])
    deletedPapers = deletedPapersFile.read().split("\n")
    deletedPapersFile.close()

    # Prepare output files
    multiple = open(f"multiple.tsv", "w")
    
    multiple.write("#\tTitle\tName\tEmail\tORCid\tNotes\n")
    
    # Prepare to process the authors info
    authorsFile = open(sys.argv[1])
    authors = csv.reader(authorsFile, delimiter='\t')
    
    # Grab the indices of important submission columns
    authorsHeaders = authors.__next__()
    NUMBER_COLUMN = authorsHeaders.index("submission #")
    FNAME_COLUMN = authorsHeaders.index("first name")
    LNAME_COLUMN = authorsHeaders.index("last name")
    EMAIL_COLUMN = authorsHeaders.index("email")
    
    # Process all the authors
    number = 0
    title = ""
    prevEmail = ""
    prevName = ""
    for entry in authors:
        email = entry[EMAIL_COLUMN]
        name = f"{entry[FNAME_COLUMN]} {entry[LNAME_COLUMN]}"
        paperNumber = entry[NUMBER_COLUMN]
        if paperNumber in deletedPapers:
            pass
        # elif validEmail(volunteers, email) or validName(volunteers, name):
        #    pass
        else:
            if email == prevEmail:
                number += 1
                title = f"{title}, {paperNumber}"
            else:
                check(multiple, number, title, prevName, prevEmail)
                number = 1
                prevEmail = email
                prevName = name
                title = paperNumber

    # Handle the last author
    check(multiple, number, title, name, prevEmail)

    # Time to clean up
    authorsFile.close()
    multiple.close()

__main__()
