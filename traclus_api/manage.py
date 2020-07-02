import os
from flask import Flask
from flask_migrate import MigrateCommand
from flask_script import Manager
from app import create_app

env = os.environ.get("flask_env") or "default"
app = create_app(env)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
