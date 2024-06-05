from requests import get
from bs4 import BeautifulSoup as bs
import openpyxl
import random
from collections import defaultdict

def elections_scraper(link: str, name_output_file: str):

  # Vytvoří seznam variovaných částí url. 
  def get_numbers(link = link):
    
    # Získá data, z nichž se vydělí část, která se v každé url variuje.
    response = get ("https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ")
    divided_response = bs(response.text, features="html.parser")
    # Najde všechny 'td' elementy s třídou 'center'
    tds = divided_response.find_all('td', {'class': 'center'})

    # Vytvoří seznam variovaných částí url.
    global numbers
    numbers = []
    for td in tds:
      if td.text != "N":
    # Získá odkaz v rámci 'td' elementu
        a = td.find('a')
    # Získá hodnotu 'href' atributu
        href = a.get('href')
    # Rozdělí 'href' na části podle znaku '='
        if "ps32?" in href:
          parts = href
          numbers.append(parts.split("=")[3])
  get_numbers()  



# Vytvoří 14 vnořených seznamů variovaných částí url, které odpovídají 14 krajům.
  def get_counties_numbers(list = numbers):
    global counties_numbers
    counties_numbers = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for x, y in enumerate(numbers):
      
      if "1100" in y:
        x =0
        counties_numbers[x].append(y)
        
      elif "21" in y:
        x = 1
        counties_numbers[x].append(y)
      elif "31" in y:
        x = 2
        counties_numbers[x].append(y)  
      elif "32" in y:
        x = 3
        counties_numbers[x].append(y)
      elif "41" in y:
        x = 4
        counties_numbers[x].append(y)
      elif "42" in y:
        x = 5
        counties_numbers[x].append(y)
      elif "51" in y:
        x = 6
        counties_numbers[x].append(y)
      elif "52" in y:
        x = 7
        counties_numbers[x].append(y)
      elif "53" in y:
        x = 8
        counties_numbers[x].append(y)
      elif "61" in y:
        x = 9
        counties_numbers[x].append(y)
      elif "62" in y:
        x = 10
        counties_numbers[x].append(y)
      elif "71" in y:
        x = 11
        counties_numbers[x].append(y)
      elif "72" in y:
        x = 12
        counties_numbers[x].append(y)
      elif "81" in y:
        x = 13
        counties_numbers[x].append(y)
  get_counties_numbers()  

    
  # Vyhodnotí správnost či nesprávnost linku.  
  def link_assessment(link = link):
    # Uložení a rozdělení vzorového url, se kterým budou porovnávány všechn url zadané uživatelem.
    reference = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2110"
    first_county = 1
    last_county = 15
    reference_parts = [reference.split("=")[0]+"=", reference.split("=")[1]+"=", first_county, last_county, reference.split("=")[-2].split("&")[1]+"=", counties_numbers]
    
    # Vyhodnocení url zadaného uživatelem pomocí srovnání se vzorovým url.
    try:
      outcome = []
      if link.split("=")[0]+"=" == reference_parts[0] and link.split("=")[1]+"=" == reference_parts[1] and link.split("=")[-2].split("&")[1]+"=" == reference_parts[4]:
        
        for county in range(first_county, last_county):
          if float(link.split("=")[-2].split("&")[0]) == county and link.split("=")[-1] in reference_parts[5][county - 1]:
            outcome.append("the link verified")                 
        else:
          outcome.append("rejected")            

      else:
        outcome.append("rejected")

    except:
      outcome.append("rejected")

    global result_1
    result_1 = outcome[0]
    return result_1
  link_assessment()




# Vyhodnocení správnosti jména výsledného souboru
  def output_name_assessment(name = name_output_file):
    if ".xlsx" not in name:
      outcome = "rejected"
    else:
      outcome = "the name verified"
    global result_2
    result_2 = outcome
    return result_2
  output_name_assessment()


# Pomocná funkce, která ukládá výsledky prvního spuštění fce link_assessment a fce output_name_assessment
  def preserver():
    global preservation
    if result_1 == "the link verified" and result_2 == "the name verified":
      preservation = "verified"
    else:
      preservation = "rejected"
  preserver()


# Vyhodnucuje, zda nebyly správné vstupy zadány ve špatném pořadí.
  def position_assessment():
    link_assessment(name_output_file)
    output_name_assessment(link)
    global result_3
    if result_1 == "the link verified" and result_2 == "the name verified":
      result_3 = "Misplacements of arguments. Change their position. Terminating the program."
    else:
      result_3 = None
  position_assessment()

