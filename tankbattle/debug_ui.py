import tkinter as tk
from tkinter import ttk
import time
import psutil
import tracemalloc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DebugUI:
    def __init__(self, game, memory_monitor, frame_rate_analyzer, event_debugger):
        self.game = game
        self.memory_monitor = memory_monitor
        self.frame_rate_analyzer = frame_rate_analyzer
        self.event_debugger = event_debugger

        self.root = tk.Tk()
        self.root.title("Debug UI")

        self.create_game_state_inspector()
        self.create_performance_dashboard()
        self.create_memory_visualization()
        self.create_frame_rate_monitor()
        self.create_event_log_viewer()
        self.create_interactive_controls()

    def create_game_state_inspector(self):
        frame = ttk.LabelFrame(self.root, text="Game State Inspector")
        frame.pack(fill=tk.BOTH, expand=True)

        self.state_text = tk.Text(frame, height=10, width=50)
        self.state_text.pack(fill=tk.BOTH, expand=True)

        self.update_game_state()

    def update_game_state(self):
        self.state_text.delete(1.0, tk.END)
        for bot in self.game.bots:
            self.state_text.insert(tk.END, f"{bot.name} at {bot.position}, Health: {bot.health}, Fuel: {bot.fuel}\n")
        self.root.after(1000, self.update_game_state)

    def create_performance_dashboard(self):
        frame = ttk.LabelFrame(self.root, text="Performance Metrics")
        frame.pack(fill=tk.BOTH, expand=True)

        self.cpu_label = ttk.Label(frame, text="CPU Usage: 0%")
        self.cpu_label.pack()
        self.memory_label = ttk.Label(frame, text="Memory Usage: 0 MB")
        self.memory_label.pack()
        self.io_label = ttk.Label(frame, text="I/O Usage: 0 KB read, 0 KB write")
        self.io_label.pack()

        self.update_performance_metrics()

    def update_performance_metrics(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        io_counters = psutil.disk_io_counters()

        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.memory_label.config(text=f"Memory Usage: {memory_info.used / 1024 / 1024:.2f} MB")
        self.io_label.config(text=f"I/O Usage: {io_counters.read_bytes / 1024:.2f} KB read, {io_counters.write_bytes / 1024:.2f} KB write")

        self.root.after(1000, self.update_performance_metrics)

    def create_memory_visualization(self):
        frame = ttk.LabelFrame(self.root, text="Memory Usage Visualization")
        frame.pack(fill=tk.BOTH, expand=True)

        self.memory_fig, self.memory_ax = plt.subplots()
        self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, master=frame)
        self.memory_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_memory_visualization()

    def update_memory_visualization(self):
        self.memory_ax.clear()
        total, stats = self.memory_monitor.get_memory_usage()
        labels = [stat.traceback[0] for stat in stats[:10]]
        sizes = [stat.size for stat in stats[:10]]

        self.memory_ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        self.memory_ax.set_title(f"Memory Usage: {total / 1024 / 1024:.2f} MB")

        self.memory_canvas.draw()
        self.root.after(5000, self.update_memory_visualization)

    def create_frame_rate_monitor(self):
        frame = ttk.LabelFrame(self.root, text="Frame Rate Monitor")
        frame.pack(fill=tk.BOTH, expand=True)

        self.frame_rate_fig, self.frame_rate_ax = plt.subplots()
        self.frame_rate_canvas = FigureCanvasTkAgg(self.frame_rate_fig, master=frame)
        self.frame_rate_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_frame_rate_monitor()

    def update_frame_rate_monitor(self):
        self.frame_rate_ax.clear()
        self.frame_rate_ax.plot(self.frame_rate_analyzer.frame_times, label='Frame Times', color='blue')
        self.frame_rate_ax.axhline(y=0.1, color='red', linestyle='--', label='Drop Threshold')
        self.frame_rate_ax.set_title('Frame Rate Over Time')
        self.frame_rate_ax.set_xlabel('Frame')
        self.frame_rate_ax.set_ylabel('Time (s)')
        self.frame_rate_ax.legend()

        self.frame_rate_canvas.draw()
        self.root.after(1000, self.update_frame_rate_monitor)

    def create_event_log_viewer(self):
        frame = ttk.LabelFrame(self.root, text="Event Log Viewer")
        frame.pack(fill=tk.BOTH, expand=True)

        self.event_listbox = tk.Listbox(frame)
        self.event_listbox.pack(fill=tk.BOTH, expand=True)

        self.update_event_log()

    def update_event_log(self):
        self.event_listbox.delete(0, tk.END)
        for event in self.event_debugger.events:
            self.event_listbox.insert(tk.END, f"{event['timestamp']} - {event['event']}")
        self.root.after(1000, self.update_event_log)

    def create_interactive_controls(self):
        frame = ttk.LabelFrame(self.root, text="Interactive Controls")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Tank Name:").pack(side=tk.LEFT)
        self.tank_name_entry = ttk.Entry(frame)
        self.tank_name_entry.pack(side=tk.LEFT)

        ttk.Label(frame, text="New Position (x, y):").pack(side=tk.LEFT)
        self.position_entry = ttk.Entry(frame)
        self.position_entry.pack(side=tk.LEFT)

        ttk.Button(frame, text="Move Tank", command=self.move_tank).pack(side=tk.LEFT)

        ttk.Label(frame, text="New Health:").pack(side=tk.LEFT)
        self.health_entry = ttk.Entry(frame)
        self.health_entry.pack(side=tk.LEFT)

        ttk.Button(frame, text="Change Health", command=self.change_health).pack(side=tk.LEFT)

    def move_tank(self):
        tank_name = self.tank_name_entry.get()
        position = tuple(map(int, self.position_entry.get().split(',')))
        tank = self._find_tank_by_name(tank_name)
        if tank:
            tank.position = position
            print(f"{tank.name} moved to {tank.position}")

    def change_health(self):
        tank_name = self.tank_name_entry.get()
        health = int(self.health_entry.get())
        tank = self._find_tank_by_name(tank_name)
        if tank:
            tank.health = health
            print(f"{tank.name} health changed to {tank.health}")

    def _find_tank_by_name(self, name):
        for bot in self.game.bots:
            if bot.name == name:
                return bot
        return None

    def run(self):
        self.root.mainloop()
