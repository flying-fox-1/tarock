import random
from InquirerPy import inquirer, prompt
from InquirerPy.base.control import Choice
from karte import igralne_karte, narisi_karte_v_roki
from pprint import pprint

from obdelava_kart import vse_karte_pridobi



def izpiši_karte_igralca(karte_med_igralci, igralec):
    imena_kart = []

    for barva, karte in karte_med_igralci[igralec].items():
        for karta in karte:
            imena_kart.append(f"{barva}_{karta}")
    #print(imena_kart)
    narisi_karte_v_roki(imena_kart)
            

def igraj_karto(karte_med_igralci, igralec, karte_na_mizi, ze_igrane_karte, igralec_ki_ni_bot="") -> str | list[str] | list[str]| dict[str , dict]:        #karte_igralca dobimo iz slovarja z uporabo igralec  # kasneje dodaj stratgije # naključno izbere karto #zaenkrat še ne šteje točk, nobeden ne pobere, vsi samo mečejo karte na mizo!
    
    print(f"Na vrsti je: {igralec}.")
    
    if not karte_na_mizi:     #Nobena karta še ni bila igrana
        
       # if igralec == igralec_ki_ni_bot:
            
           # izbira = inquirer.select(message="izberi karto: ",choices=karte_med_igralci[igralec][inquirer.select(message="izberi barvo karte: ",choices=["kara","pik","srce","križ"]).execute()],).execute()
           # print(izbira)
            #pass
        izbira = random.choice(list(karte_med_igralci[igralec].keys()))
        
        while not karte_med_igralci[igralec][izbira]:                       #preveri ali igralec nima nakjlučno izbrane karte in izbere drugo
            izbira = random.choice(list(karte_med_igralci[igralec].keys()))
        
        krajše_ime_ig_karte = random.choice(karte_med_igralci[igralec][izbira])
        
        igrana_karta = str(izbira) + "_" + str(krajše_ime_ig_karte)
        ze_igrane_karte.append(igrana_karta)
        karte_na_mizi.append(igrana_karta)      
        karte_med_igralci[igralec][izbira].remove(krajše_ime_ig_karte)
        


        
        return igrana_karta, karte_na_mizi, ze_igrane_karte, karte_med_igralci
    
    elif karte_na_mizi:     #nek igralec je že igral pred tem igrlacem
        
        barva_igrane_karte = karte_na_mizi[0].split("_")[0]
        
        if karte_med_igralci[igralec].get(barva_igrane_karte):        
            print(f"{igralec} {barva_igrane_karte}")       # IGRALEC IMA BARVO, KI JE NA MIZI
       
            izbira = barva_igrane_karte
            
            krajše_ime_ig_karte = random.choice(karte_med_igralci[igralec][izbira])
            
            igrana_karta = str(izbira) + "_" + str(krajše_ime_ig_karte)
            ze_igrane_karte.append(igrana_karta)
            karte_na_mizi.append(igrana_karta)      
            karte_med_igralci[igralec][izbira].remove(krajše_ime_ig_karte)
            

            
            return igrana_karta, karte_na_mizi, ze_igrane_karte, karte_med_igralci     
        
        
        elif karte_med_igralci[igralec].get("tarok"):     
            print(f"{igralec} nima {barva_igrane_karte}, ima tarok")
            
            izbira = "tarok"
            
            krajše_ime_ig_karte = random.choice(karte_med_igralci[igralec][izbira])
            
            igrana_karta = str(izbira) + "_" + str(krajše_ime_ig_karte)
            ze_igrane_karte.append(igrana_karta)
            karte_na_mizi.append(igrana_karta)      
            karte_med_igralci[igralec][izbira].remove(krajše_ime_ig_karte)
            

            
            return igrana_karta, karte_na_mizi, ze_igrane_karte, karte_med_igralci
            
        else:
            print(f"{igralec} nima ne {barva_igrane_karte} ne taroka")
            
            izbira = random.choice(list(karte_med_igralci[igralec].keys()))
            
            while izbira == "tarok" or not karte_med_igralci[igralec][izbira]:
                izbira = random.choice(list(karte_med_igralci[igralec].keys()))
            
            krajše_ime_ig_karte = random.choice(karte_med_igralci[igralec][izbira])
            
            igrana_karta = str(izbira) + "_" + str(krajše_ime_ig_karte)
            ze_igrane_karte.append(igrana_karta)
            karte_na_mizi.append(igrana_karta)      
            karte_med_igralci[igralec][izbira].remove(krajše_ime_ig_karte)

            
            
            return igrana_karta, karte_na_mizi, ze_igrane_karte, karte_med_igralci
   
            
