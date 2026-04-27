import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['datadna_dev']
    
    # The email that should be the ONLY admin
    admin_email = 'sankalpshrivastava04@gmail.com'
    
    # 1. Demote everyone else who might be an admin
    demote_result = await db.users.update_many(
        {'email': {'$ne': admin_email}, 'role': 'admin'},
        {'$set': {'role': 'user'}}
    )
    
    # 2. Ensure the specific user is admin
    promote_result = await db.users.update_many(
        {'email': admin_email},
        {'$set': {'role': 'admin', 'dashboard_access': True}}
    )
    
    print(f'Demoted {demote_result.modified_count} other users.')
    print(f'Ensured {promote_result.modified_count} matched user ({admin_email}) is admin.')
    client.close()

if __name__ == '__main__':
    asyncio.run(main())
