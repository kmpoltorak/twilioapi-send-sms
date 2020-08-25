# Overview
This script is created for sending SMS notification to a list of mobile phone numbers. Before sending the SMS script will verify if the number is correct.

# Prerequirements
* Twilio demo or normal account
* Account SID and auth token copied from Twilio project dashboard into **credentials.py** file
* Install all needed packages with: ```pip3 install -r requirements.txt```
* Installed Python3 (my version was 3.8 and all was working fine)
* Bought minimum one number from Twilio and set up "FRIENDLY NAME" parameter to "SMS_notification" with minimum SMS capability
* For demo account and test purposes add your real test phone number to **Phone Numbers >> Verified Caller IDs** list
* Update ```recipient_list``` variable in **main.py** file with your valid mobile numbers

# Script output
If everything will work fine in the output you should see SMS on your mobile phone and message ID printed in console.

# Good to know
Twilio's 2010 API (those under api.twilio.com/2010-04-01/Accounts) respond as XML by default, but can also return JSON, CSV, and even HTML. (Note: Newer APIs of the form productname.twilio.com/v1 are only available as JSON responses). - https://www.twilio.com/docs/usage/troubleshooting/data-types

# Twilio API knowledge base
https://www.twilio.com/docs/api
