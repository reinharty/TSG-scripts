# TSG
Collection of scripts used for my administrative tasks at a non-profit sports club.

## Requirements
Pandas

## Setup
Rename secrets-example.json to secrets.json and fill in your values.
The paths may be empty if input and output are in the same folder as the scripts.
The input must be an .xls file with a similiar layout to example.xls.
Columns "Name", "IBAN", "BIC", "Betrag" and quarters 1 to 4 are incluced.
Dictionary quartal_dict must be adjusted to point to the correct columns for each quarter.
Dictionary abteilungen_dict must be adjusted if number or names of departments change.

## Usage
Run main.py and fill input prompt with number of the to-be processed quarter and filename.