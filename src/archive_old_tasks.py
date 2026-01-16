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
        """Move a task to another list and verify it worked"""
        try:
            response = requests.put(
                f'{BASE_URL}/task/{task_id}',
                headers=self.headers,
                json={'list': target_list_id}
            )

            if response.status_code == 200:
                # Verify the task actually moved by checking its new list
                verify_response = requests.get(
                    f'{BASE_URL}/task/{task_id}',
                    headers=self.headers
                )

                if verify_response.status_code == 200:
                    task_data = verify_response.json()
                    actual_list_id = task_data.get('list', {}).get('id', '')

                    if actual_list_id == target_list_id:
                        return True
                    else:
                        print(f"        ✗ Move rejected: Task stayed in list {actual_list_id}")
                        print(f"        (ClickUp likely blocked cross-space move)")
                        return False
                else:
                    print(f"        ✗ Verification failed: HTTP {verify_response.status_code}")
                    return False
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
        """Archive tasks older than threshold - create archive in each space"""
        print(f"\n🗂️  Archiving tasks older than {ARCHIVE_AFTER_DAYS} days...")
        print(f"Strategy: Create '{ARCHIVE_LIST_NAME}' in each space")
        print(f"(ClickUp blocks cross-space task moves)\n")

        # Get all spaces
        spaces = self.get_all_spaces()
        total_archived = 0
        total_failed = 0

        # Process each space separately
        for space in spaces:
            space_id = space['id']
            space_name = space['name']

            print(f"{'='*60}")
            print(f"  📁 Space: {space_name}")
            print(f"{'='*60}")

            # Get all lists in this space
            lists = self.get_all_lists(space_id)

            # Find old tasks in this space
            old_tasks_in_space = []

            for lst in lists:
                # Skip if this IS the archive list
                if ARCHIVE_LIST_NAME.lower() in lst['name'].lower():
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
                        task['_source_list'] = list_name
                        task['_days_old'] = days_old
                        old_tasks_in_space.append(task)

            if not old_tasks_in_space:
                print(f"  ✓ No old tasks in this space\n")
                continue

            print(f"  Found {len(old_tasks_in_space)} old tasks in this space")

            # Find or create archive list in THIS space
            archive_list_id, was_created = self.find_or_create_archive_list(space_id, space_name)

            if not archive_list_id:
                print(f"  ❌ Could not find/create archive list")
                total_failed += len(old_tasks_in_space)
                print()
                continue

            if was_created:
                print(f"  ✓ Created new archive list")
            else:
                print(f"  ✓ Using existing archive list")

            print(f"\n  Moving {len(old_tasks_in_space)} tasks to archive...\n")

            # Move tasks to archive within same space
            space_archived = 0
            space_failed = 0

            for task in old_tasks_in_space:
                task_name = task['name']
                task_id = task['id']
                source_list = task.get('_source_list', 'Unknown')
                days_old = task.get('_days_old', 0)

                print(f"  📦 {task_name[:60]}...")
                print(f"     From: {source_list} ({days_old}d old)")

                if self.move_task_to_list(task_id, archive_list_id, task_name):
                    space_archived += 1
                    print(f"     ✓ Moved to archive")
                else:
                    space_failed += 1
                    # Error already printed by move_task_to_list
                print()

            total_archived += space_archived
            total_failed += space_failed

            print(f"  Space summary: {space_archived} archived, {space_failed} failed\n")

        print(f"{'='*60}")
        print(f"📊 Final Summary:")
        print(f"   Successfully archived: {total_archived} tasks")
        if total_failed > 0:
            print(f"   Failed: {total_failed} tasks")
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
