# Elections_scraper

Tento projekt je nástroj pro scraping výsledků voleb z webu `https://volby.cz`. Program načte volební data z webu a uloží je do souboru Excel. Formát excel jsem použil kvůli možnostem formátování výstupního souboru.

## Instalace

1. Nejprve nainstalujte všechny potřebné knihovny pomocí souboru `requirements.txt`. Můžete to udělat pomocí následujícího příkazu:

    ```sh
    pip install -r requirements.txt
    ```

2. Ujistěte se, že máte nainstalovány následující knihovny:
    - `requests`
    - `beautifulsoup4`
    - `openpyxl`

## Použití

Skript lze spustit přímo z příkazové řádky. Zde je ukázka, jak můžete použít skript:

```python
from requests import get
from bs4 import BeautifulSoup as bs
import openpyxl
import random
from collections import defaultdict

def elections_scraper(link: str, name_output_file: str):
    # ... (celý kód funkce elections_scraper)

## Generování odkazů pro správný a nesprávný vstup

response = get ("https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ")
divided_response = bs(response.text, features="html.parser")

tds = divided_response.find_all('td', {'class': 'center'})
numbers = []

for td in tds:
    if td.text != "N":
        a = td.find('a')
        href = a.get('href')
        if "ps32?" in href:
            parts = href
            numbers.append(parts.split("=")[3])

headers = divided_response.find_all('td')
cities = []
for x in headers:
    if x.text != "X" and x.text != "N" and x.text != "Zahraničí" and "CZ" not in x.text:
        cities.append(x.text)

numbers_and_cities = defaultdict(list)
for x, y in enumerate(numbers):
    if "1100" in y:
        numbers_and_cities[1].append([y, cities[x]])
    elif "21" in y:
        numbers_and_cities[2].append([y, cities[x]])
    elif "31" in y:
        numbers_and_cities[3].append([y, cities[x]])
    elif "32" in y:
        numbers_and_cities[4].append([y, cities[x]])
    elif "41" in y:
        numbers_and_cities[5].append([y, cities[x]])
    elif "42" in y:
        numbers_and_cities[6].append([y, cities[x]])
    elif "51" in y:
        numbers_and_cities[7].append([y, cities[x]])
    elif "52" in y:
        numbers_and_cities[8].append([y, cities[x]])
    elif "53" in y:
        numbers_and_cities[9].append([y, cities[x]])
    elif "61" in y:
        numbers_and_cities[10].append([y, cities[x]])
    elif "62" in y:
        numbers_and_cities[11].append([y, cities[x]])
    elif "71" in y:
        numbers_and_cities[12].append([y, cities[x]])
    elif "72" in y:
        numbers_and_cities[13].append([y, cities[x]])
    elif "81" in y:
        numbers_and_cities[14].append([y, cities[x]])

counties_choice = random.choice(range(1, 15))
dict_numbers_and_cities = dict(numbers_and_cities)
dictionary_choice = dict_numbers_and_cities[counties_choice][random.choice(range(0, len(dict_numbers_and_cities[counties_choice])))]
right_generated_link = f"https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj={counties_choice}&xnumnuts={dictionary_choice[0]}"
right_generated_name_file = f"{dictionary_choice[1]}.xlsx"

## Chybné vstupy

wrong_input = {1: ["https://nesmyslnevolby.cz/", "U tří sumců"], 2: ["5479213", "osobní číslo"], 3: ["https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6206", "symboly"]}
keys_choice = random.choice(range(1, 4))
wrong_dict_choice = wrong_input[keys_choice]
wrong_generated_link = wrong_dict_choice[0]
wrong_generated_name_file = wrong_dict_choice[1]

## Výběr vstupu

inputs = {1: [wrong_generated_link, wrong_generated_name_file], 2: [right_generated_link, right_generated_name_file], 3: [right_generated_name_file, right_generated_link]}
if inputs:
    random_outcome = inputs[random.choice(range(1, 4))]
    generated_link = random_outcome[0]
    generated_name_file = random_outcome[1]

print(generated_link, generated_name_file)
elections_scraper(generated_link, generated_name_file)


# Ukázka

# Správný vstup

generated_link = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100"
generated_name_file = "Praha.xlsx"
elections_scraper(generated_link, generated_name_file)

# Průběh stahování

DOWNLOADING DATA FROM SELECTED URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5304
SAVING TO A FILE: Ústí nad Orlicí.xlsx
TERMINATING THE PROGRAM

# Částečný výstup
code	location	registered	envelops	valid	Občanská demokratická strana
547981	Albrechtice	       368       214      214	 9
573426	Anenská Studánka   150        70	   69    5
553760	Běstovice	       353	     221	  218	24



# Nesprávný vstup
generated_link = "https://nesmyslnevolby.cz/"
generated_name_file = "U tří sumců"
elections_scraper(generated_link, generated_name_file)

# Výstup

The wrong input, terminating the program.



