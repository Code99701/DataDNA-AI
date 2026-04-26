import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['datadna_dev']
    user = await db.users.find_one({}, sort=[('created_at', -1)])
    if user:
        print(f"Email: {user.get('email')}")
        print(f"OTP: {user.get('otp_code', 'none')}")
    else:
        print('No users found')
    client.close()

if __name__ == '__main__':
    asyncio.run(main())
