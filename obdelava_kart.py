import random
import os
import sys
from textwrap import dedent
from pprint import pprint
from karte import pridobi_karte_vse_izris, igralne_karte


def izberi_igralca_za_igro(igralci: list[str], razdeli=True, karte_med_igralci=None, talon=None) -> str:
    
    if razdeli:
        talon,karte_med_igralci = razdeli_karte(igralci)
    
    visoki_taroki = [
        "sk",
        "21",
        "20",
        "19",
        "18",
        "17",
        "16",
        "15"
    ]
    
    vTR_igralca = {}
    vTR_igralca = {igralec: {} for igralec in igralci}
    for igralec in igralci:
        vTR_igralca[igralec]["visoki taroki"] = 0
        for i in visoki_taroki:
            if i in karte_med_igralci[igralec]["tarok"]:
                vTR_igralca[igralec]["visoki taroki"] += 1
    #pprint(karte_med_igralci)
    #pprint(vTR_igralca)
    
    igralec_z_najv_TR = "igralec", 0
    
    for igralec in igralci:
        if vTR_igralca[igralec]["visoki taroki"] >= igralec_z_najv_TR[1]: #SPREMENI, DA SE NA PODLAGI BARV ODLOČI!
            igralec_z_najv_TR = igralec,vTR_igralca[igralec]["visoki taroki"]

        #elif vTR_igralca[igralec]["visoki taroki"] == igralec_z_najv_TR[1]:
    
    igralec_z_najv_TR = str(igralec_z_najv_TR[0])
    return talon, igralec_z_najv_TR, karte_med_igralci# PREJ igralec_z_najv_TR[0] #!!!!!!!!!!!!!!!VRNE NEPRAVILNO NAJVTR !!!!!!!!!!!
    
def vse_karte_pridobi():
        vse_karte = {
        "srce" : {
            "k" : 8,
            "d" : 7,
            "s" : 6,
            "p" : 5,
            "1" : 4,
            "2" : 3,
            "3" : 2,
            "4" : 1
        },
        
        "kara" : {
            "k" : 8,
            "d" : 7,
            "s" : 6,
            "p" : 5,
            "1" : 4,
            "2" : 3,
            "3" : 2,
            "4" : 1
            
        },
        
        "pik" : {
            "k" : 8,
            "d" : 7,
            "s" : 6,
            "p" : 5,
            "10" : 4,
            "9" : 3,
            "8" : 2,
            "7" : 1            
        },
        
        "križ" : {
            "k" : 8,
            "d" : 7,
            "s" : 6,
            "p" : 5,
            "10" : 4,
            "9" : 3,
            "8" : 2,
            "7" : 1           
        },
        
       "tarok": {
            "sk": 22,
            "21": 21,
            "20": 20,
            "19": 19,
            "18": 18,
            "17": 17,
            "16": 16,
            "15": 15,
            "14": 14,
            "13": 13,
            "12": 12,
            "11": 11,
            "10": 10,
            "9": 9,
            "8": 8,
            "7": 7,
            "6": 6,
            "5": 5,
            "4": 4,
            "3": 3,
            "2": 2,
            "1": 1
            }
    }
        return vse_karte


def razdeli_karte(igralci):
    
    vse_karte = vse_karte_pridobi()
    
    
    karte = ["srce", "kara", "pik", "križ"]
    karte_med_igralci = {igralec: {} for igralec in igralci} #G

#G

    kup = []

    for barva, karte in vse_karte.items():
        for vrednost, podatek in karte.items():
            kup.append((barva, vrednost, podatek))

    random.shuffle(kup)

    razdeljene_karte = kup[:-6]
    talon = kup[-6:]

    for i, (barva, vrednost, podatek) in enumerate(razdeljene_karte):
        igralec = igralci[i % len(igralci)]

        if barva not in karte_med_igralci[igralec]:
            karte_med_igralci[igralec][barva] = []

        karte_med_igralci[igralec][barva].append(vrednost)

#G


    return talon, karte_med_igralci
    



# ============================================================
# KARTE
# ============================================================


