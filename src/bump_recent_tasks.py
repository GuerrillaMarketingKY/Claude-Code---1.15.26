"""
ClickUp Task Bumper - Bump assignees on tasks created in last 14 days
Skips closed/completed tasks, only bumps in-progress and not-started tasks
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
BUMP_TASKS_CREATED_DAYS = 14  # Bump tasks created in last 14 days

class ClickUpBumper:
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
                    'include_closed': 'false'  # Skip closed tasks
                }
            )
            response.raise_for_status()
            return response.json().get('tasks', [])
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            return []

    def format_assignee_mentions(self, assignees):
        """Format assignee mentions for ClickUp comment"""
        if not assignees:
            return ""

        # Create mention format: @[user_id]
        mentions = []
        for assignee in assignees:
            user_id = assignee.get('id')
            username = assignee.get('username', 'Unknown')
            if user_id:
                mentions.append(f"@{user_id}")

        return " ".join(mentions) if mentions else ""

    def add_task_comment(self, task_id: str, comment_text: str):
        """Add a comment to a task"""
        try:
            response = requests.post(
                f'{BASE_URL}/task/{task_id}/comment',
                headers=self.headers,
                json={
                    'comment_text': comment_text,
                    'notify_all': True  # Notify all assignees
                }
            )

            if response.status_code == 200:
                return True
            else:
                print(f"        ✗ Failed to comment: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"        ✗ Error adding comment: {e}")
            return False

    def should_bump_task(self, task):
        """Check if task should be bumped"""
        # Get task status
        status = task.get('status', {}).get('status', '').lower()

        # Skip if status contains 'closed' or 'complete'
        if 'closed' in status or 'complete' in status or 'done' in status:
            return False

        # Only bump if status suggests in-progress or not started
        # Common statuses: "to do", "in progress", "not started", "pending", etc.
        return True

    def bump_recent_tasks(self):
        """Find and bump tasks created in last 14 days"""
        print(f"\n🔔 ClickUp Task Bumper")
        print(f"{'='*60}")
        print(f"Bumping tasks created in last {BUMP_TASKS_CREATED_DAYS} days")
        print(f"Skipping: closed, completed, done tasks")
        print(f"{'='*60}\n")

        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=BUMP_TASKS_CREATED_DAYS)

        spaces = self.get_all_spaces()
        total_bumped = 0
        total_skipped = 0

        for space in spaces:
            space_id = space['id']
            space_name = space['name']

            print(f"📁 Space: {space_name}")

            lists = self.get_all_lists(space_id)

            for lst in lists:
                list_name = lst['name']
                tasks = self.get_tasks_in_list(lst['id'])

                for task in tasks:
                    # Check if task was created in last 14 days
                    date_created_str = task.get('date_created')
                    if not date_created_str:
                        continue

                    date_created = datetime.fromtimestamp(int(date_created_str) / 1000)

                    if date_created < cutoff_date:
                        continue  # Task too old

                    # Check if we should bump this task
                    if not self.should_bump_task(task):
                        total_skipped += 1
                        continue

                    # Task is recent and open - bump it
                    task_name = task['name']
                    task_id = task['id']
                    assignees = task.get('assignees', [])
                    status = task.get('status', {}).get('status', 'No status')
                    days_since_created = (datetime.now() - date_created).days

                    print(f"\n  📌 {task_name[:50]}...")
                    print(f"     List: {list_name}")
                    print(f"     Status: {status}")
                    print(f"     Created: {days_since_created} days ago")
                    print(f"     Assignees: {len(assignees)}")

                    # Format comment with mentions
                    mentions = self.format_assignee_mentions(assignees)

                    if assignees:
                        comment = f"""🔔 Task Check-In: This task was created {days_since_created} day{'s' if days_since_created != 1 else ''} ago.

{mentions} - Please provide a status update or mark as complete."""
                    else:
                        comment = f"""🔔 Task Check-In: This task was created {days_since_created} day{'s' if days_since_created != 1 else ''} ago.

Please assign someone or provide a status update."""

                    if self.add_task_comment(task_id, comment):
                        total_bumped += 1
                        print(f"     ✓ Bump comment added")
                    else:
                        print(f"     ✗ Failed to add comment")

            print()  # Space between spaces

        print(f"{'='*60}")
        print(f"📊 Summary:")
        print(f"   Tasks bumped: {total_bumped}")
        print(f"   Tasks skipped (closed/completed): {total_skipped}")
        print(f"{'='*60}")


def main():
    print("=" * 60)
    print("  ClickUp Task Bumper")
    print("=" * 60)

    if not CLICKUP_API_TOKEN:
        print("\n❌ CLICKUP_API_TOKEN not found in .env")
        return

    if not WORKSPACE_ID:
        print("\n❌ WORKSPACE_ID not found in .env")
        return

    bumper = ClickUpBumper(CLICKUP_API_TOKEN, WORKSPACE_ID)
    bumper.bump_recent_tasks()


if __name__ == '__main__':
    main()
