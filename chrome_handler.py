import os
import subprocess
import time
import sys
import platform

def get_chrome_path():
    """Returns the path to the Chrome executable based on the OS."""
    os_name = platform.system().lower()
    
    if os_name == "darwin":  # macOS
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    elif os_name == "windows":
        chrome_32bit_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        chrome_64bit_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

        if os.path.exists(chrome_32bit_path):
            return chrome_32bit_path
        elif os.path.exists(chrome_64bit_path):
            return chrome_64bit_path
        else:
            raise FileNotFoundError("Chrome executable not found in either 32-bit or 64-bit directories.")
    
    elif os_name == "linux":
        return "/usr/bin/google-chrome"
    
    else:
        raise Exception(f"Unsupported OS: {os_name}")
    
def start_chrome():
    """Starts Chrome with remote debugging enabled."""
    chrome_path = get_chrome_path()
    print(f"[+] Starting Chrome from: {chrome_path}")
    subprocess.Popen([chrome_path, "--remote-debugging-port=9222", "--user-data-dir=chromedata"],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def kill_chrome():
    """Kills all Chrome processes safely."""
    os_name = platform.system().lower()

    try:
        if os_name == "darwin":  # macOS
            subprocess.run(["pkill", "-f", "Google Chrome"], check=True)
            print("[+] Google Chrome has been terminated.")

        elif os_name == "windows":
            subprocess.run(["taskkill", "/IM", "chrome.exe", "/F"], check=True)
            print("[+] Google Chrome has been terminated.")

        elif os_name == "linux":
            subprocess.run(["pkill", "-f", "google-chrome"], check=True)
            print("[+] Google Chrome has been terminated.")

        else:
            print("[-] Unsupported OS for automatic process termination.")

    except subprocess.CalledProcessError:
        print("[-] No running Chrome process found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chrome_handler.py [s|k]")
        print("s -> Start Chrome with remote debugging")
        print("k -> Kill all Chrome instances")
        sys.exit(1)

    if sys.argv[1] == "s":
        start_chrome()
    elif sys.argv[1] == "k":
        kill_chrome()
    else:
        print("Invalid option. Use 's' to start Chrome or 'k' to kill Chrome.")
