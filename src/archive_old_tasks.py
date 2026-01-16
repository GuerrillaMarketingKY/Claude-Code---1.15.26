"""
ClickUp Task Archiver - Move old tasks to archive
Moves tasks with no updates in 30+ days to "Task Archive - Needs Reviewed"
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

CLICKUP_API_TOKEN = os.getenv('CLICKUP_API_TOKEN')
WORKSPACE_ID = os.getenv('WORKSPACE_ID')
BASE_URL = 'https://api.clickup.com/api/v2'

# Configuration
ARCHIVE_AFTER_DAYS = 30
ARCHIVE_LIST_NAME = "Task Archive - Needs Review"

class ClickUpArchiver:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            'Authorization': api_token,
            'Content-Type': 'application/json'
        }

    def get_all_lists(self, space_id: str):
        """Get all lists in a space"""
        try:
            response = requests.get(
                f'{BASE_URL}/space/{space_id}/list',
                headers=self.headers,
                params={'archived': 'false'}
            )
            response.raise_for_status()
            return response.json().get('lists', [])
        except Exception as e:
            print(f"Error fetching lists: {e}")
            return []

    def get_tasks_in_list(self, list_id: str):
        """Get all tasks in a list"""
        try:
            response = requests.get(
                f'{BASE_URL}/list/{list_id}/task',
                headers=self.headers,
                params={'archived': 'false', 'include_closed': 'false'}
            )
            response.raise_for_status()
            return response.json().get('tasks', [])
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            return []

    def move_task_to_list(self, task_id: str, target_list_id: str):
        """Move a task to another list"""
        try:
            response = requests.put(
                f'{BASE_URL}/task/{task_id}',
                headers=self.headers,
                json={'list': target_list_id}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error moving task: {e}")
            return False

    def find_archive_list(self, space_id: str):
        """Find or suggest creating the archive list"""
        lists = self.get_all_lists(space_id)
        for lst in lists:
            if ARCHIVE_LIST_NAME.lower() in lst['name'].lower():
                return lst['id']
        return None

    def archive_old_tasks(self, space_id: str):
        """Archive tasks older than threshold"""
        print(f"\n🗂️  Archiving tasks older than {ARCHIVE_AFTER_DAYS} days...")
        print(f"Target: {ARCHIVE_LIST_NAME}\n")

        # Find archive list
        archive_list_id = self.find_archive_list(space_id)
        if not archive_list_id:
            print(f"❌ Archive list '{ARCHIVE_LIST_NAME}' not found!")
            print(f"   Please create this list in your space first.")
            return

        print(f"✓ Found archive list\n")

        cutoff_date = datetime.now() - timedelta(days=ARCHIVE_AFTER_DAYS)
        lists = self.get_all_lists(space_id)

        archived_count = 0
        skipped_count = 0

        for lst in lists:
            # Skip the archive list itself
            if lst['id'] == archive_list_id:
                continue

            list_name = lst['name']
            tasks = self.get_tasks_in_list(lst['id'])

            for task in tasks:
                date_updated_str = task.get('date_updated')
                if not date_updated_str:
                    continue

                last_updated = datetime.fromtimestamp(int(date_updated_str) / 1000)
                days_old = (datetime.now() - last_updated).days

                if days_old >= ARCHIVE_AFTER_DAYS:
                    task_name = task['name']
                    print(f"📦 Archiving: {task_name} ({days_old}d old)")

                    if self.move_task_to_list(task['id'], archive_list_id):
                        archived_count += 1
                        print(f"   ✓ Moved to archive")
                    else:
                        skipped_count += 1
                        print(f"   ✗ Failed to move")

        print(f"\n📊 Summary:")
        print(f"   Archived: {archived_count} tasks")
        if skipped_count > 0:
            print(f"   Failed: {skipped_count} tasks")


def main():
    print("=" * 60)
    print("  ClickUp Task Archiver")
    print("=" * 60)

    if not CLICKUP_API_TOKEN:
        print("\n❌ CLICKUP_API_TOKEN not found in .env")
        return

    archiver = ClickUpArchiver(CLICKUP_API_TOKEN)

    # You'll need to provide your space ID
    # Get it from ClickUp URL: app.clickup.com/WORKSPACE_ID/v/l/SPACE_ID
    space_id = input("\nEnter your Space ID (from ClickUp URL): ").strip()

    if space_id:
        archiver.archive_old_tasks(space_id)
    else:
        print("❌ Space ID required")

if __name__ == '__main__':
    main()
