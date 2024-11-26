import subprocess
import requests
import os

res = requests.get("https://aaaaaaaaaaaaaa.pythonanywhere.com/download")
print(res.status_code)
if res.status_code == 200:
    with open("data.pickle", "wb") as f:
        f.write(res.content)
if os.path.exists("data.pickle"):
    with open("data.pickle", "rb") as f:
        print(requests.post("https://aaaaaaaaaaaaaa.pythonanywhere.com/upload", files={"file": f}).text)

for i in range(10):
    subprocess.run(["python", "tournament_loop.py"])
    with open("data.pickle", "rb") as f:
        requests.post("https://aaaaaaaaaaaaaa.pythonanywhere.com/upload", files={"file": f})