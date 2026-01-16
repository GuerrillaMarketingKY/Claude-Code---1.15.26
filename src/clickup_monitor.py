"""
ClickUp Task Monitor - Simple on-demand task checker
Checks all tasks in workspace for:
- Approaching deadlines (within 2 days)
- Stale tasks (7-30 days without updates)
- Old tasks (30+ days - recommends archiving instead of alerting)
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

CLICKUP_API_TOKEN = os.getenv('CLICKUP_API_TOKEN')
WORKSPACE_ID = os.getenv('WORKSPACE_ID')
BASE_URL = 'https://api.clickup.com/api/v2'

# Configuration
DEADLINE_WARNING_DAYS = 2    # Warn when deadline is within this many days
STALE_TASK_DAYS = 7          # Consider task stale after this many days
ARCHIVE_THRESHOLD_DAYS = 30  # Tasks older than this should be archived

class ClickUpMonitor:
    def __init__(self, api_token: str, workspace_id: str):
        self.api_token = api_token
        self.workspace_id = workspace_id
        self.headers = {
            'Authorization': api_token,
            'Content-Type': 'application/json'
        }
        self.processed_reminders = set()  # Track which tasks we've already reminded about

    def get_all_teams(self) -> List[Dict]:
        """Get all teams in the workspace"""
        try:
            response = requests.get(
                f'{BASE_URL}/team',
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get('teams', [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching teams: {e}")
            return []

    def get_all_spaces(self, team_id: str) -> List[Dict]:
        """Get all spaces in a team"""
        try:
            response = requests.get(
                f'{BASE_URL}/team/{team_id}/space',
                headers=self.headers,
                params={'archived': 'false'}
            )
            response.raise_for_status()
            return response.json().get('spaces', [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching spaces: {e}")
            return []

    def get_all_lists(self, space_id: str) -> List[Dict]:
        """Get all lists in a space"""
        try:
            response = requests.get(
                f'{BASE_URL}/space/{space_id}/list',
                headers=self.headers,
                params={'archived': 'false'}
            )
            response.raise_for_status()
            return response.json().get('lists', [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching lists: {e}")
            return []

    def get_tasks_in_list(self, list_id: str) -> List[Dict]:
        """Get all tasks in a list"""
        try:
            response = requests.get(
                f'{BASE_URL}/list/{list_id}/task',
                headers=self.headers,
                params={
                    'archived': 'false',
                    'include_closed': 'false'
                }
            )
            response.raise_for_status()
            return response.json().get('tasks', [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching tasks: {e}")
            return []

    def get_all_tasks(self) -> List[Dict]:
        """Get all active tasks across the entire workspace"""
        all_tasks = []

        print("📥 Fetching all tasks from workspace...")
        teams = self.get_all_teams()

        for team in teams:
            team_id = team['id']
            team_name = team['name']
            print(f"  📁 Team: {team_name}")

            spaces = self.get_all_spaces(team_id)
            for space in spaces:
                space_id = space['id']
                space_name = space['name']
                print(f"    📂 Space: {space_name}")

                lists = self.get_all_lists(space_id)
                for list_item in lists:
                    list_id = list_item['id']
                    list_name = list_item['name']

                    tasks = self.get_tasks_in_list(list_id)
                    all_tasks.extend(tasks)
                    print(f"      📋 List: {list_name} ({len(tasks)} tasks)")

        print(f"\n✓ Total tasks found: {len(all_tasks)}\n")
        return all_tasks

    def check_approaching_deadline(self, task: Dict) -> Optional[Dict]:
        """Check if task has a deadline approaching within threshold"""
        due_date_str = task.get('due_date')
        if not due_date_str:
            return None

        # Convert milliseconds timestamp to datetime
        due_date = datetime.fromtimestamp(int(due_date_str) / 1000)
        now = datetime.now()
        time_until_due = due_date - now

        # Check if deadline is within warning period
        if timedelta(0) < time_until_due <= timedelta(days=DEADLINE_WARNING_DAYS):
            hours_remaining = time_until_due.total_seconds() / 3600
            return {
                'type': 'deadline',
                'task': task,
                'hours_remaining': hours_remaining,
                'due_date': due_date
            }

        return None

    def check_stale_task(self, task: Dict) -> Optional[Dict]:
        """Check if task hasn't been updated recently (7-30 days)"""
        date_updated_str = task.get('date_updated')
        if not date_updated_str:
            return None

        # Convert milliseconds timestamp to datetime
        last_updated = datetime.fromtimestamp(int(date_updated_str) / 1000)
        now = datetime.now()
        days_since_update = (now - last_updated).days

        # Only alert on tasks between 7-30 days stale
        # Tasks over 30 days should be archived instead
        if STALE_TASK_DAYS <= days_since_update < ARCHIVE_THRESHOLD_DAYS:
            return {
                'type': 'stale',
                'task': task,
                'days_since_update': days_since_update,
                'last_updated': last_updated
            }

        return None

    def check_old_task(self, task: Dict) -> bool:
        """Check if task is older than archive threshold (30+ days)"""
        date_updated_str = task.get('date_updated')
        if not date_updated_str:
            return False

        # Convert milliseconds timestamp to datetime
        last_updated = datetime.fromtimestamp(int(date_updated_str) / 1000)
        now = datetime.now()
        days_since_update = (now - last_updated).days

        # Return True if task is 30+ days old
        return days_since_update >= ARCHIVE_THRESHOLD_DAYS

    def add_task_comment(self, task_id: str, comment_text: str) -> bool:
        """Add a comment to a task"""
        try:
            response = requests.post(
                f'{BASE_URL}/task/{task_id}/comment',
                headers=self.headers,
                json={'comment_text': comment_text}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding comment to task {task_id}: {e}")
            return False

    def format_assignee_mentions(self, assignees: List[Dict]) -> str:
        """Format assignee mentions for comment"""
        if not assignees:
            return ""

        mentions = []
        for assignee in assignees:
            username = assignee.get('username', 'User')
            user_id = assignee.get('id')
            if user_id:
                mentions.append(f"@{username}")

        return " ".join(mentions) if mentions else ""

    def process_deadline_warning(self, alert: Dict) -> None:
        """Send deadline warning comment"""
        task = alert['task']
        task_id = task['id']
        task_name = task['name']
        hours_remaining = alert['hours_remaining']
        due_date = alert['due_date']

        # Create unique key for this reminder
        reminder_key = f"deadline_{task_id}_{due_date.date()}"

        # Skip if we've already sent this reminder
        if reminder_key in self.processed_reminders:
            return

        assignees = task.get('assignees', [])
        mentions = self.format_assignee_mentions(assignees)

        if hours_remaining < 24:
            urgency = "⚠️ URGENT"
            time_desc = f"{int(hours_remaining)} hours"
        else:
            urgency = "📅 Reminder"
            days = int(hours_remaining / 24)
            time_desc = f"{days} day{'s' if days > 1 else ''}"

        comment = f"""{urgency}: Deadline Approaching!

{mentions}

This task is due in **{time_desc}** ({due_date.strftime('%Y-%m-%d %H:%M')}).

Please update the status or adjust the deadline if needed."""

        print(f"⏰ {urgency}: {task_name} (due in {time_desc})")

        if self.add_task_comment(task_id, comment):
            self.processed_reminders.add(reminder_key)
            print(f"   ✓ Reminder sent to task {task_id}")

    def process_stale_task_warning(self, alert: Dict) -> None:
        """Send stale task warning comment"""
        task = alert['task']
        task_id = task['id']
        task_name = task['name']
        days_since_update = alert['days_since_update']
        last_updated = alert['last_updated']

        # Create unique key for this reminder (once per day)
        reminder_key = f"stale_{task_id}_{datetime.now().date()}"

        # Skip if we've already sent this reminder today
        if reminder_key in self.processed_reminders:
            return

        assignees = task.get('assignees', [])
        mentions = self.format_assignee_mentions(assignees)

        comment = f"""🔔 Task Update Reminder

{mentions}

This task hasn't been updated in **{days_since_update} day{'s' if days_since_update > 1 else ''}** (last update: {last_updated.strftime('%Y-%m-%d %H:%M')}).

Please provide a status update or move the task forward."""

        print(f"💤 Stale: {task_name} ({days_since_update} days since update)")

        if self.add_task_comment(task_id, comment):
            self.processed_reminders.add(reminder_key)
            print(f"   ✓ Reminder sent to task {task_id}")

    def monitor_once(self) -> Dict[str, int]:
        """Run a single monitoring check"""
        print(f"\n{'='*60}")
        print(f"🔍 Starting monitoring check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        tasks = self.get_all_tasks()

        deadline_alerts = []
        stale_alerts = []
        old_tasks_count = 0

        # Check each task
        for task in tasks:
            # Check for approaching deadlines
            deadline_alert = self.check_approaching_deadline(task)
            if deadline_alert:
                deadline_alerts.append(deadline_alert)

            # Check for stale tasks (7-30 days)
            stale_alert = self.check_stale_task(task)
            if stale_alert:
                stale_alerts.append(stale_alert)

            # Count old tasks (30+ days) - these should be archived
            if self.check_old_task(task):
                old_tasks_count += 1

        # Process alerts
        print(f"\n📊 Monitoring Results:")
        print(f"   Deadline warnings: {len(deadline_alerts)}")
        print(f"   Stale task warnings: {len(stale_alerts)} (7-30 days old)")
        if old_tasks_count > 0:
            print(f"   📦 Old tasks found: {old_tasks_count} (30+ days - ready for archive)")
        print()

        if deadline_alerts:
            print("\n⏰ Deadline Warnings:\n")
            for alert in deadline_alerts:
                self.process_deadline_warning(alert)

        if stale_alerts:
            print("\n💤 Stale Task Warnings:\n")
            for alert in stale_alerts:
                self.process_stale_task_warning(alert)

        if not deadline_alerts and not stale_alerts:
            print("✓ No alerts at this time - all tasks are on track!\n")

        # Notify user about old tasks that should be archived
        if old_tasks_count > 0:
            print(f"\n{'='*60}")
            print(f"📦 Archive Recommendation")
            print(f"{'='*60}")
            print(f"Found {old_tasks_count} tasks older than {ARCHIVE_THRESHOLD_DAYS} days.")
            print(f"These tasks are NOT receiving reminders.")
            print(f"\nTo move them to 'Task Archive - Needs Reviewed', run:")
            print(f"   python src\\archive_old_tasks.py")
            print(f"{'='*60}\n")

        return {
            'total_tasks': len(tasks),
            'deadline_warnings': len(deadline_alerts),
            'stale_warnings': len(stale_alerts),
            'old_tasks': old_tasks_count
        }


def main():
    # Validate environment variables
    if not CLICKUP_API_TOKEN:
        print("❌ Error: CLICKUP_API_TOKEN not found in environment")
        print("   Please set it in your .env file")
        return

    if not WORKSPACE_ID:
        print("❌ Error: WORKSPACE_ID not found in environment")
        print("   Please set it in your .env file")
        return

    # Create monitor instance
    monitor = ClickUpMonitor(CLICKUP_API_TOKEN, WORKSPACE_ID)

    # Run check once and exit
    monitor.monitor_once()


if __name__ == '__main__':
    main()
