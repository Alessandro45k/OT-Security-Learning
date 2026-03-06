import requests 

target_ip = "10.0.2.15"
port= "80"

wordlist = ["backup.sql", "config.bin", "firmware.zip", "secret_key"]
print(f"--- Starting Industrial Fuzzing on {target_ip} ---")

for directory in wordlist:
	url = f"http://{target_ip}:{port}/{directory}"
	try:

		response = requests.get(url)
		if response.status_code == 200:
			print (f"[SUCCES] Sensitive file found: {url}")
		elif response.status_code == 404:
			pass
	except requests.exceptions.ConnectionError:
		print("[ERROR] Connection refused. Is the server running?")
		break
print("---Scan Finished ---")	

import os 

loot_dir = "industrial_loot"

if  response.status_code == 200:
	print(f"[SUCCESS] Real file found: {url}")

	file_name = f"{loot_dir}/{directory}"
	with open(file_name, 'wb') as f:
		f.write(response.content)
	
	if b"<!DOCTYPE HTML" in response.content:
		print(f"[!] Warning: {directory} might be just a fake error page.")
elif response.status_code == 404:
	pass
