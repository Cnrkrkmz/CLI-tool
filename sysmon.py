#!/usr/bin/env python3
#import argparse
import os
import psutil 
import time
import ctypes
import platform
import GPUtil
import datetime
from colorama import Fore, Style, init

init(autoreset=True)

#parser = argparse.ArgumentParser(description='System monitoring tool')

#parser.add_argument('--cpu', action='store_true', help='Shows CPU usage')
#parser.add_argument('--ram', action='store_true', help='Shows RAM usage')
#parser.add_argument('--disk', action='store_true', help='Shows disk usage')
#parser.add_argument('--uptime', action='store_true', help='Shows returns system boot time')
#parser.add_argument('--avgl', action='store_true', help='Shows average system load')
#parser.add_argument('--mcpu',action='store_true', help='Shows most used cpu process (must be used as sudo)')
#parser.add_argument('--gpu', action='store_true', help='Shows activity and degree of gpu')

#args = parser.parse_args()

def get_system_uptime():

    
    system=platform.system()
    if(system == "Linux"):
        t = os.popen('uptime -p').read()[:-1]
        #print(f"System uptime: {t}")
        return f"System uptime: {t}"

    
    elif(system == "Windows"):
        
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        now = datetime.datetime.now()
        uptime = now - boot_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        #print(f"{days} days, {hours:02}:{minutes:02}:{seconds:02}")
        return f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"

    elif(system == "Darwin"):
        t = os.popen('uptime').read()
        uptime_part = t.split(" up ")[1].split(",")
        up_time = uptime_part[0].strip()

        #print(f"System uptime: {up_time}")

        if(":" in up_time):
            hour_part = up_time.split(":")[0]
            min_part = up_time.split(":")[1]
            #print(f"{hour_part} hours, {min_part} minutes")
            return f"{hour_part} hours, {min_part} minutes"
            
        elif "day" in up_time:
            #print(f"System uptime: {up_time}")
            return f"System uptime: {up_time}"
        else:
            #print(f"System uptime: {up_time}")
            return f"System uptime: {up_time}"
    
    else:
        #print("Unsupported OS.")
        return "Unsupported OS."

def print_most_cpu_usage():

    
    for p in psutil.process_iter():
        try:
            p.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(1)

    util = list(psutil.process_iter(['pid', 'name', 'cpu_percent']))
    new_util = []
    for p in util:
        try:

            if p.info['cpu_percent'] is not None:
                new_util.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_util = sorted(new_util, key=lambda p: p.info['cpu_percent'], reverse=True) [:1]
    if top_util:
        p = top_util[0]
        return p.info['name'], p.info['cpu_percent']
    else:
        return "Unknown", 0.0

def ram_usage():

    
    ram_usage = psutil.virtual_memory().percent

    if(ram_usage >= 90):
        #print(Fore.RED +f"Warning high ram usage {ram_usage}")
        return f"Warning high ram usage {ram_usage}", "#E50F0F"
    else:
        #print(Fore.GREEN + f"RAM Usage: {ram_usage}")
        return f"RAM Usage: {ram_usage}", "#21FB04"

def cpu_usage():

    
    cpu_usage = psutil.cpu_percent(1)
    if(cpu_usage >= 85):
        #print(Fore.RED + f"Warning high cpu usage {cpu_usage}")
        return f"Warning high cpu usage {cpu_usage}" ,"#E50F0F"
    else:
        #print(Fore.GREEN + f"CPU usage: {cpu_usage}")
        return f"CPU usage: {cpu_usage}", "#21FB04"

def disk_usage():

    
    if platform.system() == "Windows":
        
        windows_c_disk_usage= psutil.disk_usage("C://").percent
        windows_d_disk_usage= psutil.disk_usage("D://").percent
        disk_usages = [windows_c_disk_usage, windows_d_disk_usage]

        
        for usages in disk_usages:

            if usages > 80:
                #print(Fore.RED + f"Warning: High disk usage {usages}")
                return f"Warning: High disk usage {usages}","#E50F0F"
            elif usages > 60:
                #print(Fore.YELLOW + f"Disk usage moderate: {usages}")
                return f"Disk usage moderate: {usages}","#FFE100FF"
            else:
                #print(Fore.GREEN + f"Disk usage: {usages}")
                return f"Disk usage: {usages}", "#21FB04"

    usage = psutil.disk_usage('/').percent
    if usage > 80:
        #print(Fore.RED + f"Warning: High disk usage {usage}")
        return f"Warning: High disk usage {usage}", "#E50F0F"
    elif usage > 60:
        #print(Fore.YELLOW + f"Disk usage moderate: {usage}")
        return f"Disk usage moderate: {usage}", "#FFE100FF"
    else:
        #print(Fore.GREEN + f"Disk usage: {usage}")
        return f"Disk usage: {usage}", "#21FB04"

def core_usage():

    
    if platform.system() == "Windows":
        #print("Load average not supported on Windows.")
        return "Load average not supported on Windows.", "cyan"
        
    
    if hasattr(psutil, "getloadavg"):

        load1, load5, load15 = psutil.getloadavg()
        core_count = os.cpu_count()
        if load1 > core_count:
            #print(Fore.RED + f"Warning: High system load - Load(1min): {load1:.2f} > CPU Cores: {core_count}")
            return f"Warning: High system load - Load(1min): {load1:.2f} > CPU Cores: {core_count}","#E50F0F"
        
        elif load1 > core_count * 0.7:
            #print(Fore.YELLOW + f"Load moderate: {load1:.2f} (1 min avg)")
            return f"Load moderate: {load1:.2f} (1 min avg)", "#FFE100FF"
        else:
            #print(Fore.GREEN + f"Load average (1, 5, 15 min): {load1:.2f}, {load5:.2f}, {load15:.2f}")
            return f"Load average (1, 5, 15 min): {load1:.2f}, {load5:.2f}, {load15:.2f}", "#21FB04"
    else:
        #print("Load average not supported on this OS.") 
        return "Load average not supported on this OS.", "cyan"

def gpu_usage_windows_nvidia():

    
    gpus= GPUtil.getGPUs()
    for gpu in gpus:
        usage = gpu.load * 100
        temp = gpu.temperature
        if usage > 90:
            #print(Fore.RED + f"GPU {gpu.name} - Usage: {usage:.1f}% | Temp: {temp}°C")
            return f"GPU {gpu.name} - Usage: {usage:.1f}% | Temp: {temp}°C", "#E50F0F"
        elif usage > 60:
            return f"GPU {gpu.name} - Usage: {usage:.1f}% | Temp: {temp}°C","#FFE100FF"
            #print(Fore.YELLOW + f"GPU {gpu.name} - Usage: {usage:.1f}% | Temp: {temp}°C")
        else:  
            #print(Fore.GREEN + f"GPU {gpu.name} - Usage: {usage:.1f}% | Temp: {temp}°C")
            return f"GPU {gpu.name} - Usage: {usage:.1f}% | Temp: {temp}°C", "#21FB04"

    return "No GPU detected", "cyan"



features = {
    'cpu': cpu_usage,
    
    'ram': ram_usage,
    
    'disk': disk_usage,
    
    'uptime':  get_system_uptime,
    
    'avgl': core_usage,
    
    'mcpu':  print_most_cpu_usage,

    'gpu': gpu_usage_windows_nvidia

    #'live': keep_live
}


