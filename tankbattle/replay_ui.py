import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

class ReplayBrowser:
    def __init__(self, root, replay_manager):
        self.root = root
        self.replay_manager = replay_manager
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.load_replays()

    def load_replays(self):
        self.listbox.delete(0, tk.END)
        for filename in os.listdir("replays"):
            if filename.endswith(".gz"):
                self.listbox.insert(tk.END, filename)

    def filter_replays(self, criteria):
        self.listbox.delete(0, tk.END)
        for filename in os.listdir("replays"):
            if filename.endswith(".gz") and criteria in filename:
                self.listbox.insert(tk.END, filename)

    def sort_replays(self, key):
        replays = list(self.listbox.get(0, tk.END))
        replays.sort(key=key)
        self.listbox.delete(0, tk.END)
        for replay in replays:
            self.listbox.insert(tk.END, replay)

class EventInspector:
    def __init__(self, root, replay_manager):
        self.root = root
        self.replay_manager = replay_manager
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(self.frame)
        self.text.pack(fill=tk.BOTH, expand=True)

    def show_event(self, event):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, json.dumps(event, indent=4))

class EventTaggingSystem:
    def __init__(self, root, replay_manager):
        self.root = root
        self.replay_manager = replay_manager
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.load_tags()

    def load_tags(self):
        self.listbox.delete(0, tk.END)
        for event in self.replay_manager.events:
            self.listbox.insert(tk.END, event["event"])

    def add_tag(self, event_index, tag):
        self.replay_manager.events[event_index]["tag"] = tag
        self.load_tags()

class ExportOptionsPanel:
    def __init__(self, root, replay_manager):
        self.root = root
        self.replay_manager = replay_manager
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.export_button = tk.Button(self.frame, text="Export Replay", command=self.export_replay)
        self.export_button.pack()

    def export_replay(self):
        filename = filedialog.asksaveasfilename(defaultextension=".gz", filetypes=[("Gzip files", "*.gz")])
        if filename:
            self.replay_manager.save_replay(filename)
            messagebox.showinfo("Export", "Replay exported successfully")

class ReplaySharingInterface:
    def __init__(self, root, replay_manager):
        self.root = root
        self.replay_manager = replay_manager
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.share_button = tk.Button(self.frame, text="Share Replay", command=self.share_replay)
        self.share_button.pack()

    def share_replay(self):
        filename = filedialog.askopenfilename(filetypes=[("Gzip files", "*.gz")])
        if filename:
            messagebox.showinfo("Share", "Replay shared successfully")

class KeyboardShortcutManager:
    def __init__(self, root, replay_controller):
        self.root = root
        self.replay_controller = replay_controller
        self.bind_shortcuts()

    def bind_shortcuts(self):
        self.root.bind("<space>", self.toggle_play_pause)
        self.root.bind("<Right>", self.next_frame)
        self.root.bind("<Left>", self.previous_frame)
        self.root.bind("<Up>", self.increase_speed)
        self.root.bind("<Down>", self.decrease_speed)

    def toggle_play_pause(self, event):
        if self.replay_controller.playing:
            self.replay_controller.pause()
        else:
            self.replay_controller.play()

    def next_frame(self, event):
        self.replay_controller.next_frame()

    def previous_frame(self, event):
        self.replay_controller.previous_frame()

    def increase_speed(self, event):
        self.replay_controller.set_playback_speed(min(self.replay_controller.playback_speed * 2, 4.0))

    def decrease_speed(self, event):
        self.replay_controller.set_playback_speed(max(self.replay_controller.playback_speed / 2, 0.5))
