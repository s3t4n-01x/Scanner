import os
import re
import whois
import dns.resolver
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init
from getpass import getpass

init(autoreset=True)

# ------------------ LOAD PASSWORD ------------------ #
def load_password():
    if not os.path.exists("config.conf"):
        print(Fore.RED + "File config.conf tidak ditemukan!")
        exit()
    with open("config.conf", "r") as f:
        for line in f:
            if line.startswith("PASSWORD="):
                return line.strip().split("=", 1)[1]
    print(Fore.RED + "Password tidak ditemukan di config.conf!")
    exit()

PASSWORD = load_password()

# ------------------ SCAN FUNCTIONS ------------------ #
def whois_scan(domain):
    try:
        data = whois.whois(domain)
        print(Fore.GREEN + "[WHOIS RESULT]")
        for k, v in data.items():
            print(f"{k}: {v}")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

def dns_scan(domain):
    record_types = ["A", "AAAA", "MX", "NS", "TXT"]
    print(Fore.GREEN + "[DNS RESULT]")

    # Disable auto load resolv.conf
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ["8.8.8.8", "1.1.1.1"]  # DNS Google dan Cloudflare

    for rtype in record_types:
        try:
            answers = resolver.resolve(domain, rtype)
            for rdata in answers:
                print(f"{rtype}: {rdata}")
        except dns.resolver.NoAnswer:
            print(Fore.YELLOW + f"{rtype}: Tidak ditemukan")
        except Exception as e:
            print(Fore.RED + f"{rtype}: Error ({e})")
            
def email_harvester(domain):
    urls = [f"http://{domain}", f"https://{domain}"]
    emails_found = set()
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text()
            emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
            emails_found.update(emails)
            for link in soup.find_all("a", href=True):
                if "mailto:" in link["href"]:
                    emails_found.add(link["href"].replace("mailto:", ""))
        except requests.RequestException:
            pass
    if emails_found:
        print(Fore.GREEN + "[EMAIL FOUND]")
        for email in emails_found:
            print(email)
    else:
        print(Fore.YELLOW + "Tidak ada email ditemukan")

def social_media_scan(domain):
    platforms = {
        "Facebook": f"https://www.facebook.com/{domain}",
        "Twitter": f"https://twitter.com/{domain}",
        "Instagram": f"https://www.instagram.com/{domain}",
        "LinkedIn": f"https://www.linkedin.com/company/{domain}"
    }
    print(Fore.GREEN + "[SOCIAL MEDIA CHECK]")
    for name, url in platforms.items():
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                print(Fore.GREEN + f"{name}: DITEMUKAN ({url})")
            else:
                print(Fore.YELLOW + f"{name}: Tidak ditemukan")
        except:
            print(Fore.YELLOW + f"{name}: Tidak ditemukan")

# ------------------ MAIN PROGRAM ------------------ #
def clear():
    os.system("cls" if os.name == "nt" else "clear")

clear()
print(Fore.CYAN + "=" * 50)
print(Fore.GREEN + r"""

   __________________ __  _   __      ____ ____  __
  / ___/__  /_  __/ // / / | / /     / __ <  / |/ /
  \__ \ /_ < / / / // /_/  |/ /_____/ / / / /|   / 
 ___/ /__/ // / /__  __/ /|  /_____/ /_/ / //   |  
/____/____//_/    /_/ /_/ |_/      \____/_//_/|_|  
                    𝕯𝖊𝖛𝖊𝖑𝖔𝖕𝖊𝖗 𝕭𝖔𝖙
""")
print(Fore.CYAN + "=" * 50)

# Login
while True:
    pwd = getpass(Fore.GREEN + "Masukkan password: ")
    if pwd == PASSWORD:
        print(Fore.GREEN + "Login berhasil!")
        break
    else:
        print(Fore.RED + "Password salah!")

# Banner Welcome Back
clear()
print(Fore.GREEN + r"""

   _____ _________    _   __      ____  ____  __  ______    _____   __
  / ___// ____/   |  / | / /     / __ \/ __ \/  |/  /   |  /  _/ | / /
  \__ \/ /   / /| | /  |/ /_____/ / / / / / / /|_/ / /| |  / //  |/ / 
 ___/ / /___/ ___ |/ /|  /_____/ /_/ / /_/ / /  / / ___ |_/ // /|  /  
/____/\____/_/  |_/_/ |_/     /_____/\____/_/  /_/_/  |_/___/_/ |_/   
                             𝕭𝖞 𝕾3𝕿4𝕹-01𝖃
""")
print(Fore.YELLOW + "WELCOME BACK!\n")

# Validasi domain
while True:
    domain = input(Fore.GREEN + "Masukkan domain (contoh: example.com): ").strip()
    pattern = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    if re.match(pattern, domain):
        break
    else:
        print(Fore.RED + "Domain tidak valid! Coba lagi.")

# Menu
while True:
    clear()
    print(Fore.WHITE + "Target: " + Fore.GREEN + domain)
    print(Fore.CYAN + "\n--- MENU ---")
    print("1. Whois Scan")
    print("2. DNS Scan")
    print("3. Email Harvester")
    print("4. Social Media Scan")
    print("5. Keluar")

    pilih = input(Fore.WHITE + "Pilih menu: ")

    if pilih == "1":
        whois_scan(domain)
    elif pilih == "2":
        dns_scan(domain)
    elif pilih == "3":
        email_harvester(domain)
    elif pilih == "4":
        social_media_scan(domain)
    elif pilih == "5":
        print(Fore.GREEN + "Keluar...")
        break
    else:
        print(Fore.RED + "Pilihan tidak valid!")

    input(Fore.CYAN + "\nTekan ENTER untuk kembali ke menu...")