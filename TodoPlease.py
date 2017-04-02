# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
import os.path
import json

def get_settings():
    return sublime.load_settings('TodoPlease.sublime-settings')

class TodoPlease(sublime_plugin.WindowCommand):

    def get_project_manager_projects(self):
        with open(os.path.join(sublime.packages_path(), 'User', 'Projects', 'recent.json')) as fp:
            return json.load(fp)

    def get_workspaces(self):
        with open(os.path.join(sublime.packages_path(), '..', 'Local', 'Session.sublime_session'),
                  encoding='utf-8') as fp:
            workspaces = json.load(fp).get('workspaces', {}).get('recent_workspaces')

        for workspace in workspaces:
            workspace = workspace[1] + ':' + workspace[2:-9] + 'project'
            yield workspace


    def get_projects_filenames(self):
        try:
            recent_project_files = self.get_project_manager_projects()
        except FileNotFoundError:
            recent_project_files = list(self.get_workspaces())

        project_filenames = []

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
        todo_names = get_settings().get('todo_names')

        projects = self.get_projects_filenames()
        self.todos = []
        for project in projects:
            for todo_name in todo_names:
                filename = os.path.join(project, todo_name)
                if os.path.isfile(filename):
                    self.todos.append([os.path.basename(project), '→ ' + filename])
                break

        if not projects:
            return
        self.window.show_quick_panel(self.todos, self.open_todo, on_highlight=self.preview_todo)
