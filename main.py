__author__ = 'di-erz'

import os
import glob
from kivy.app import App
from kivy.lang import Builder

from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListView, ListItemButton, ListItemLabel
from kivy.properties import (StringProperty)

data = []


class VideoListButton(ListItemButton):
    filename = StringProperty('')


args_converter = lambda row_index, rec: {'text': rec['text'],
                                         'size_hint_y': None,
                                         'height': 25,
                                         'filename': rec['filename']}

list_adapter = ListAdapter(data=[],
                           args_converter=args_converter,
                           cls=VideoListButton,
                           selection_mode='single',
                           allow_empty_selection=False)


class SimpleVideoPlayer(App):

    def __init__(self):
        self.root = Builder.load_file('main.kv')
        self.root.ids.path.bind(text=self.change_path)
        self.pattern = '*.mp4'
        self.root.ids.filelist.adapter = list_adapter
        self.root.ids.filelist.adapter.bind(
            on_selection_change=self.change_selection)

    def built(self):
        return self.root

    def change_selection(self, instance):
        if instance and instance.selection and instance.selection[0].filename:
            self.root.ids.videoplayer.source = instance.selection[0].filename
            self.root.ids.videoplayer.state = 'play'

    def change_path(self, instance, value):
        if not (value and os.path.isdir(value)):
            self.root.ids.filelist.adapter.data = [{'text': 'File not found',
                                                    'is_selected': False,
                                                    'filename': ''}]
            return
        self.filelist = glob.iglob(os.path.join(value, self.pattern))
        self.root.ids.filelist.adapter.data = [{'text': os.path.basename(f),
                                                'is_selected': False,
                                                'filename': f} for f in self.filelist]


if __name__ == '__main__':
    SimpleVideoPlayer().run()
