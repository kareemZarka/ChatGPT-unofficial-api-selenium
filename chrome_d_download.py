import subprocess
import requests
import os
import zipfile
import shutil

# === Step 1: Function to get installed Chrome version ===
def get_installed_chrome_version():
    """Returns the installed Google Chrome version on macOS."""
    try:
        result = subprocess.run(
            ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().split(" ")[2]  # Extract version number
    except subprocess.CalledProcessError:
        print("[-] Error: Google Chrome is not installed or cannot be found.")
        exit(1)

# === Step 2: Fetch the latest Chromedriver version from Google API ===
def get_latest_chromedriver_version(chrome_version):
    """Fetch the latest stable Chromedriver version matching the installed Chrome version."""
    major_version = chrome_version.split(".")[0]  # Extract major version (e.g., 132)
    url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Find the closest matching Chromedriver version
        available_versions = [entry["version"] for entry in data["versions"] if entry["version"].startswith(major_version)]
        if not available_versions:
            print(f"[-] No matching Chromedriver found for Chrome {chrome_version}")
            exit(1)

        closest_version = max(available_versions)  # Get the highest available version
        return closest_version

    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching latest Chromedriver version: {e}")
        exit(1)

# === Step 3: Download the Chromedriver ZIP ===
def download_file(url, save_path):
    """Downloads the file and ensures it's valid."""
    try:
        print(f"[+] Downloading: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"[+] File downloaded: {save_path}")

        # Verify if file is actually a ZIP
        if not zipfile.is_zipfile(save_path):
            print("[-] Error: The downloaded file is not a valid ZIP. Retrying...")
            os.remove(save_path)
            return False
        return True

    except requests.exceptions.RequestException as e:
        print(f"[-] Download Error: {e}")
        return False

# === Step 4: Extract and Install Chromedriver ===
def extract_and_setup_chromedriver(zip_path):
    """Extracts the Chromedriver and moves it to the correct location."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("chromeDriver_zips")

    extracted_folder = "chromeDriver_zips/chromedriver-mac-x64"
    chromedriver_path = f"{extracted_folder}/chromedriver"

    if os.path.exists(chromedriver_path):
        shutil.move(chromedriver_path, "chromeDriver_zips/chromedriver")
        os.chmod("chromeDriver_zips/chromedriver", 0o755)  # Make it executable
        shutil.rmtree(extracted_folder)  # Clean up extracted folder
        print("[+] Chromedriver installed and set up successfully.")
    else:
        print("[-] Extraction failed! Chromedriver not found.")
        exit(1)

# === Step 5: Main Function to Install Chromedriver ===
def chromeDriverDownloader():
    print("[+] Detected System: Apple Mac")

    # Get installed Chrome version
    chrome_version = get_installed_chrome_version()
    print(f"[+] Installed Chrome version: {chrome_version}")

    # Get matching Chromedriver version
    driver_version = get_latest_chromedriver_version(chrome_version)
    print(f"[+] Downloading Chromedriver version: {driver_version}")

    # Construct the correct URL
    download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{driver_version}/mac-x64/chromedriver-mac-x64.zip"
    save_path = "chromeDriver_zips/chromedriver_mac64.zip"

    # Ensure download folder exists
    if not os.path.exists("chromeDriver_zips"):
        os.mkdir("chromeDriver_zips")

    # Download the Chromedriver ZIP
    if not download_file(download_url, save_path):
        print("[-] Failed to download a valid Chromedriver ZIP. Exiting.")
        exit(1)

    # Extract and set up Chromedriver
    extract_and_setup_chromedriver(save_path)

    # Verify installation
    os.system("chromeDriver_zips/chromedriver --version")

# Run the function
chromeDriverDownloader()
