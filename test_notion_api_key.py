import os
import sys

import requests
from dotenv import load_dotenv


def test_notion_api_key(api_key, database_id):
    """
    Test if a Notion API key is valid and has access to the specified database.
    
    Args:
        api_key (str): Your Notion API key
        database_id (str): The ID of the database you want to test access to
    
    Returns:
        bool: True if successful, False if failed
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # First, test basic API access
    try:
        # Test users endpoint
        users_response = requests.get(
            "https://api.notion.com/v1/users",
            headers=headers
        )
        
        if users_response.status_code != 200:
            print(f"❌ API Key validation failed. Status code: {users_response.status_code}")
            print(f"Error: {users_response.json().get('message', 'Unknown error')}")
            return False
            
        print("✅ API key is valid and can access Notion API")
        
        # Test database access
        db_response = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers
        )
        
        if db_response.status_code != 200:
            print(f"❌ Database access failed. Status code: {db_response.status_code}")
            print(f"Error: {db_response.json().get('message', 'Unknown error')}")
            return False
            
        print("✅ Successfully accessed the database")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error occurred: {e}")
        return False

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    api_key = os.getenv('NOTION_API_KEY')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    if not api_key or not database_id:
        print("❌ Missing required environment variables. Please check your .env file.")
        sys.exit(1)
    
    success = test_notion_api_key(api_key, database_id)
    if success:
        print("🎉 All tests passed! Your API key is working correctly.")
    else:
        print("❌ Some tests failed. Please check the errors above.")