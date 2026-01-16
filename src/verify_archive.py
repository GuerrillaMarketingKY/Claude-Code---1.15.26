"""
Quick script to verify what's actually in the Task Archive list
Shows ALL tasks including closed/archived ones
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLICKUP_API_TOKEN = os.getenv('CLICKUP_API_TOKEN')
WORKSPACE_ID = os.getenv('WORKSPACE_ID')
BASE_URL = 'https://api.clickup.com/api/v2'

headers = {
    'Authorization': CLICKUP_API_TOKEN,
    'Content-Type': 'application/json'
}

def find_archive_list():
    """Find the archive list"""
    # Get all spaces
    response = requests.get(
        f'{BASE_URL}/team/{WORKSPACE_ID}/space',
        headers=headers,
        params={'archived': 'false'}
    )
    spaces = response.json().get('spaces', [])

    for space in spaces:
        # Get lists in space
        response = requests.get(
            f'{BASE_URL}/space/{space["id"]}/list',
            headers=headers,
            params={'archived': 'false'}
        )
        lists = response.json().get('lists', [])

        for lst in lists:
            if 'task archive' in lst['name'].lower():
                return lst['id'], lst['name'], space['name']

    return None, None, None

def get_all_tasks_in_archive(list_id):
    """Get ALL tasks in archive including closed/archived"""
    # Try with include_closed=true
    response = requests.get(
        f'{BASE_URL}/list/{list_id}/task',
        headers=headers,
        params={
            'archived': 'false',
            'include_closed': 'true',  # Include closed tasks
            'subtasks': 'true'
        }
    )

    if response.status_code == 200:
        return response.json().get('tasks', [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

print("=" * 60)
print("  Archive List Verification")
print("=" * 60)

list_id, list_name, space_name = find_archive_list()

if not list_id:
    print("\n❌ Archive list not found!")
else:
    print(f"\n✓ Found: '{list_name}' in '{space_name}' space")
    print(f"  List ID: {list_id}\n")

    print("Fetching ALL tasks (including closed)...\n")
    tasks = get_all_tasks_in_archive(list_id)

    print(f"{'='*60}")
    print(f"Total tasks in archive: {len(tasks)}")
    print(f"{'='*60}\n")

    if tasks:
        print("Tasks found:")
        for i, task in enumerate(tasks, 1):
            status = task.get('status', {}).get('status', 'No status')
            print(f"{i}. {task['name']} (Status: {status})")
    else:
        print("❌ NO TASKS FOUND IN ARCHIVE LIST")
        print("\nThis means the API move operations may have failed silently,")
        print("or the tasks were moved to a different list/space.")
