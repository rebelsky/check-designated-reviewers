# Checking Designated Reviewers

A script to see which designated reviewers for SIGCSE TS submissions have not yet signed up to review.

## Use case

_As a Program Chair of ACM SIGCSE TS, I want to be able to easily determine which designated reviewers have actually signed up to review and which have not. Unfortunately, submitters do not follow instructions well, so the "Designated Reviewer" field can have a variety of forms of information (ORCIDs in various forms, email, names, the word "None", etc.; some put separate reviewers on separate lines, some use commas to separate them)._

## Standard workflow

1. Create `missing.tsv` using `dr.py`. This also creates `matched.tsv` and `none.tsv`

        python3 dr.py submissions.tsv volunteers.tsv authors.tsv ""

2. Read through `missing.tsv` to exclude any that seem unnecessary or correct any missing information.

3. Generate an HTML file with mailto links using `make-letters.py`. (I decided that mailto links are the best compromise for pretending I have mail merge.)

        python3 make-letters.py missing.tsv letters/needs-to-volunteer.txt > mail-links.html

4. Open the HTML file, click on each link, and send with your mail program.

## Required data files

`volunteers.tsv`
  : The downloaded Google survey results

`submissions.tsv`
  : The list of submissions, downloaded from EasyChair. 
  : Make sure that this includes the designated reviewer field.  If not, click "click here to select which fields should be visible" and add the appropriate field.
  : Note that you'll need to download an Excel file and convert to a tab-separated value file.
  : On a Mac, I find it better to use Numbers and "Export To TSV ...".  Excel's Export to TSV seems to use a strange encoding that Python doesn't like.

`authors.tsv`
  : The list of authors, downloaded from EasyChair.
  : You find these in Conference -> Conference data download. 

## Forthcoming

* A technique for identifying authors of three or more submissions who have not volunteered to review.
* Identify accepted authors from last year who are on NONE papers this year.
