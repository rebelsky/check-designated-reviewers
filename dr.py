import sys
import csv
import re

# +----------+-------------------------------------------------------
# | Settings |
# +----------+

ORCID_PATTERN = "\d\d\d\d-\d\d\d\d-\d\d\d\d-\d\d\d[0-9Xx]"
EMAIL_PATTERN = "[0-9A-Za-z._+-]*@[0-9A-Za-z._-]*\.[A-Za-z0-9]*"

# +-----------+------------------------------------------------------
# | Utilities |
# +-----------+

def validORCID(volunteers, orcid):
    return orcid.lower() in volunteers

def validEmail(volunteers, email):
    return email.lower() in volunteers

def validName(volunteers, name):
    return name.lower() in volunteers

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
            if name == currentName:
                return authorInfo[3]
    return "EMAIL"

# +------+-----------------------------------------------------------
# | Main |
# +------+

def __main__():
    # Sanity check
    if (len(sys.argv) != 5):
        sys.exit(f"Invalid number of arguments; four required (submissions file, volunteers file, authors file, suffix). E.g.,\n  python3 {sys.argv[0]} submissions.tsv volunteers.tsv authors.tsv monday")
    
    # Grab all the info on volunteers
    volunteersFile = open(sys.argv[2])
    volunteers = volunteersFile.read().lower().replace("\t", " ")
    volunteersFile.close()
   
    # Authors
    authorsFile = open(sys.argv[3])
    authors = authorsFile.read().split("\n")
    authorsFile.close()

    # Prepare output files
    SUFFIX = sys.argv[4]
    matched = open(f"matched{SUFFIX}.tsv", "w")
    missing = open(f"missing{SUFFIX}.tsv", "w")
    none = open(f"none{SUFFIX}.tsv", "w")
    
    matched.write("#\tTitle\tName\tEmail\tORCid\tNotes\n")
    missing.write("#\tTitle\tName\tEmail\tORCid\tNotes\n")
    none.write("#\tAuthors\tTitle\tNotes\n")
    
    # Prepare to process the submission info
    submissionsFile = open(sys.argv[1])
    submissions = csv.reader(submissionsFile, delimiter='\t')
    
    # Grab the indices of important submission columns
    submissionsHeaders = submissions.__next__()
    SUBMISSIONS_NUMBER_COLUMN = submissionsHeaders.index("#")
    SUBMISSIONS_AUTHORS_COLUMN = submissionsHeaders.index("Authors")
    SUBMISSIONS_TITLE_COLUMN = submissionsHeaders.index("Title")
    SUBMISSIONS_DR_COLUMN = submissionsHeaders.index("Designated Reviewer")
    
    # Process all the submissions
    for entry in submissions:
        number = entry[SUBMISSIONS_NUMBER_COLUMN]
        authors = entry[SUBMISSIONS_AUTHORS_COLUMN]
        title = entry[SUBMISSIONS_TITLE_COLUMN]
        designatedReviewers = entry[SUBMISSIONS_DR_COLUMN]
        for reviewer in designatedReviewers.split("\n"):
            foundMatch = False
            name = "NAME"
            orcid = "ORCID"
            email = "EMAIL"
            if reviewer.lower() == "none":
                none.write(f"{number}\t{authors}\t{title}\t\n")
            else:
                orcids = re.findall(ORCID_PATTERN, reviewer)
                for orcid in orcids:
                    if validORCID(volunteers, orcid):
                        foundMatch = True
                emails = re.findall(EMAIL_PATTERN, reviewer)
                for email in emails:
                    if validEmail(volunteers, email):
                        foundMatch = True
                if orcid == "ORCID" and email == "EMAIL":
                    for name in reviewer.split(","):
                        if validName(volunteers, name):
                            foundMatch = True
                    name = reviewer
                if name != "NAME" and email == "EMAIL":
                    email = lookupEmail(authors, number, name)
                    if email != "EMAIL" and validEmail(volunteers, email):
                        foundMatch = True
                if email != "EMAIL" and name == "NAME":
                    name = lookupName(authors, number,email)
                info = f'{number}\t{title}\t{name}\t{email}\t{orcid}\t\n'
                if foundMatch:
                    matched.write(info)
                else:
                    missing.write(info)
    
    # Time to clean up
    submissionsFile.close()
    matched.close()
    missing.close()
    none.close()

__main__()
