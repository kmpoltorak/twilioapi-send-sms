#!/usr/bin/python3

# Import packages
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Import credentials
from credentials import ACCOUNT_SID, AUTH_TOKEN


def main():
    """
    Script is sending SMS message to mobile phones included in text file
    To run this script properly you have to have in Twilio dashboard "SMS_notification" friendly_name
    parameter under one of active phone numbers. Successful on minimum Python 3.8.

    """

    # File with list of recipient numbers one by one, phone number must be in E.123 format (+[international-prefix][phone-number])
    recipient_file = "recipients.txt"
    # Message which will be send to recipients via SMS
    body_msg = "Test message sent by Python script using Twilio API."

    # List from txt file of SMS recipient phone numbers,
    if os.path.exists(recipient_file):
        if os.stat(recipient_file).st_size != 0:
            with open(recipient_file, encoding="utf-8") as file:
                recipient_list = file.read()
            file.close()
            print(recipient_list)
        else:
            raise Exception(f'File {recipient_file} is empty')
    else:
        raise Exception(f"File {recipient_file} don't exist")

    try:
        # Initialize connection to Twilio API
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        # Get active number which friendly_name parameter is SMS_notification if exists
        if client.incoming_phone_numbers.list(friendly_name="SMS_notification"):
            # Get first record from the list and use as sender number
            sender_number = client.incoming_phone_numbers.list(
                friendly_name="SMS_notification")[0].phone_number
        else:
            raise Exception("Phone number with friendly_name = SMS_notification doesn't exist. \
            Go to Twilio dashboard and verify the number or parameter.")

        # For each recipient from the list send SMS
        for recipient_number in recipient_list:
            # Verify the phone number is it valid mobile number
            client.lookups.phone_numbers(
                recipient_number).fetch(type=["carrier"])
            # If there was no error send SMS
            message = client.messages.create(
                from_=sender_number, to=recipient_number, body=body_msg)
            # Print message unique SID (string identifier)
            print(f"Message ID: {message.sid}")

    except TwilioRestException as exception:
        print(f"{exception}")

# Run the script
if __name__ == "__main__":
    main()