# Tiskne výsledky vyhodnocení a případně ukončuje program.
  def printer():
    if preservation == "rejected" and result_3 == "Misplacements of arguments. Change their position. Terminating the program.":
      print(result_3)
      exit()
    elif preservation == "verified":
      print(f"DOWNLOADING DATA FROM SELECTED URL: {link}")
    elif preservation == "rejected":
      print("The wrong input, terminating the program.")
      exit()
  printer()


# Vytvoří všechna url, z nichž budou stažena data do výsledného souboru.
  def generating_links(link = link) -> str:
# Ze zadaného url získá číslo kraje a číslo volebního okresu.
    divided_adress = link.split("=")
    county_code = divided_adress[-2].split("&")[0]
    muni_code = divided_adress[-1]

# Ze zadaného url získá data, z nichž budou vytvořena url vedoucím k datům,
# která budou zapsána do výsledného souboru.
    response = get(link)
    divided_response = bs(response.text, features="html.parser")
    # Najde všechny 'td' elementy s třídou 'center'
    tds = divided_response.find_all('td', {'class': 'cislo'})

    global link_muni
    link_muni = []
    for td in tds:
    # Získá odkaz v rámci 'td' elementu
      a = td.find('a')
    # Získá hodnotu 'href' atributu
      href = a.get('href')
    # Rozdělí 'href' na části podle znaku '='
      if "ps311?" in href:
        parts = href.split('&xvyber')[-2].split("=")
        link_muni.append(f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={county_code}&xobec={parts[-1]}&xvyber={muni_code}")
         
    return (link_muni)
  generating_links()


# Vytvoří hlavičky sloupců.
  def headers_maker():
# získání a úprava zdrojového kódu
    argument = link_muni[0]
    response = get(argument)
    divided_response = bs(response.text, features="html.parser")
# získání hlavičky
    global list_of_headers
    list_of_headers = ["code", "location", "registered", "envelops", "valid"]
    tds = divided_response.find_all('td', {'class': 'overflow_name'})
    for party in tds:
      list_of_headers.append(party.text)
    return list_of_headers
  headers_maker()


# Vytvoří řady.
  def rows_supplier():
    global rows
    rows = []
    supplier = link_muni
    for link_supply in supplier:
      temporary = []
      # získání a úprava zdrojového kódu
      response = get(link_supply)
      divided_response = bs(response.text, features="html.parser")
    # Získání kódu obce
      divs = divided_response.find("div", {"class":"tab_full_ps311"})  
      a = divs.find('a')
      href = a.get('href')
      if "ps311?" in href:
        parts = href.split('=')[-3].split("&XVYBER")
        temporary.append(parts[0])
    # Získání jména obce
      h3s = divided_response.find_all("h3")
      if h3s[0].text.split(":")[1].strip() == "Hlavní město Praha":
        temporary.append(h3s[1].text.split(":")[1].strip())
      else:
        temporary.append(h3s[2].text.split(":")[1].strip())
    # Získání počtu registrovaných voličů
      tds = divided_response.find('td', {"headers":"sa2"})
      if "\xa0" in tds.text:
        temporary.append(tds.text.split("\xa0")[0]+tds.text.split("\xa0")[1])
      else:
        temporary.append(tds.text)
    # Získání počtu odevzdaných obálek
      tds2 = divided_response.find('td', {"headers":"sa5"})
      if "\xa0" in tds2.text:
        temporary.append(tds2.text.split("\xa0")[0]+tds2.text.split("\xa0")[1])
      else:
        temporary.append(tds2.text)
    # Získání počtu platných hlasů
      tds3 = divided_response.find('td', {"headers":"sa6"})
      if "\xa0" in tds3.text:
        temporary.append(tds3.text.split("\xa0")[0]+tds3.text.split("\xa0")[1])
      else:
        temporary.append(tds3.text)
    # Získání počtu platných hlasů pro jednotlivé strany
      tds4 = divided_response.find_all('td', {"headers":"t1sa2 t1sb3"})
      for votes in tds4:
        if votes.text != "-" and "\xa0" in votes.text:
          temporary.append(votes.text.split("\xa0")[0]+votes.text.split("\xa0")[1])
        elif votes.text != "-":
          temporary.append(votes.text)
      tds5 = divided_response.find_all('td', {"headers":"t2sa2 t2sb3"})
      for votes_2 in tds5:
        if votes_2.text != "-" and "\xa0" in votes_2.text:
          temporary.append(votes_2.text.split("\xa0")[0]+votes_2.text.split("\xa0")[1])
        elif votes_2.text != "-": 
          temporary.append(votes_2.text)
    
      rows.append(temporary)

    return rows
  rows_supplier()


# Vytvoří výsledný soubor.
  def xlsx_maker():
  # zápis hlavičky, nastavení šířky sloupce
    wb = openpyxl.Workbook()
    ws = wb.active
    headers = list_of_headers
    ws.append(headers)
    for row in rows:
      ws.append(row)
    for col in ws.columns:
      max_length = 0
      column = col[0].column_letter # Získá písmeno sloupce.

      for cell in col:
        try:
          if len(str(cell.value)) > max_length:
            max_length = len(str(cell.value))
        except:
          pass
      adjusted_width = (max_length + 2)
      ws.column_dimensions[column].width = adjusted_width

# Uložení souboru
      wb.save(name_output_file)
    print(f"SAVING TO A FILE: {name_output_file}")
    print("TERMINATING THE PROGRAM")
  xlsx_maker()













# Vyvtoří scénář s náhodně generovanými správnými vstupy, scenář se chybními vstupy a scénář
# s náhodně generovanými správnými vstupy na chybných pozicích. Náhodně mezi nimi zvolí.

response = get ("https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ")
divided_response = bs(response.text, features="html.parser")

# Najdeme všechny 'td' elementy s třídou 'center'
tds = divided_response.find_all('td', {'class': 'center'})

# Vytvoří seznam čísel volebních okresů.
numbers = []
for td in tds:
  if td.text != "N":
    # Získáme odkaz v rámci 'td' elementu
    a = td.find('a')
    # Získáme hodnotu 'href' atributu
    href = a.get('href')
    # Rozdělíme 'href' na části podle znaku '='
    if "ps32?" in href:
        parts = href
        numbers.append(parts.split("=")[3])



# Vytvoří seznam měst, pod něž spadá daný volební okres.
headers = divided_response.find_all('td')
cities = []
for x in headers:
   if x.text != "X" and x.text != "N" and x.text != "Zahraničí" and "CZ" not in x.text:
    cities.append(x.text)


# Vytvoří seznam s vnořenými seznamy, které obsahují vnořené seznamy s číslem volebního okresu a jeho jménem.
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


# Náhodná volba čísla kraje.
counties_choice = random.choice(range(1, 15))

# Náhodná volba vnořeného seznamu s číslem volebního okresu a jeho jménem.
dict_numbers_and_cities = dict(numbers_and_cities)
dictionary_choice = dict_numbers_and_cities[counties_choice][random.choice(range(0, len(dict_numbers_and_cities[counties_choice])))]

# Náhodně vytvoří správné url a jméno výsledného souboru.
right_generated_link = f"https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj={counties_choice}&xnumnuts={dictionary_choice[0]}"
right_generated_name_file = f"{dictionary_choice[1]}.xlsx" 


#Chybné vstupy.
wrong_input = {1 : ["https://nesmyslnevolby.cz/", "U tří sumců"], 2 : ["5479213", "osobní číslo"], 3 : ["https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6206", "symboly"]}

# Náhodně zvolí mezi chybnými vstupy. 
keys_choice = random.choice(range(1, 4))
wrong_dict_choice = wrong_input[keys_choice]

# Vytvoří chybný vstup.
wrong_generated_link = wrong_dict_choice[0]
wrong_generated_name_file = wrong_dict_choice[1]



# Slovník chybný vstupů, správných vstupů a správných vstupů na chybných pozicích. 
inputs = {1 : [wrong_generated_link, wrong_generated_name_file], 2 : [right_generated_link, right_generated_name_file], 3 : [right_generated_name_file, right_generated_link]}

# Náhodně zvolí mezi vytvořenými scénáři.
if inputs:
  random_outcome = inputs[random.choice(range(1, 4))]
  generated_link = random_outcome[0]
  generated_name_file = random_outcome[1]


print(generated_link, generated_name_file)
elections_scraper(generated_link, generated_name_file)