def izberi_karto_v_roki(
    karte,
    needed_color,
    zamik=6,
    visina_kazalca=1
):
    if not karte:
        raise ValueError("Ni kart za izbiro.")

    # Če na mizi ni kart (needed_color je None ali ""), lahko izbereš katero koli karto
    if not needed_color:
        dovoljene_karte = {
            barva: vrednosti
            for barva, vrednosti in karte.items()
            if vrednosti
        }
    # Če imaš zahtevano barvo na mizi, moraš igrati to barvo
    elif needed_color in karte and karte[needed_color]:
        dovoljene_karte = {needed_color: karte[needed_color]}
    # Če nimaš zahtevane barve, moraš (če jih imaš) igrati taroka
    elif "tarok" in karte and karte["tarok"]:
        dovoljene_karte = {"tarok": karte["tarok"]}
    # Če nimaš niti zahtevane barve niti taroka, lahko odigraš poljubno karto
    else:
        dovoljene_karte = {
            barva: vrednosti
            for barva, vrednosti in karte.items()
            if vrednosti
        }

    imena_kart = []
    for barva, vrednosti in dovoljene_karte.items():
        for vrednost in vrednosti:
            imena_kart.append(f"{barva}_{vrednost}")

    if not imena_kart:
        raise ValueError("Ni dovoljenih kart za izbiro.")

    ascii_karte = []
    for ime in imena_kart:
        vrstica = igralne_karte(ime).splitlines()
        ascii_karte.append(vrstica)

    visina = max(len(karta) for karta in ascii_karte)
    sirina = max(
        len(vrstica)
        for karta in ascii_karte
        for vrstica in karta
    )

    for karta in ascii_karte:
        for i in range(len(karta)):
            karta[i] = karta[i].ljust(sirina)
        while len(karta) < visina:
            karta.append(" " * sirina)

    stevilo_kart = len(ascii_karte)
    x_pozicije = [i * zamik for i in range(stevilo_kart)]
    sirina_platna = x_pozicije[-1] + sirina
    izbran = min(5, stevilo_kart - 1)
    premik = 1
    zgornji_prostor = visina_kazalca + premik
    zamik_y = zgornji_prostor

    def novo_platno():
        return [
            [" "] * sirina_platna
            for _ in range(zgornji_prostor + visina + visina_kazalca)
        ]

    def narisi_normalne_karte(platno):
        for i, karta in enumerate(ascii_karte):
            if i == izbran:
                continue
            x = x_pozicije[i]
            vidna_sirina = (
                sirina if i == stevilo_kart - 1 else min(zamik, sirina)
            )
            for r, vrstica in enumerate(karta):
                py = zamik_y + r
                for c in range(vidna_sirina):
                    znak = vrstica[c]
                    if znak == " ":
                        continue
                    px = x + c
                    if 0 <= px < sirina_platna and 0 <= py < len(platno):
                        platno[py][px] = znak

    def narisi_izbrano_karto(platno):
        karta = ascii_karte[izbran]
        x = x_pozicije[izbran]
        for r, vrstica in enumerate(karta):
            py = zamik_y + r - premik
            for c in range(sirina):
                znak = vrstica[c]
                px = x + c
                if 0 <= px < sirina_platna and 0 <= py < len(platno):
                    platno[py][px] = znak

    def narisi_kazalec(platno):
        x = x_pozicije[izbran]
        py_zgoraj = zamik_y - premik - 1
        for c in range(sirina):
            px = x + c
            if 0 <= px < sirina_platna and 0 <= py_zgoraj < len(platno):
                platno[py_zgoraj][px] = "v"

        py_spodaj = zamik_y + visina - premik
        for c in range(sirina):
            px = x + c
            if 0 <= px < sirina_platna and 0 <= py_spodaj < len(platno):
                platno[py_spodaj][px] = "^"

    def izrisi():
        if hasattr(izrisi, "stevilo_vrstic"):
            print(f"\033[{izrisi.stevilo_vrstic}A", end="")

        platno = novo_platno()
        narisi_normalne_karte(platno)
        narisi_izbrano_karto(platno)
        narisi_kazalec(platno)

        for vrstica in platno:
            print("\r\033[2K" + "".join(vrstica), end="\n")

        print("\r\033[2K<- / -> izbira    ENTER potrdi    ESC izhod", end="\n")
        izrisi.stevilo_vrstic = len(platno) + 1

    def beri_tipko():
        if os.name == "nt":
            import msvcrt

            znak = msvcrt.getch()
            if znak in (b"\xe0", b"\x00"):
                znak2 = msvcrt.getch()
                if znak2 == b"K":
                    return "LEVO"
                if znak2 == b"M":
                    return "DESNO"
                return None
            if znak in (b"\r", b"\n"):
                return "ENTER"
            if znak == b"\x1b":
                return "ESC"
            if znak == b"\x03":
                raise KeyboardInterrupt
            return None

        import select
        import termios
        import tty

        fd = sys.stdin.fileno()
        stare_nastavitve = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            znak = sys.stdin.read(1)

            if znak == "\x1b":
                # Preverimo, ali v 0.05 s sledijo dodatni znaki za puščico
                r, _, _ = select.select([sys.stdin], [], [], 0.05)
                if r:
                    naslednja = sys.stdin.read(2)
                    if naslednja == "[D":
                        return "LEVO"
                    if naslednja == "[C":
                        return "DESNO"
                return "ESC"

            if znak in ("\r", "\n"):
                return "ENTER"
            if znak == "\x03":
                raise KeyboardInterrupt

            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, stare_nastavitve)

    izrisi()

    try:
        while True:
            tipka = beri_tipko()

            if tipka == "LEVO":
                izbran = (izbran - 1) % stevilo_kart
                izrisi()

            elif tipka == "DESNO":
                izbran = (izbran + 1) % stevilo_kart
                izrisi()

            elif tipka == "ENTER":
                return imena_kart[izbran]

            elif tipka == "ESC":
                return None

    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")
        return None




if __name__ == "__main__":
    #razdeli_karte(igralci=["player1", "player2", "player3", "player4"])
    izberi_igralca_za_igro(igralci=["player1", "player2", "player3", "player4"])