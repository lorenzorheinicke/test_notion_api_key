import json
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv


def explore_database_metadata(api_key: str, database_id: str) -> Dict[str, Any]:
    """
    Fetch and display all metadata/property configurations from a Notion database.
    
    Args:
        api_key (str): Your Notion API key
        database_id (str): The ID of the database or view
    
    Returns:
        Dict[str, Any]: Dictionary containing the database properties
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    try:
        # First try getting database schema
        response = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"❌ Error accessing database: {response.status_code}")
            print(f"Error message: {response.json().get('message', 'Unknown error')}")
            return {}
        
        database_info = response.json()
        properties = database_info.get('properties', {})
        
        # Print database title if available
        if 'title' in database_info:
            title = database_info['title'][0]['plain_text'] if database_info['title'] else 'Untitled'
            print(f"\n📚 Database: {title}")
        
        print("\n🔍 Property Metadata:")
        print("-" * 50)
        
        # Process and display each property
        for prop_name, prop_info in properties.items():
            prop_type = prop_info['type']
            print(f"\n📋 {prop_name}")
            print(f"   Type: {prop_type}")
            
            # Show additional details based on property type
            if prop_type == 'select':
                options = prop_info['select']['options']
                print("   Options:")
                for opt in options:
                    color = opt.get('color', 'default')
                    print(f"    - {opt['name']} ({color})")
                    
            elif prop_type == 'multi_select':
                options = prop_info['multi_select']['options']
                print("   Options:")
                for opt in options:
                    color = opt.get('color', 'default')
                    print(f"    - {opt['name']} ({color})")
                    
            elif prop_type == 'relation':
                related_db = prop_info['relation']['database_id']
                print(f"   Related Database ID: {related_db}")
                
            elif prop_type == 'formula':
                formula = prop_info['formula']['expression']
                print(f"   Formula: {formula}")
                
            elif prop_type == 'rollup':
                relation = prop_info['rollup']['relation_property_name']
                rollup = prop_info['rollup']['rollup_property_name']
                print(f"   Rollup: {relation} → {rollup}")
        
        # Get a sample entry to show actual data structure
        query_response = requests.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            headers=headers,
            json={"page_size": 1}
        )
        
        if query_response.status_code == 200:
            results = query_response.json().get('results', [])
            if results:
                print("\n📝 Sample Data Entry:")
                print("-" * 50)
                sample_props = results[0]['properties']
                for prop_name, prop_data in sample_props.items():
                    print(f"\n{prop_name}:")
                    print(f"   Raw structure: {json.dumps(prop_data, indent=2)}")
        
        return properties
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return {}

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if not api_key or not database_id:
        print("❌ Error: Missing required environment variables")
        print("Please ensure NOTION_API_KEY and NOTION_DATABASE_ID are set in your .env file")
        exit(1)
    
    properties = explore_database_metadata(api_key, database_id)
    
    print("\n💡 Usage Tips:")
    print("-" * 50)
    print("• To access a property in your queries, use the exact property names shown above")
    print("• Property types determine how you can filter and sort your data")
    print("• For relation properties, you'll need the related database ID for deep queries")