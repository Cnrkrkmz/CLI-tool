import tkinter as tk
from tkinter import ttk
import sysmon
import platform

root = tk.Tk()

import platform

system_name = platform.system()
architecture = platform.machine()
processor_name = platform.processor()
system_version_short = platform.mac_ver()[0] if system_name == "Darwin" else platform.version()

system_info_text = f"{system_name} {architecture} | {processor_name} | Version: {system_version_short}"

style = ttk.Style()
style.theme_use('default')

style.configure("green.Horizontal.TProgressbar", troughcolor='#3e3e3e', background='limegreen')
style.configure("yellow.Horizontal.TProgressbar", troughcolor='#3e3e3e', background='gold')
style.configure("blue.Horizontal.TProgressbar", troughcolor='#3e3e3e', background='dodgerblue')
style.configure("red.Horizontal.TProgressbar", troughcolor='#3e3e3e', background='orangered')

main_frame = tk.Frame(root, bg="#323232")
main_frame.pack(padx=20, pady=20, anchor="nw") 


cpu_label = tk.Label(main_frame, font=("Courier", 14), bg="#323232", fg="white")
cpu_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
cpu_bar = ttk.Progressbar(main_frame, style="green.Horizontal.TProgressbar", orient="horizontal", length=300, mode="determinate", maximum=100)
cpu_bar.grid(row=0, column=1, padx=5)

ram_label = tk.Label(main_frame, font=("Courier", 14), bg="#323232", fg="white")
ram_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
ram_bar = ttk.Progressbar(main_frame, style="yellow.Horizontal.TProgressbar", orient="horizontal", length=300, mode="determinate", maximum=100)
ram_bar.grid(row=1, column=1, padx=5)

disk_label = tk.Label(main_frame, font=("Courier", 14), bg="#323232", fg="white")
disk_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
disk_bar = ttk.Progressbar(main_frame, style="blue.Horizontal.TProgressbar", orient="horizontal", length=300, mode="determinate", maximum=100)
disk_bar.grid(row=2, column=1, padx=5)

gpu_label = tk.Label(main_frame, font=("Courier", 14), bg="#323232", fg="white")
gpu_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
gpu_bar = ttk.Progressbar(main_frame, style="red.Horizontal.TProgressbar", orient="horizontal", length=300, mode="determinate", maximum=100)
gpu_bar.grid(row=3, column=1, padx=5)

uptime_label = tk.Label(main_frame, font=("Courier", 14), bg="#323232", fg="white")
uptime_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=10)

core_label = tk.Label(main_frame, font=("Courier", 14), bg="#323232", fg="white")
core_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=5)

mcpu_label = tk.Label(main_frame, font=("Courier", 14), bg="#323232", fg="white")
mcpu_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=5, pady=5)


def extract_percent(text):
    
    for part in text.split():
        try:
            return float(part)
        except ValueError:
            continue
    return 0.0

def update_stats():
    try:

        cpu_text, cpu_color = sysmon.cpu_usage()
        ram_text, ram_color = sysmon.ram_usage()
        uptime_text = sysmon.get_system_uptime()
        disk_text, disk_color = sysmon.disk_usage()
        core_text, core_color = sysmon.core_usage()
        gpu_text, gpu_color = sysmon.gpu_usage_windows_nvidia()
        most_cpu_app, mcpu_percent = sysmon.print_most_cpu_usage()

        # CPU
        cpu_label.config(text=cpu_text, fg=cpu_color)
        cpu_bar['value'] = extract_percent(cpu_text)

        # RAM
        ram_label.config(text=ram_text, fg=ram_color)
        ram_bar['value'] = extract_percent(ram_text)

        # Disk
        disk_label.config(text=disk_text, fg=disk_color)
        disk_bar['value'] = extract_percent(disk_text)

        # GPU
        gpu_label.config(text=gpu_text, fg=gpu_color)
        gpu_bar['value'] = extract_percent(gpu_text)

       
        uptime_label.config(text=f"Uptime: {uptime_text}")
        core_label.config(text=core_text, fg=core_color)
        mcpu_label.config(text=f"Most CPU usage: {most_cpu_app} ({mcpu_percent:.2f}%)")

    except Exception as e:
        print("Hata: ",e)
    root.after(5000, update_stats)

footer_frame = tk.Frame(root, bg="#2a2a2a")
footer_frame.pack(fill="x", side="bottom")

system_info_label = tk.Label(
    footer_frame, 
    text=system_info_text, 
    font=("Courier", 10), 
    fg="white", 
    bg="#2a2a2a",
    anchor="w",
    padx=10,
    pady=5
)
system_info_label.pack(fill="x")

root.geometry("600x400")
root.configure(bg="#323232")
root.title("SysMon")
update_stats()
root.mainloop()