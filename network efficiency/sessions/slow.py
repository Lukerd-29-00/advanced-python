import requests
import time

TOTAL_LENGTH = 0 #I'm being a bit lazy and using a global for demo purposes.
URL="https://pokeapi.co/api/v2/pokemon/{id}" #global constants are fine.

def grab_mon(id: int):
    global TOTAL_LENGTH
    res = requests.get(URL.format(id=id))
    if res.ok:
        TOTAL_LENGTH += int(res.headers["Content-Length"])
        return res.json()
    else:
        res.raise_for_status()

def grab_names(startID: int = 1, count: int = 100):
    output = []
    for id in range(startID,startID+count):
        output.append(grab_mon(id)["species"]["name"])
    return output

def timer():
    start = time.time()
    print(grab_names())
    return time.time() - start

if __name__ == "__main__":
    elapsed = timer()
    print(f"Time elapsed: {elapsed}")
    print(f"Downloaded: {TOTAL_LENGTH}")
    print(f"Average download rate: {round((TOTAL_LENGTH/1024)/elapsed)} kB/s")
