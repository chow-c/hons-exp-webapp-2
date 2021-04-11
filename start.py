import os
import subprocess
import time

root_dir = os.getcwd()

print("Launching coffee server for Eyetribe collection")
os.chdir(os.path.join(root_dir, "eyetribe-websocket-master"))
os.system("start coffee server.coffee")
time.sleep(2)

print("Launching flask server for webpage display")
os.chdir(root_dir)
subprocess.Popen(
    [os.path.join(root_dir, "Scripts\\python.exe"), os.path.join(root_dir, "run.py")],
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
time.sleep(2)

print("Launching neulog api")
subprocess.Popen([r"C:\neulog_api\neulog_api.exe"])
time.sleep(2)

print("Launching EyeTribe Server")
subprocess.Popen(
    [r"C:\Program Files (x86)\EyeTribe\Server\EyeTribe.exe"],
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
time.sleep(2)

print("Launching Chrome in kiosk mode")
CHROME = os.path.join(
    "C:\\", "Program Files (x86)", "Google", "Chrome", "Application", "chrome.exe"
)
subprocess.Popen([CHROME, "--incognito", "--kiosk", "http://localhost:5000"])
time.sleep(2)
