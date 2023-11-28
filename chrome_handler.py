import os
import subprocess
import time
import sys

def start_chrome():
    subprocess.Popen([r"D:\Chrome\chrome\chrome-win\chrome.exe",'--remote-debugging-port=9222','--user-data-dir=chromedata'],stdout = subprocess.PIPE, stderr = subprocess.PIPE)

def kill_chrome():
    # 根据操作系统选择适当的命令
    subprocess.run(['WMIC', 'PROCESS', 'WHERE', "CommandLine LIKE '%%chrome%%'", 'CALL', 'TERMINATE'], shell=True)

if __name__ == "__main__":
    if sys.argv[1] == "s":
        start_chrome()
    elif sys.argv[1] == "k":
        kill_chrome()