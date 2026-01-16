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
    def __init__(self, api_token: str, workspace_id: str):
        self.api_token = api_token
        self.workspace_id = workspace_id
        self.headers = {
            'Authorization': api_token,
            'Content-Type': 'application/json'
        }

    def get_all_spaces(self):
        """Get all spaces in the workspace"""
        try:
            response = requests.get(
                f'{BASE_URL}/team/{self.workspace_id}/space',
                headers=self.headers,
                params={'archived': 'false'}
            )
            response.raise_for_status()
            return response.json().get('spaces', [])
        except Exception as e:
            print(f"Error fetching spaces: {e}")
            return []

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
                params={
                    'archived': 'false',
                    'include_closed': 'true',  # Include closed tasks
                    'subtasks': 'true'
                }
            )
            response.raise_for_status()
            return response.json().get('tasks', [])
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            return []

    def create_list(self, space_id: str, list_name: str):
        """Create a new list in a space"""
        try:
            response = requests.post(
                f'{BASE_URL}/space/{space_id}/list',
                headers=self.headers,
                json={'name': list_name}
            )
            response.raise_for_status()
            return response.json().get('id')
        except Exception as e:
            print(f"Error creating list: {e}")
            return None

    def move_task_to_list(self, task_id: str, target_list_id: str, task_name: str = ""):
        """Move a task to another list (must be in same space)"""
        try:
            response = requests.put(
                f'{BASE_URL}/task/{task_id}',
                headers=self.headers,
                json={'list': target_list_id}
            )

            if response.status_code == 200:
                return True
            else:
                print(f"        ✗ Failed: HTTP {response.status_code} - {response.text[:100]}")
                return False
        except Exception as e:
            print(f"        ✗ Error: {e}")
            return False

    def find_or_create_archive_list(self, space_id: str, space_name: str):
        """Find or create archive list in a specific space"""
        lists = self.get_all_lists(space_id)

        # Try to find existing archive list
        for lst in lists:
            if ARCHIVE_LIST_NAME.lower() in lst['name'].lower():
                return lst['id'], False  # Found existing

        # Create new archive list in this space
        print(f"     Creating '{ARCHIVE_LIST_NAME}' list in '{space_name}' space...")
        list_id = self.create_list(space_id, ARCHIVE_LIST_NAME)
        if list_id:
            print(f"     ✓ Created archive list")
            return list_id, True  # Created new
        else:
            return None, False

    def get_all_tasks_across_workspace(self):
        """Get ALL tasks from all spaces in workspace"""
        all_tasks = []
        spaces = self.get_all_spaces()

        for space in spaces:
            space_id = space['id']
            space_name = space['name']
            print(f"  📁 Scanning space: {space_name}")

            lists = self.get_all_lists(space_id)

            for lst in lists:
                # Skip archive lists
                if ARCHIVE_LIST_NAME.lower() in lst['name'].lower():
                    continue

                list_name = lst['name']
                tasks = self.get_tasks_in_list(lst['id'])

                for task in tasks:
                    task['_source_space'] = space_name
                    task['_source_list'] = list_name
                    all_tasks.append(task)

        return all_tasks

    def archive_old_tasks(self):
        """Archive tasks older than threshold - move all to Production archive"""
        print(f"\n🗂️  Archiving tasks older than {ARCHIVE_AFTER_DAYS} days...")
        print(f"Target: {ARCHIVE_LIST_NAME} (Production space)")
        print(f"Scanning all spaces in workspace...\n")

        # HARDCODED: Production space archive list ID (from user)
        PRODUCTION_ARCHIVE_LIST_ID = "901324425454"

        # Get all tasks across all spaces
        print("Fetching all tasks across workspace...\n")
        all_tasks = self.get_all_tasks_across_workspace()

        print(f"\n✓ Total tasks found: {len(all_tasks)}\n")

        # Find tasks older than 30 days
        old_tasks = []
        for task in all_tasks:
            date_updated_str = task.get('date_updated')
            if not date_updated_str:
                continue

            last_updated = datetime.fromtimestamp(int(date_updated_str) / 1000)
            days_old = (datetime.now() - last_updated).days

            if days_old >= ARCHIVE_AFTER_DAYS:
                old_tasks.append((task, days_old))

        print(f"Found {len(old_tasks)} tasks older than {ARCHIVE_AFTER_DAYS} days\n")

        if not old_tasks:
            print("✓ No old tasks to archive!")
            return

        # Move all old tasks to Production archive
        archived_count = 0
        skipped_count = 0

        print(f"Moving tasks to archive list (ID: {PRODUCTION_ARCHIVE_LIST_ID})...\n")

        for task, days_old in old_tasks:
            task_name = task['name']
            task_id = task['id']
            source_space = task.get('_source_space', 'Unknown')
            source_list = task.get('_source_list', 'Unknown')

            print(f"📦 {task_name}")
            print(f"   From: {source_space} / {source_list} ({days_old}d old)")

            if self.move_task_to_list(task_id, PRODUCTION_ARCHIVE_LIST_ID, task_name):
                archived_count += 1
                print(f"   ✓ Moved to archive")
            else:
                skipped_count += 1
                # Error already printed by move_task_to_list
            print()  # Blank line

        print(f"{'='*60}")
        print(f"📊 Summary:")
        print(f"   Archived: {archived_count} tasks")
        if skipped_count > 0:
            print(f"   Skipped/Failed: {skipped_count} tasks")
        print(f"{'='*60}")


def main():
    print("=" * 60)
    print("  ClickUp Task Archiver")
    print("=" * 60)

    if not CLICKUP_API_TOKEN:
        print("\n❌ CLICKUP_API_TOKEN not found in .env")
        return

    if not WORKSPACE_ID:
        print("\n❌ WORKSPACE_ID not found in .env")
        return

    archiver = ClickUpArchiver(CLICKUP_API_TOKEN, WORKSPACE_ID)
    archiver.archive_old_tasks()

if __name__ == '__main__':
    main()
