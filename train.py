import subprocess
import requests
import os

res = requests.get("https://aaaaaaaaaaaaaa.pythonanywhere.com/download/data.pickle")
print(res.status_code)
if res.status_code == 200:
    with open("data.pickle", "wb") as f:
        f.write(res.content)

for i in range(100):
    subprocess.run(["python", "tournament_loop.py"])
    with open("data.pickle", "rb") as f:
        requests.post("https://aaaaaaaaaaaaaa.pythonanywhere.com/upload", files={"file": f})

    with open("best_weights.npy", "rb") as f:
        requests.post("https://aaaaaaaaaaaaaa.pythonanywhere.com/upload", files={"file": f})

# https://aaaaaaaaaaaaaa.pythonanywhere.com/download/best_weights.npy