def razdeli_točke(igralci, karte_na_mizi_igralcev: dict[str, str], štih) -> dict[str,list[str]] | str: #karte_na_mizi_igralcev):
    

    vse_karte = vse_karte_pridobi()
    Največja_karta = karte_na_mizi_igralcev[igralci[0]]  # "tarok_8"
    igralec_z_naj_tarokom = igralci[0]
    
    #print("Največja Karta je ", Največja_karta)
    
    for igralec in igralci:
        
        
        
        karta_igralca = karte_na_mizi_igralcev[igralec]
        
        barva_vrednost_karta_igralca = karte_na_mizi_igralcev[igralec].split(sep="_") # ["tarok","8"]
        
        barva_vrednost_igrane_karte = Največja_karta.split(sep="_") #['tarok', '2']
        
        if barva_vrednost_igrane_karte[0] == barva_vrednost_karta_igralca[0]:
            
            
            if vse_karte[barva_vrednost_karta_igralca[0]][barva_vrednost_karta_igralca[1]] > vse_karte[barva_vrednost_igrane_karte[0]][barva_vrednost_igrane_karte[1]]:
                print(f"Najvišja karta je {barva_vrednost_karta_igralca[0]} {barva_vrednost_igrane_karte[1]} od {igralec} \n")
                
                Največja_karta = karta_igralca
                igralec_z_naj_tarokom = igralec
                print(igralec_z_naj_tarokom)
                
        elif barva_vrednost_karta_igralca[0] == "tarok" and Največja_karta.split(sep="_")[0] != "tarok":
            print(f"Najvišja karta je {barva_vrednost_karta_igralca} od {igralec}")
            Največja_karta = karta_igralca
            igralec_z_naj_tarokom = igralec
        elif barva_vrednost_karta_igralca[0] == "tarok" and barva_vrednost_igrane_karte[0] == "tarok":
            
            if vse_karte["tarok"][barva_vrednost_karta_igralca[1]] > vse_karte["tarok"][barva_vrednost_igrane_karte[1]]:
                print(f"Najvišja karta je {barva_vrednost_karta_igralca[0], barva_vrednost_igrane_karte[1]} od {igralec}")
                Največja_karta = karta_igralca
                igralec_z_naj_tarokom = igralec
                print(igralec_z_naj_tarokom)
            
    if štih[igralec_z_naj_tarokom] == None:
        štih[igralec_z_naj_tarokom] = []
        
        
    for  igralec in igralci:
        štih[igralec_z_naj_tarokom].append(karte_na_mizi_igralcev[igralec])
        
    
    return štih, igralec_z_naj_tarokom
            
def točke(karte_i1: list) -> int:
    if not karte_i1:
        return 0

    vrednosti = {
        "tarok_21": 5,
        "tarok_1": 5,
        "tarok_sk": 5,
        "k": 5,
        "d": 4,
        "s": 3,
        "p": 2,
    }

    karte_vrednosti = []
    for karta in karte_i1:
        # If passed as a tuple from talon e.g. ("kara", "k", 5)
        if isinstance(karta, tuple):
            karta_str = f"{karta[0]}_{karta[1]}"
        else:
            karta_str = str(karta)

        # 1. Direct match (honours / special taroks)
        if karta_str in vrednosti:
            karte_vrednosti.append(vrednosti[karta_str])
        # 2. Suit card match e.g. "pik_k" -> "k"
        elif "_" in karta_str:
            del_st = karta_str.split("_")
            val = del_st[1] if len(del_st) > 1 else del_st[0]
            karte_vrednosti.append(vrednosti.get(val, 1))
        # 3. Fallback standard card (1 point)
        else:
            karte_vrednosti.append(1)

    vsota = 0
    št_kart = len(karte_vrednosti)

    # Groups of 3 (Sum of 3 cards - 2)
    for i in range(0, št_kart - (št_kart % 3), 3):
        skupina = karte_vrednosti[i : i + 3]
        vsota += sum(skupina) - 2

    # Remainder 1 or 2 cards (Sum - 1)
    ostanek = št_kart % 3
    if ostanek > 0:
        vsota += sum(karte_vrednosti[-ostanek:]) - 1

    return vsota

            
if __name__ == "__main__":
    igralci = [f"Igralec {i}" for i in range(1, 4 + 1)]
    karte_na_mizi_igralcev = {'Igralec 1': 'tarok_2', 'Igralec 2': 'tarok_sk', 'Igralec 3': 'tarok_5', 'Igralec 4': 'tarok_8'}
    karte_na_mizi_igralcev = {'Igralec 1': 'kara_2', 'Igralec 2': 'kara_k', 'Igralec 3': 'pik_10', 'Igralec 4': 'tarok_2'}

    razdeli_točke(igralci,karte_na_mizi_igralcev, rezultat_igralcev="")
