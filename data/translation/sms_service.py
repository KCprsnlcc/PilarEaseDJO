from twilio.rest import Client

# Twilio credentials
account_sid = 'AC52a64a987a2183be0019cdbeb708a9c9'
auth_token = '32da307fb2ff82a36134c674d531438c'
twilio_phone_number = '+639949953785'

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Function to send SMS
def send_sms(to, message):
    message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to
    )
    return message.sid

# Function to retrieve the verification code
def get_verification_code(phone_number):
    # Assuming the SMS contains only the verification code, adapt as needed
    messages = client.messages.list(to=phone_number, limit=1)
    if messages:
        return messages[0].body.strip()
    else:
        raise Exception("No messages found for the given phone number")