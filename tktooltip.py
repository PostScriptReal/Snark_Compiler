#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Class for creating a tkinter tool tip.

The tool tip can be attached to any widget's mouse enter and leave events.
It displays the given text wrapped in a box of high contrast.

THIS IS A FORKED VERSION OF THE ORIGINAL CODE FROM https://github.com/DaedalicEntertainment/python-ui
THIS FORK ADDS THE ABILITY TO THEME THE TOOLTIP
'''

import tkinter as tk

###############################################################################


class ToolTip(object):

    def __init__(self, widget, text='tool tip', background='bisque', foreground='black'):
        self.widget = widget
        self.text = text
        self.bg = background
        self.fg = foreground
        if not self.text:
            self.widget.unbind('<Enter>')
            self.widget.unbind('<Leave>')
        else:
            self.widget.bind('<Enter>', self.enter)
            self.widget.bind('<Leave>', self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        # create a "window" that is just a label
        self.window = tk.Toplevel(self.widget)
        self.window.wm_overrideredirect(True)
        self.window.wm_geometry('+%d+%d' % (x, y))
        label = tk.Label(self.window, text=self.text, justify='left', padx=4, pady=2, wraplength=250,
            background=self.bg, foreground=self.fg, relief='flat', borderwidth=0)
        label.pack(ipadx=1)
    
    def changeTheme(self, background, foreground):
        self.bg = background
        self.fg = foreground

    def close(self, event=None):
        if self.window:
            self.window.destroy()
