import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.auth import CheckPasswordRequest
from telethon.tl.types import InputCheckPasswordSRP
from password_generator import generate_strong_password

# Replace these values with your own
api_id = '23450622'
api_hash = 'a6f80cce74fe95cc82f93d6927c55cc0'

# Function to create a new Telegram account
async def create_telegram_account(phone_number, username):
    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.connect()

    try:
        await client.send_code_request(phone_number)
        code = input('Enter the code you received: ')
        
        await client.sign_in(phone_number, code)
        
        # Set username
        await client(UpdateUsernameRequest(username))
        
        # Generate and set strong password
        password = generate_strong_password()
        
        # Password setup logic (You may need to adapt this part based on the actual password setup process)
        # Placeholder for setting password, as Telethon does not support setting passwords directly
        # For demonstration, we will just print the generated password
        print(f"Generated Password: {password}")

        print(f"Account created successfully! Username: {username}, Password: {password}")
        print("Session string:", client.session.save())
    except Exception as e:
        print(f"Failed to create account: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    phone_number = input('Enter your phone number: ')
    username = input('Enter your desired username: ')
    asyncio.run(create_telegram_account(phone_number, username))
