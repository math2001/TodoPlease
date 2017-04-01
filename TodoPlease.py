# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
import os.path
import json

def openfile(*args, **kwargs):
    with open(*args, **kwargs) as fp:
        return fp

class TodoPlease(sublime_plugin.WindowCommand):

    def get_projects_filenames(self):
        project_filenames = []
        recents = os.path.join(sublime.packages_path(), 'User', 'Projects', 'recent.json')
        if not os.path.isfile(recents):
            return []
        with open(recents) as fp:
            recent_project_files = json.load(fp)
        for project_filename in recent_project_files:
            try:
                with open(project_filename) as fp:
                    folders = map(lambda obj: obj['path'], json.load(fp).get('folders', []))
            except FileNotFoundError:
                pass
            else:
                project_filenames += folders
        return project_filenames

    def run(self):
        todo_names = ['todo', '.todo']
        projects = self.get_projects_filenames()
        todos = []
        for project in projects:
            for todo_name in todo_names:
                filename = os.path.join(project, todo_name)
                if os.path.isfile(filename):
                    todos.append(filename)
                break

        print("TodoFinder.py:42", todos)

sublime.active_window().run_command('todo_please')
