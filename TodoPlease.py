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

    def open_todo(self, index):
        if index == -1:
            self.window.run_command('close')
            return
        self.window.open_file(self.todos[index][1][2:])

    def preview_todo(self, index):
        self.window.open_file(self.todos[index][1][2:], sublime.TRANSIENT)

    def run(self):
        todo_names = ['todo', '.todo']
        projects = self.get_projects_filenames()
        self.todos = []
        for project in projects:
            for todo_name in todo_names:
                filename = os.path.join(project, todo_name)
                if os.path.isfile(filename):
                    self.todos.append([os.path.basename(project), '→ ' + filename])
                break

        self.window.show_quick_panel(self.todos, self.open_todo, on_highlight=self.preview_todo)
