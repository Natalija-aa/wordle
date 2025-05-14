import random
import requests #HTTP zahtjevi
from rich.markdown import Markdown
from rich.console import Console
from rich.theme import Theme
import time

def rules():
    game_rules = """
#WORDLE
##PRAVILA IGRE

Pogodi riječ od 5 slova u 6 pokušaja. Riječ mora biti imenica u jednini.
Slova se mogu ponavljati u riječi.
Boja kvadrata se mijenja nakon svakog pokušaja.

##BOJA KVADRATA
- Ako se slovo nalazi u rijeci, i na dobrom je mjestu, kvadrat postane zelen 🟩
- Ako se slovo nalazi u rijeci, ali nije na dobrom je mjestu, kvadrat postane zut 🟨
- Ako slovo nije urijeci, kvadrat postane bijl ⬜
(rijeci moraju biti na engleskom jeziku, jer ne postoji mnogo besplatnih javnih API servisa koji pružaju detaljne definicije reči na srpskom jeziku)
--- 
    """

    console = Console()
    rules = Markdown(game_rules)
    console.print(rules)

def target_word():
    with open(r"C:\Users\Korisnik\Desktop\wordle\wordle\five-letter-words.txt") as file:
        words = []

        for line in file:
            words.append(line.rstrip())
        
        word = random.choice(words)
        return word

def users_guess():
    guess = input("\nTvoja rijec: ").strip().lower()
    return check_guess(guess) 

def check_guess(word):
    if not word.isalpha():
        print("Rijec ne snije da sadrzi znakove koji nisu slova")
        return users_guess()
    
    if len(word) != 5:
        print("Rijec mora da sadrzi 5 slova. Pokusaj ponovi!")
        return users_guess()
    
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    res = requests.get(url)
    data = res.json()
    
    speech = []

    try:
        for i in data:
            for j in i["meanings"]:
                speech.append(j["partOfSpeech"])    #koja je vrsta rijeci

        if "noun" not in speech:
            print("Rijec mora biti imenica u jednini. Pkusaj ponovi!")
            return users_guess()
        
    except TypeError:
        print("Rijec nije u rijecniku. Pokusaj opet!")
        return users_guess()
    
    return word

def compare_words(target, guess, letters, i):
    guess_progress = [None] * 5
    target_counts = {}
    guess_counts = {}
    
    #broj ponavljanja slova u target rijeci
    for char in target:
        target_counts[char] = target_counts.get(char, 0) + 1    #0 ako ne postoji

    for n in range(5):
        if guess[n] == target[n]:
            guess_progress[n] = guess[n]
            target_counts[guess[n]] -= 1    #smanji broj preostalih slova
    
    for n in range(5):
        if guess[n] != target[n]:
            if guess[n] in target_counts and target_counts[guess[n]] > 0:
                guess_progress[n] = '?' #nije na dobrom mjestu
                target_counts[guess[n]] -= 1
            else:
                guess_progress[n] = " "
    
    for n in range(5):
        x = " " + guess[n] + " "
        if guess_progress[n] == guess[n]:
            letters[i][n] = {x: "correct"}
        elif guess_progress[n] == "?":
            letters[i][n] = {x: "wrong"}
        else:
            letters[i][n] = {x: "unable"}
    
    return letters

def compar_word_emoji(target, guess, emoji, i):
    guess_progress = [None] * 5
    target_counts = {}
    
    for char in target:
        target_counts[char] = target_counts.get(char, 0) + 1
    
    for n in range(5):
        if guess[n] == target[n]:
            guess_progress[n] = '🟩'
            target_counts[guess[n]] -= 1
    
    for n in range(5):
        if guess[n] != target[n]:
            if guess[n] in target_counts and target_counts[guess[n]] > 0:
                guess_progress[n] = '🟨'
                target_counts[guess[n]] -= 1
            else:
                guess_progress[n] = '⬜'
    
    for n in range(5):
        emoji[i][n] = guess_progress[n]
    
    return emoji

def victory(target, duration, name):
    min = f"{duration // 60:.0f}"   #// cjelobrojno djeljenje

    if min == "1":
        minutes = min + " minut"
    else:
        minutes = min + " minute"

    sec = f"{duration % 60:.0f}"

    if sec == "1":
        seconds = sec + " sekund"
    else:
        seconds = sec + " sekunde"

    print()
    text = f"""
# {name.upper()}, POGODILI STE RIJEC "{target.upper()}" u {minutes} {seconds}
    """

    console = Console()
    a = Markdown(text)
    console.print(a)

def loss(target, duration, name):
    min = f"{duration // 60:.0f}"   #// cjelobrojno djeljenje

    if min == "1":
        minutes = min + " minut"
    else:
        minutes = min + " minute"

    sec = f"{duration % 60:.0f}"

    if sec == "1":
        seconds = sec + " sekund"
    else:
        seconds = sec + " sekunde"

    
    print()
    text = f"""
# {name.upper()}, NISTE POGODILI RIJEC "{target.upper()}" 
##  {minutes} {seconds}
---
    """
    console = Console()
    b = Markdown(text)
    console.print(b)

def funkcija(letters, console_theme):
    #prikaz svih rezultata igre
    print()
    for word in letters:    #lista pokusaja
        for letter in word: #prolazi kroz slova
            for key, value in letter.items():   #"A":"correct"
                console_theme.print(key.upper(), style = value, end = "")
                console_theme.print(" ", end = "")  #razmak izmedju slova
        print()

def main():
    #game ruls
    rules()

    name = input("UNESI IME: ")
    line = """
---
"""
    console = Console()
    l_p = Markdown(line)
    console.print(l_p)

    start_time = time.time()    #vrijeme pocetka igre

    target = target_word()

    costum_theme = Theme({
        "correct": "bold white on green",
        "wrong": "bold white on yellow",
        "unable": "bold white on white",
        "default": "bold black on black"
    })

    console_theme = Console(theme=costum_theme)
    letters = [[{" ": "default"} for i in range(5)] for j in range(6)]
    emoji = [["⬜", "⬜", "⬜", "⬜", "⬜"] for k in range(6)]

    #pogadjanje rijeci 6 pokusaja
    for i in range(6):
        print()
        text = f"""
## POKUSAJ {i + 1}
        """

        round_n = Markdown(text)
        console.print(round_n)
        print()

        #prikaz pokusaja
        for word in letters:    #lista pokusaja
            for letter in word: #prolazi kroz slova
                for key, value in letter.items():   #"A":"correct"
                    console_theme.print(key.upper(), style = value, end = "")
                    console_theme.print(" ", end = "")  #razmak izmedju slova
            print()

        guess = users_guess()
        letters = compare_words(target, guess, letters, i)
        emoji = compar_word_emoji(target, guess, emoji, i)

        if target == guess: #ako je pogodjena rijec
            break

        end_time = time.time()  #vrijeme kraja igre
        t = end_time - start_time  # vrijeme trajanja igre

    funkcija(letters, console_theme)

    if target == guess:     
        victory(target, t, name)
    else:
        loss(target, t, name)

    
    
    x = """
## REZULTAT PARTIJE emoji
"""
    copy_e = Markdown(x)
    console.print(copy_e)

    for i in emoji:
        console.print(*i)   #iz jednog reda


if __name__ == "__main__":
    main()