import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import xml.etree.ElementTree as ET
import csv
import os
import threading
import time

class LogManagementUI:
    def __init__(self, root, log_file):
        self.root = root
        self.log_file = log_file
        self.logs = self._load_logs()

        self.root.title("Log Management UI")
        self.create_widgets()

    def _load_logs(self):
        with open(self.log_file, 'r') as file:
            return file.readlines()

    def create_widgets(self):
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(fill=tk.X)

        self.search_label = tk.Label(self.search_frame, text="Search:")
        self.search_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(fill=tk.X, padx=5, expand=True)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_logs)
        self.search_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack(fill=tk.X)

        self.filter_label = tk.Label(self.filter_frame, text="Filter by Level:")
        self.filter_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.filter_combobox = ttk.Combobox(self.filter_frame, values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.filter_combobox.pack(fill=tk.X, padx=5, expand=True)

        self.filter_button = tk.Button(self.filter_frame, text="Filter", command=self.filter_logs)
        self.filter_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.log_listbox = tk.Listbox(self.root)
        self.log_listbox.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

        self.export_frame = tk.Frame(self.root)
        self.export_frame.pack(fill=tk.X)

        self.export_label = tk.Label(self.export_frame, text="Export as:")
        self.export_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.export_combobox = ttk.Combobox(self.export_frame, values=["CSV", "JSON", "XML"])
        self.export_combobox.pack(fill=tk.X, padx=5, expand=True)

        self.export_button = tk.Button(self.export_frame, text="Export", command=self.export_logs)
        self.export_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.alert_frame = tk.Frame(self.root)
        self.alert_frame.pack(fill=tk.X)

        self.alert_label = tk.Label(self.alert_frame, text="Alert for Level:")
        self.alert_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.alert_combobox = ttk.Combobox(self.alert_frame, values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.alert_combobox.pack(fill=tk.X, padx=5, expand=True)

        self.alert_button = tk.Button(self.alert_frame, text="Set Alert", command=self.set_alert)
        self.alert_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.monitor_button = tk.Button(self.root, text="Start Monitoring", command=self.start_monitoring)
        self.monitor_button.pack(fill=tk.X, padx=5, pady=5)

    def search_logs(self):
        query = self.search_entry.get()
        results = [log for log in self.logs if query in log]
        self.update_log_listbox(results)

    def filter_logs(self):
        level = self.filter_combobox.get()
        results = [log for log in self.logs if f" - {level} - " in log]
        self.update_log_listbox(results)

    def update_log_listbox(self, logs):
        self.log_listbox.delete(0, tk.END)
        for log in logs:
            self.log_listbox.insert(tk.END, log)

    def export_logs(self):
        export_format = self.export_combobox.get()
        if export_format == "CSV":
            self.export_as_csv()
        elif export_format == "JSON":
            self.export_as_json()
        elif export_format == "XML":
            self.export_as_xml()

    def export_as_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Logger", "Level", "Message"])
                for log in self.logs:
                    parts = log.split(" - ")
                    writer.writerow(parts)

    def export_as_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'w') as file:
                json.dump(self.logs, file, indent=4)

    def export_as_xml(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if filename:
            root = ET.Element("logs")
            for log in self.logs:
                parts = log.split(" - ")
                log_element = ET.SubElement(root, "log")
                ET.SubElement(log_element, "timestamp").text = parts[0]
                ET.SubElement(log_element, "logger").text = parts[1]
                ET.SubElement(log_element, "level").text = parts[2]
                ET.SubElement(log_element, "message").text = parts[3]
            tree = ET.ElementTree(root)
            tree.write(filename)

    def set_alert(self):
        level = self.alert_combobox.get()
        self.alert_level = level
        messagebox.showinfo("Alert Set", f"Alert set for {level} level logs")

    def start_monitoring(self):
        self.monitoring = True
        self.monitor_button.config(text="Stop Monitoring", command=self.stop_monitoring)
        self.monitor_thread = threading.Thread(target=self.monitor_logs)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.monitoring = False
        self.monitor_button.config(text="Start Monitoring", command=self.start_monitoring)

    def monitor_logs(self):
        while self.monitoring:
            new_logs = self._load_logs()
            if len(new_logs) > len(self.logs):
                new_entries = new_logs[len(self.logs):]
                self.logs = new_logs
                self.update_log_listbox(self.logs)
                for log in new_entries:
                    if f" - {self.alert_level} - " in log:
                        messagebox.showwarning("Alert", f"New {self.alert_level} log entry detected:\n{log}")
            time.sleep(1)
