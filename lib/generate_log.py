import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def generate_log(data, output_directory="."):
    """Write each log entry to a date-stamped text file and return its path."""
    if not isinstance(data, list):
        raise ValueError("data must be a list")

    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
    output_path = Path(output_directory) / filename
    with output_path.open("w") as file:
        for entry in data:
            file.write(f"{entry}\n")

    print(f"Log written to {output_path}")
    return str(output_path)


@dataclass
class Task:
    title: str
    completed: bool = False


class UserAccount:
    """Owns the tasks belonging to one user."""

    def __init__(self, username):
        if not username.strip():
            raise ValueError("username cannot be empty")
        self.username = username
        self.tasks = {}

    def add_task(self, title):
        title = title.strip()
        if not title:
            raise ValueError("task title cannot be empty")
        if title in self.tasks:
            raise ValueError(f"task already exists: {title}")
        task = Task(title)
        self.tasks[title] = task
        return task

    def complete_task(self, title):
        try:
            task = self.tasks[title]
        except KeyError as error:
            raise KeyError(f"task not found: {title}") from error
        task.completed = True
        return task


def build_parser():
    parser = argparse.ArgumentParser(description="Manage tasks for a user account.")
    parser.add_argument("--user", default="default", help="account username")
    commands = parser.add_subparsers(dest="command", required=True)

    add_parser = commands.add_parser("add-task", help="add a task")
    add_parser.add_argument("title", help="task title")

    complete_parser = commands.add_parser("complete-task", help="complete a task")
    complete_parser.add_argument("title", help="task title")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    account = UserAccount(args.user)

    try:
        if args.command == "add-task":
            task = account.add_task(args.title)
            print(f"Added task for {account.username}: {task.title}")
        else:
            task = account.complete_task(args.title)
            print(f"Completed task for {account.username}: {task.title}")
    except (KeyError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
