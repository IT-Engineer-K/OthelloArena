import requests

res = requests.get("https://aaaaaaaaaaaaaa.pythonanywhere.com/download/best_weights.npy")
print(res.status_code)
if res.status_code == 200:
    with open("best_weights.npy", "wb") as f:
        f.write(res.content)