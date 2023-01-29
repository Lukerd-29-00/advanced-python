import requests
import typing
import time

URL="https://pokeapi.co/api/v2/pokemon/{id}"

class PokemonSession(requests.Session):
    total_downloaded: int
    pokemon: typing.List[str]

    def __init__(self, startID: int = 1, count: int = 100):
        super(PokemonSession,self).__init__()
        self.total_downloaded = 0
        self.pokemon = self._download_range(startID,count)

    def _download(self, id: int):
        res = self.get(URL.format(id=id))
        if res.ok:
            self.total_downloaded += int(res.headers["Content-Length"])
            return res.json()
        else:
            res.raise_for_status()
    
    def _download_range(self, startID: int = 1, count: int = 100):
        output = []
        for id in range(startID,startID+count):
            output.append(self._download(id)["species"]["name"])
        return output

def timer():
    start = time.time()
    session = PokemonSession()
    print(session.pokemon)
    return session.total_downloaded, time.time() - start

if __name__ == "__main__":
    total_downloaded, elapsed = timer()
    print(f"Time elapsed: {elapsed}")
    print(f"Downloaded: {total_downloaded}")
    print(f"Average download rate: {round((total_downloaded/1024)/elapsed)} kB/s")
