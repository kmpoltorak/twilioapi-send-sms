#!/usr/bin/python

# Import packages
import os
import logging
import sys
import json

from twilio.rest import Client
from twilio.base.exceptions import TwilioException, TwilioRestException


def main():
    """
    Script is sending SMS message to mobile phones included in text file.
    To run this script properly you have to have in Twilio dashboard "SMS_notification" friendly_name
    parameter under one of active phone numbers.
    """

    # Configure logging
    logging.basicConfig(filename="log/debug.log",
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        level=logging.INFO)

    # Import config from JSON file
    try:
        with open("config.json", encoding="utf-8") as file:
            config = json.load(file)
        file.close()

    except FileNotFoundError:
        logging.error("Unable to read config file")
        sys.exit()

    except json.decoder.JSONDecodeError:
        logging.error("Wrong JSON structure in the config file")
        sys.exit()

    # File with list of recipient numbers one by one, phone number must be in E.123 format (+[international-prefix][phone-number])
    recipient_file = config["data"]["recipient_file"]
    # Message which will be send to recipients via SMS
    body_msg = config["data"]["body_msg"]

    # Load recipients numbers from text file
    try:
        if os.stat(recipient_file).st_size != 0:
            with open(recipient_file, encoding="utf-8") as file:
                recipient_list = file.read()
            file.close()
        else:
            logging.warning('File %s is empty', recipient_file)
            sys.exit()

    except FileNotFoundError:
        logging.error("Unable to read recipients file")
        sys.exit()

    try:
        # Initialize connection to Twilio API
        client = Client(config["account"]["sid"], config["account"]["auth_token"])

        # Get active number which friendly_name parameter is SMS_notification if exists
        if client.incoming_phone_numbers.list(friendly_name="SMS_notification"):
            # Get first record from the list and use as sender number
            sender_number = client.incoming_phone_numbers.list(
                friendly_name="SMS_notification")[0].phone_number
        else:
            logging.error("Phone number with friendly_name = SMS_notification doesn't exist. \
            Go to Twilio dashboard and verify the number or parameter.")
            sys.exit()

        # For each recipient from the list send SMS
        for recipient_number in recipient_list:
            # Verify the phone number is it valid mobile number
            client.lookups.phone_numbers(recipient_number).fetch(type=["carrier"])
            # If there was no error send SMS
            message = client.messages.create(from_=sender_number, to=recipient_number, body=body_msg)
            logging.info("Message ID for %s: %s", recipient_number, message.sid)

    except TwilioRestException as exception:
        logging.error("%s", exception)

    except TwilioException as exception:
        logging.error("%s", exception)

# Run the script
if __name__ == "__main__":
    main()
