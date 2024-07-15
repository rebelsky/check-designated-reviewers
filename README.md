# Checking Designated Reviewers

A script to see which designated reviewers for SIGCSE TS submissions have not yet signed up to review.

## Use case

_As a Program Chair of ACM SIGCSE TS, I want to be able to easily determine which designated reviewers have actually signed up to review and which have not. Unfortunately, submitters do not follow instructions well, so the "Designated Reviewer" field can have a variety of forms of information (ORCIDs in various forms, email, names, the word "None", etc.; some put separate reviewers on separate lines, some use commas to separate them)._

## Instructions

1. Download the list of volunteers from the Google survey results
   as a TSV.  I tend to use `volunteers-YYYYMMDD-HHMM.tsv`

2. Make sure that the submissions page on EasyChair includes the
   designated reviewer field. If not, click "click here to select
   which fields should be visible" and add the appropriate field.

3. Download the list of submissions from EasyChair as an Excel file. 
   I tend to use `submissions-YYYYMMDD-HHMM.xlsx` 

4. Convert the Excel file to a TSV file. On a Mac, I find it better
   to use Numbers and "Export To TSV ...".  Excel's Export to TSV
   seems to use a strange encoding that Python doesn't like.

5. Pick a suffix to use for the created files. For example
   `YYYYMMDD-HHMM`.

6. Run the program
```
python3 dr.py SUBMISSIONS.tsv VOLUNTEERS.tsv SUFFIX
```

7. Peruse the output
   * matched-SUFFIX.tsv contains the designated reviewers who matched
   * missing-SUFFIX.tsv contains the designated reviewers who did not match
   * none-SUFFIX.tsv contains the papers with no designated reviewer

## Followup activities

1. Look through PREFIX-missing.tsv and re-check the results with the list of volunteers.

2. For any missing volunteers, create and send letters. Sample letters can be found in the `letters` directory. (I'm working on a tool to help with creating the letters from the missing reviewers file).


