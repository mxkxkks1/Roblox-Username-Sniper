import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor
import json
from colorama import init, Fore, Style

init(autoreset=True)

s = requests.Session()

def loadwords():
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
    r = requests.get(url)
    return [w for w in r.text.split() if 3 < len(w) < 20]

words = loadwords()

def gen():
    return random.choice(words).lower()

def check(u):
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-CSRF-TOKEN': s.cookies.get_dict().get('_csrf', ''),
    }
    r = s.get(f'https://auth.roblox.com/v1/usernames/validate?username={u}&birthday=2000-01-01&context=Signup', headers=h)
    if r.status_code == 200:
        resp = json.loads(r.text)
        if resp.get('code') == 0:
            print(f"{Fore.GREEN}Available: {u}")
            with open("available.txt", "a") as f:
                f.write(f"{u}\n")
        else:
            print(f"{Fore.RED}Taken: {u}")
    else:
        print(f"{Fore.YELLOW}Error: {u} - Status Code: {r.status_code}")

def main():
    # ASCII art
    ascii_art = """
    ╔═════════════════════════════════════════════╗
    ║  ____       _     _                         ║
    ║ |  _ \ ___ | |__ | | _____  __              ║
    ║ | |_) / _ \| '_ \| |/ _ \ \/ /              ║
    ║ |  _ < (_) | |_) | | (_) >  <               ║
    ║ |_| \_\___/|_.__/|_|\___/_/\_\              ║
    ║                                             ║
    ║           Username Checker                  ║
    ╚═════════════════════════════════════════════╝
    """
    print(Fore.CYAN + ascii_art)
    print(Fore.MAGENTA + Style.BRIGHT + "Made by mxkxkks\n")

    s.get('https://www.roblox.com/')  # Get initial cookies
    t = int(input(Fore.YELLOW + "Threads: "))
    print(Fore.CYAN + "\nStarting username check...\n")
    with ThreadPoolExecutor(max_workers=t) as e:
        while True:
            u = gen()
            e.submit(check, u)
            time.sleep(random.uniform(2, 4))

if __name__ == "__main__":
    main()
