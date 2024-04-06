# Automatic Job Application Tool

- This is a simple Python 3 program designed to automate job applications by sending requests to email addresses along with a cover letter and CV PDF file.

## How to Use

1. Ensure that you have installed the required libraries by running: 
`pip install -r requirements.txt`

2. Before running the program, ensure to update the credentials in the main function and add your email address and password to the `.env` file.

3. Append new data to the `data.csv` file. (The recruiter's name can be left empty; in that case, the company name will replace the recruiter's name.)

4. Run the following command: 
`python3 apply-jobs.py`

## For Gmail Users

1. Make sure you have activated 2FA for your account.
2. Generate an app password.
3. Delete spaces in the 16-character-long password and use this password in the `.env` file.
