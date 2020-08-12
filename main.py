#!/usr/bin/python3

# Import packages
from twilio.rest import Client

# Import constants from credentials file
from credentials import *

"""
Script is sending SMS message to verified mobile phones included in a list of variables.
To run this script properly you have to have in Twilio dashboard "SMS_notification" friendly_name parameter under one of active phone numbers.
Successful on minimum Python 3.8.
"""


def main():
    try:
        # Initialize connection to Twilio API
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        # List of SMS recipient phone numbers (can be loaded from file or database), phone number must be in E.123 format (+[international-prefix][phone-number])
        recipient_list = ["+00000000000", "+00000000000"]
        # Message which will be send to recipients via SMS (can be loaded from file or database)
        body_msg = "Test message sent by Python script using Twilio API."

        # Get active number which friendly_name parameter is SMS_notification if exists
        if client.incoming_phone_numbers.list(friendly_name="SMS_notification"):
            # Get first record from the list and use as sender number
            sender_number = client.incoming_phone_numbers.list(friendly_name="SMS_notification")[0].phone_number
        # Print error if it not exists
        else:
            raise Exception(
                "Phone number with friendly_name parameter equal SMS_notification doesn't exist. \
                Go to Twilio dashboard and verify the number or parameter.")

        # If recipient list is not empty send SMS
        if recipient_list:
            # For each recipient from the list send SMS
            for recipient_number in recipient_list:
                try:
                    # Verify the phone number is it valid mobile number
                    client.lookups.phone_numbers(recipient_number).fetch(type=["carrier"])
                    # If there was no error send SMS
                    message = client.messages.create(from_=sender_number, to=recipient_number, body=body_msg)
                    # Print message unique SID (string identifier)
                    print(f"Message ID: {message.sid}")
                # Print error if the number is not right
                except Exception as e:
                    raise Exception(
                        f"Mobile phone number ({recipient_number}) is not valid.\nError message from Twilio:\n{e}")
        # Print error if the recipient list is empty
        else:
            raise Exception("The recipient list is empty. Nothing has been sent.")

    # Print other errors that can occur
    except Exception as e:
        print(f"ERROR: {e}")


# Run the script
if __name__ == "__main__":
    main()
