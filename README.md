# Checking Designated Reviewers

A script to see which designated reviewers for SIGCSE TS submissions have not yet signed up to review.

## Use case

_As a Program Chair of ACM SIGCSE TS, I want to be able to easily determine which designated reviewers have actually signed up to review and which have not. Unfortunately, submitters do not follow instructions well, so the "Designated Reviewer" field can have a variety of forms of information (ORCIDs in various forms, email, names, the word "None", etc.; some put separate reviewers on separate lines, some use commas to separate them)._

## Instructions

1. Download the list of volunteers from the Google sheet as a TSV. 
   I tend to use `volunteers-YYYYMMDD-HHMM.tsv`

2. Make sure that the submissions page on EasyChair includes the
   designated reviewer field. If not, click "click here to select
   which fields should be visible" and add the appropriate field.

3. Download the list of submissions as an Excel file. I tend to 
   use `submissions-YYYYMMDD-HHMM.xlsx` 

4. Convert the Excel file to a TSV file. On a Mac, I find it better
   to use Numbers and "Export To TSV ...".  Excel's Export to TSV
   seems to use a strange encoding that Python doesn't like.

6. Make sure the column numbers in the settings section match those
   in the spreadsheets. (Unfortunately, these depend on too many
   factors to be sure.)

7. Pick a prefix to use for the created files. For example
   `YYYYMMDD-HHMM`.

8. Run the program
```
python3 dr.py SUBMISSIONS.tsv VOLUNTEERS.tsv PREFIX
```

8. Peruse the output
   * PREFIX-matched.tsv contains the designated reviewers who matched
   * PREFIX-missing.tsv contains the designated reviewers who did not match
   * PREFIX-none.tsv contains the papers with no designated reviewer

## Followup activities

1. Look through PREFIX-missing.tsv and re-check the results with the list of volunteers.

2. For any missing volunteers, create letters. A sample letter can be found in the `letters` directory.


