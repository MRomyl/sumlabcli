import argparse
import json
import os


class Task:
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

    def complete(self):
        self.completed = True
        print(f"✅ Task '{self.title}' marked as complete.")

    def to_dict(self):
        return {"title": self.title, "completed": self.completed}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["completed"])


class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f"📝 Task '{task.title}' added to project '{self.name}'.")

    def list_tasks(self):
        if not self.tasks:
            print(f"No tasks for project '{self.name}'.")
        for task in self.tasks:
            status = "✅" if task.completed else "❌"
            print(f"  {status} {task.title}")

    def to_dict(self):
        return {
            "name": self.name,
            "tasks": [t.to_dict() for t in self.tasks]
        }

    @classmethod
    def from_dict(cls, data):
        project = cls(data["name"])
        project.tasks = [Task.from_dict(t) for t in data["tasks"]]
        return project


class User:
    def __init__(self, name):
        self.name = name
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)
        print(f"📁 Project '{project.name}' added for user '{self.name}'.")

    def list_projects(self):
        if not self.projects:
            print(f"User '{self.name}' has no projects.")
        for p in self.projects:
            print(f"📂 {p.name}")

    def to_dict(self):
        return {
            "name": self.name,
            "projects": [p.to_dict() for p in self.projects]
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["name"])
        user.projects = [Project.from_dict(p) for p in data["projects"]]
        return user



DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return [User.from_dict(u) for u in data]

def save_data(users):
    with open(DATA_FILE, "w") as f:
        json.dump([u.to_dict() for u in users], f, indent=2)



def create_user(args):
    users = load_data()
    user = User(args.name)
    users.append(user)
    save_data(users)
    print(f"👤 User '{args.name}' created successfully!")

def list_users(args):
    users = load_data()
    if not users:
        print("No users found.")
    for user in users:
        print(f"👤 {user.name}")

def add_project(args):
    users = load_data()
    for user in users:
        if user.name == args.user:
            project = Project(args.project)
            user.add_project(project)
            save_data(users)
            return
    print(f"User '{args.user}' not found.")

def list_projects(args):
    users = load_data()
    for user in users:
        if user.name == args.user:
            user.list_projects()
            return
    print(f"User '{args.user}' not found.")

def add_task(args):
    users = load_data()
    for user in users:
        for project in user.projects:
            if project.name == args.project:
                project.add_task(Task(args.task))
                save_data(users)
                return
    print(f"Project '{args.project}' not found.")

def complete_task(args):
    users = load_data()
    for user in users:
        for project in user.projects:
            for task in project.tasks:
                if task.title == args.task:
                    task.complete()
                    save_data(users)
                    return
    print(f"Task '{args.task}' not found.")



parser = argparse.ArgumentParser(description="Project Management CLI Tool")
subparsers = parser.add_subparsers()

create_user_cmd = subparsers.add_parser("create_user", help="Create a new user")
create_user_cmd.add_argument("name", help="User name")
create_user_cmd.set_defaults(func=create_user)

list_users_cmd = subparsers.add_parser("list_users", help="List all users")
list_users_cmd.set_defaults(func=list_users)

add_project_cmd = subparsers.add_parser("add_project", help="Add a project to a user")
add_project_cmd.add_argument("user", help="User name")
add_project_cmd.add_argument("project", help="Project name")
add_project_cmd.set_defaults(func=add_project)

list_projects_cmd = subparsers.add_parser("list_projects", help="List projects for a user")
list_projects_cmd.add_argument("user", help="User name")
list_projects_cmd.set_defaults(func=list_projects)

add_task_cmd = subparsers.add_parser("add_task", help="Add a task to a project")
add_task_cmd.add_argument("project", help="Project name")
add_task_cmd.add_argument("task", help="Task title")
add_task_cmd.set_defaults(func=add_task)

complete_task_cmd = subparsers.add_parser("complete_task", help="Mark a task as complete")
complete_task_cmd.add_argument("task", help="Task title")
complete_task_cmd.set_defaults(func=complete_task)


if __name__ == "__main__":
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
