from InquirerPy import inquirer, prompt
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import EmptyInputValidator, NumberValidator
#from main_simulation import točke_main
from obdelava_kart import izberi_igralca_za_igro, razdeli_karte
from pprint import pprint
from obdelava_igralcev import izpiši_karte_igralca, igraj_karto, razdeli_točke, točke
from karte import izpiši_talon, narisi_karte_v_roki
from obdelava_kart import izberi_karto_v_roki

import random

global rezultat_ekipe_1
        
def main():
    global ekipe, prosti_igralci, ekipa_1
    
    
    izbira = inquirer.select(message="",choices=[
        Choice(value=True, name="Zaženi igro"), 
        Choice(value=None, name="Izhod")],).execute()
    
    if izbira:      # ZAŽENI IGRO
        st_igralcev = int(inquirer.number(message="Vnesi število igralcev: ",min_allowed=3,max_allowed=4, validate=EmptyInputValidator(),).execute())
        
        print(st_igralcev)
        igralci = [f"Igralec {i}" for i in range(1, st_igralcev + 1)] #G

            
        izbira = inquirer.select(message="Kot kateri igralec Igrate?",choices=(*igralci,"Simuliraj Igro"),).execute()
        
        if izbira == "Simuliraj Igro":      #SIMULIRAJ IGRO - 0 IGRALCEV
            
            igra_sam = False
            
            rezultat_igralcev = dict.fromkeys(igralci)
            print(f"rezultat = {rezultat_igralcev}")
        
            talon, igralec_ki_igra, karte_med_igralci  = izberi_igralca_za_igro(igralci)
            print(f"Trenutno igra {igralec_ki_igra}.")
            print("\nV talonu so karte: ")
            izpiši_talon(talon)
            karte_na_mizi = []
            ze_igrane_karte = []


            if len(igralci) == 3:
                št_rund = 16
            else:
                št_rund = 12
                
                
            možnosti = ["kara","srce","pik","križ"]
            
            pprint(karte_med_igralci)
            
            for možnost in možnosti:
                if možnost in karte_med_igralci[igralec_ki_igra] and "k" in karte_med_igralci[igralec_ki_igra][možnost]:
                    možnosti.remove(možnost)

            izbrana_barva_kralja = random.choice(možnosti)
            print(izbrana_barva_kralja)
        
            prosti_igralci = igralci.copy()

            for i,x,y in talon:                 
                    if i == izbrana_barva_kralja and x == "k":
                        #Igralec igra sam
                        print(f"{igralec_ki_igra} se je zarufal, igra sam.")
                        ekipe = (igralec_ki_igra)
                        prosti_igralci.remove(igralec_ki_igra)
                        igra_sam = True
                    else:                          
                        igra_sam = False


            partner = None
            for igralec in igralci:
                if izbrana_barva_kralja in karte_med_igralci[igralec]:
                    if "k" in karte_med_igralci[igralec][izbrana_barva_kralja]:
                        partner = igralec
                        break

            # Če ima kralja v talonu ali v svoji roki, igra sam
            if partner is None or partner == igralec_ki_igra or igra_sam:
                ekipa_1 = [igralec_ki_igra]
                ekipa_2 = [igralec for igralec in igralci if igralec != igralec_ki_igra]
            else:
                ekipa_1 = [igralec_ki_igra, partner]
                ekipa_2 = [igralec for igralec in igralci if igralec not in ekipa_1]

            print("Ekipa 1 :", ekipa_1)
            print("Ekipa 2 :", ekipa_2)
            
    
            karte_na_mizi_igralcev = {}
            for igralec in igralci:
                karte_na_mizi_igralcev[igralec] =  None
                
            štih = dict.fromkeys(igralci)
            
            #pprint(karte_med_igralci)
            for i in range(št_rund):  #dejanska simulacija igre po rundah
                
                
                for igralec in igralci:
                    
                    print(f"Karte {igralec}")
                    izpiši_karte_igralca(karte_med_igralci, igralec)
                    
                    igrana_karta, karte_na_mizi, ze_igrane_karte, karte_med_igralci = igraj_karto(karte_med_igralci, igralec, karte_na_mizi, ze_igrane_karte)
                    karte_na_mizi_igralcev[igralec] = igrana_karta
                    
                    print()
                
                štih, igralec_ki_pobere = razdeli_točke(igralci, karte_na_mizi_igralcev, štih)
                
                print(f"Te karte pobere {igralec_ki_pobere}")
                index = igralci.index(igralec_ki_pobere)
                
                igralci = igralci[index:] + igralci[:index]
                
                karte_na_mizi = []
                                
                imena_kart_za_izpis = []

                for karta in karte_na_mizi_igralcev.values():
                    imena_kart_za_izpis.append(karta)
                narisi_karte_v_roki(imena_kart_za_izpis, 10)          

            if igralec_ki_igra in štih:
                if štih[igralec_ki_igra] is None:
                    štih[igralec_ki_igra] = []
                štih[igralec_ki_igra].extend(talon)


            for igralec in igralci:
                pobrane = štih.get(igralec) or []
                rezultat_igralcev[igralec] = točke(pobrane)

            
            rezultat_ekipe_1 = sum(rezultat_igralcev[i] for i in ekipa_1)
            rezultat_ekipe_2 = sum(rezultat_igralcev[i] for i in ekipa_2)

            imena_ekipa_1 = ", ".join(ekipa_1)
            imena_ekipa_2 = ", ".join(ekipa_2)

            print("\n" + "=" * 40)
            print("           REZULTAT IGRALCEV            ")
            print("=" * 40)
            for igralec in sorted(rezultat_igralcev.keys()):
                print(f" {igralec} : {rezultat_igralcev[igralec]} točk")

            print("-" * 40)
            print(f" Ekipa 1 ({imena_ekipa_1}): {rezultat_ekipe_1} točk")
            print(f" Ekipa 2 ({imena_ekipa_2}): {rezultat_ekipe_2} točk")
            print("=" * 40 + "\n")
                
        else:
#-------------------------------------------------------------------- IGRAJ Z BOTI
            igrani_igralec = izbira
            
            boti = igralci.copy()
            boti.remove(izbira)
            
            igralci = [f"Igralec {i}" for i in range(1, st_igralcev + 1)] #G
            
            talon, karte_med_igralci = razdeli_karte(igralci)
            print("Vaše Karte:")
            izpiši_karte_igralca(karte_med_igralci, igrani_igralec)
            
            
            izbira = inquirer.select(message="Ali Igrate?",choices=("Da", "Ne"),).execute()
            
            if izbira == "Da":          
                igralec_ki_igra = igrani_igralec        #IGRAJ V NEKI BARVI
                
                print(f"{igralec_ki_igra} je šel igrati.")
                
                izbrana_barva_kralja = inquirer.text(message="V kateri barvi igrate?",completer={"srce": None,"kara": None,"pik": None,"križ" :None},multicolumn_complete=True,).execute()
                
                
                
                for i,x,y in talon:                 #PREVERI ALI SE JE IGRALEC "ZARUFAL"
                    if i == izbira and x == "k":
                        # dodaj za igranje sam - zarufal
                        print("Igrate sami")
                
                print("\nV talonu so karte: ")
                izpiši_talon(talon)
            
                igra_sam = False
                
                rezultat_igralcev = dict.fromkeys(igralci)
    
                karte_na_mizi = []
                ze_igrane_karte = []


                if len(igralci) == 3:
                    št_rund = 16
                else:
                    št_rund = 12
                    
                    
                možnosti = ["kara","srce","pik","križ"]
                
                
                for možnost in možnosti:
                    if možnost in karte_med_igralci[igralec_ki_igra] and "k" in karte_med_igralci[igralec_ki_igra][možnost]:
                        možnosti.remove(možnost)

                print(f"\n{igralec_ki_igra} igra v {izbrana_barva_kralja} \n")
            
                prosti_igralci = boti.copy()

                for i,x,y in talon:                 
                        if (i == izbrana_barva_kralja and x == "k") or ( izbrana_barva_kralja in karte_med_igralci[igralec_ki_igra] and "k" in karte_med_igralci[igrani_igralec][izbrana_barva_kralja]):
                            #Igralec igra sam
                            print(f"{igralec_ki_igra} se je zarufal, igra sam.")
                            if igralec_ki_igra in prosti_igralci:
                                prosti_igralci.remove(igralec_ki_igra)
                            igra_sam = True
                            break

                # Poiščemo partnerja (kdo ima klicanega kralja)
                partner = None
                for igralec in igralci:
                    if izbrana_barva_kralja in karte_med_igralci[igralec]:
                        if "k" in karte_med_igralci[igralec][izbrana_barva_kralja]:
                            partner = igralec
                            break

                # Če ima kralja v talonu ali ga ima on igra sam
                if partner is None or partner == igralec_ki_igra or igra_sam:
                    ekipa_1 = [igralec_ki_igra]
                    ekipa_2 = [igralec for igralec in igralci if igralec != igralec_ki_igra]
                else:
                    ekipa_1 = [igralec_ki_igra, partner]
                    ekipa_2 = [igralec for igralec in igralci if igralec not in ekipa_1]

                print("Ekipa 1 :", ekipa_1)
                print("Ekipa 2 :", ekipa_2)

                
        
                karte_na_mizi_igralcev = {}
                for igralec in igralci:
                    karte_na_mizi_igralcev[igralec] =  None
                    
                štih = dict.fromkeys(igralci)
            
                
                for i in range(št_rund):  #dejanska simulacija igre po rundah
                
                
                    for igralec in igralci:
                        if igralec == igrani_igralec:
                            if karte_na_mizi:
        
                                print("karte na mizi: ")
                                prva_karta = karte_na_mizi[0]

                                potrebna_barva, k3arta = prva_karta.split("_")
                                narisi_karte_v_roki(karte_na_mizi)
                                
                                igrana_karta = izberi_karto_v_roki(karte_med_igralci[igrani_igralec], potrebna_barva)
                            else:
                                print("Na mizi še ni kart")
                                igrana_karta = izberi_karto_v_roki(karte_med_igralci[igrani_igralec], None)
                            
                            if igrana_karta == None:
                                raise Exception("Konec Igre")
                            
                            karte_na_mizi.append(igrana_karta)
                            karte_na_mizi_igralcev[igralec] = igrana_karta
                            barva, karta = igrana_karta.split(sep="_")
                            karte_med_igralci[igralec][barva].remove(karta)
                        else:
                            igrana_karta, karte_na_mizi, ze_igrane_karte, karte_med_igralci = igraj_karto(karte_med_igralci, igralec, karte_na_mizi, ze_igrane_karte)
                            karte_na_mizi_igralcev[igralec] = igrana_karta
                        
                        print()
                    
                    štih, igralec_ki_pobere = razdeli_točke(igralci, karte_na_mizi_igralcev, štih)
                    
                    print(f"Te karte pobere {igralec_ki_pobere}")
                    indeks = igralci.index(igralec_ki_pobere)
                    
                    igralci = igralci[indeks:] + igralci[:indeks]
                    
                    karte_na_mizi = []
                                    
                    imena_kart_za_izpis = []

                    for karta in karte_na_mizi_igralcev.values():
                        imena_kart_za_izpis.append(karta)
                    narisi_karte_v_roki(imena_kart_za_izpis, 10)

                # Izračun vsote točk
                if štih.get(igralec_ki_igra) is None:
                    štih[igralec_ki_igra] = []

                štih[igralec_ki_igra].extend(talon)

                for igralec in igralci:   
                    if rezultat_igralcev[igralec] == None:
                        rezultat_igralcev[igralec] = 0
                        if štih[igralec] == [] or štih[igralec] == None:
                            continue               
                        
                    rezultat_igralcev[igralec] = točke(štih[igralec]) 


                
                
                rezultat_ekipe_1 = sum(rezultat_igralcev[igralec] for igralec in ekipa_1)
                rezultat_ekipe_2 = sum(rezultat_igralcev[igralec] for igralec in ekipa_2)


                imena_ekipa_1 = ", ".join(ekipa_1)
                imena_ekipa_2 = ", ".join(ekipa_2)

                print("\n" + "=" * 40)
                print("           REZULTAT IGRALCEV            ")
                print("=" * 40)
                for igralec in sorted(rezultat_igralcev.keys()):
                    print(f" {igralec} : {rezultat_igralcev[igralec]} točk")


                print(f" Ekipa 1 ({imena_ekipa_1}): {rezultat_ekipe_1} točk")
                print(f" Ekipa 2 ({imena_ekipa_2}): {rezultat_ekipe_2} točk")
                print("=" * 40 + "\n")
            else:
#----------------------------------------------------------IGRALEC NE IGRA; IGRA BOT
                rezultat_igralcev = dict.fromkeys(igralci)
                print(rezultat_igralcev)
            
                talon, igralec_ki_igra, karte_med_igralci  = izberi_igralca_za_igro(igralci,True,None, talon)  #boti zato, ker igralec ne igra
                talon, igralec_ki_igra, karte_med_igralci  = izberi_igralca_za_igro(boti,False,karte_med_igralci, talon)
                pprint(f"Trenutno igra {igralec_ki_igra}.")
                #for igralec in boti:     # popravil iz igralci-> boti
                    #print(f"Karte {igralec}")
                    #izpiši_karte_igralca(karte_med_igralci, igralec) #popravil iz boti->igralec
                
                #igrani_igralec = izbira
                
                #igralec_ki_igra = igrani_igralec        #IGRAJ V NEKI BARVI
                
                print(f"Igrati je šel {igralec_ki_igra}.")
                
                izbrana_barva_kralja = random.choice(["pik","kara","križ","srce"])
                
                igra_sam = False
                
                print("\nV talonu so karte: ")
                izpiši_talon(talon)
                
                rezultat_igralcev = dict.fromkeys(igralci)
                print(f"rezultat = {rezultat_igralcev}")
    
                karte_na_mizi = []
                ze_igrane_karte = []


                if len(igralci) == 3:
                    št_rund = 16
                else:
                    št_rund = 12
                    
                    
                možnosti = ["kara","srce","pik","križ"]
                
                
                for možnost in možnosti:
                    if možnost in karte_med_igralci[igralec_ki_igra] and "k" in karte_med_igralci[igralec_ki_igra][možnost]:
                        možnosti.remove(možnost)

                print(f"\n{igralec_ki_igra} igra v ", izbrana_barva_kralja, "\n")

                prosti_igralci = [item for item in igralci if item != igralec_ki_igra] #G
                
                for i,x,y in talon:                 
                        if (i == izbrana_barva_kralja and x == "k") or ( izbrana_barva_kralja in karte_med_igralci[igralec_ki_igra] and "k" in karte_med_igralci[igralec_ki_igra][izbrana_barva_kralja]):
                            #Igralec igra sam
                            print(f"{igralec_ki_igra} se je zarufal, igra sam.")
                            if igralec_ki_igra in prosti_igralci:
                                prosti_igralci.remove(igralec_ki_igra)
                            igra_sam = True
                            break
                            
                # kdo ima klicanega kralja
                partner = None
                for igralec in igralci:
                    if izbrana_barva_kralja in karte_med_igralci[igralec]:
                        if "k" in karte_med_igralci[igralec][izbrana_barva_kralja]:
                            partner = igralec
                            break

                # Če ima kralja v talonu ali v svoji roki, igra sam
                if partner is None or partner == igralec_ki_igra or igra_sam:
                    ekipa_1 = [igralec_ki_igra]
                    ekipa_2 = [igralec for igralec in igralci if igralec != igralec_ki_igra]
                else:
                    ekipa_1 = [igralec_ki_igra, partner]
                    ekipa_2 = [igralec for igralec in igralci if igralec not in ekipa_1]

                print("Ekipa 1 :", ekipa_1)
                print("Ekipa 2 :", ekipa_2)

                
        
                karte_na_mizi_igralcev = {}
                for igralec in igralci:
                    karte_na_mizi_igralcev[igralec] =  None
                    
                štih = dict.fromkeys(igralci)
            
                
                for i in range(št_rund):  #dejanska simulacija igre po rundah
                
                
                    for igralec in igralci:
                        
                        if igralec == igrani_igralec:   #Preveri ali je navrsti dejanski igralec in ne bot
                            if karte_na_mizi:
                                print()
        
                                print("karte na mizi ", karte_na_mizi)
                                prva_karta = karte_na_mizi[0]

                                potrebna_barva, k3arta = prva_karta.split("_")
                                narisi_karte_v_roki(karte_na_mizi)
                                
                                igrana_karta = izberi_karto_v_roki(karte_med_igralci[igrani_igralec], potrebna_barva)
                                
                            else:
                                print("Na mizi še ni kart")
                                igrana_karta = izberi_karto_v_roki(karte_med_igralci[igrani_igralec], None)
                            
                            if igrana_karta == None:
                                raise Exception("Konec Igre")
                            karte_na_mizi.append(igrana_karta)
                            karte_na_mizi_igralcev[igralec] = igrana_karta
                            barva, karta = igrana_karta.split(sep="_")
                            print(barva, karta)
                            karte_med_igralci[igralec][barva].remove(karta)
                            pprint(karte_med_igralci[igralec])
                        else:
                            igrana_karta, karte_na_mizi, ze_igrane_karte, karte_med_igralci = igraj_karto(karte_med_igralci, igralec, karte_na_mizi, ze_igrane_karte)
                            karte_na_mizi_igralcev[igralec] = igrana_karta
                        
                        print()
                    
                    if štih.get(igralec_ki_igra) is None:
                        štih[igralec_ki_igra] = []
                    
                    štih, igralec_ki_pobere = razdeli_točke(igralci, karte_na_mizi_igralcev, štih)
                    
                    print(f"Te karte pobere {igralec_ki_pobere}")
                    index = igralci.index(igralec_ki_pobere)
                    
                    igralci = igralci[index:] + igralci[:index]
                    
                    karte_na_mizi = []
                                    
                    imena_kart_za_izpis = []

                    for karta in karte_na_mizi_igralcev.values():
                        imena_kart_za_izpis.append(karta)
                    narisi_karte_v_roki(imena_kart_za_izpis, 10)

                štih[igralec_ki_igra].extend(talon)

                for igralec in igralci:   
                    if rezultat_igralcev[igralec] == None:
                        rezultat_igralcev[igralec] = 0
                        if štih[igralec] == [] or štih[igralec] == None:
                            continue               
                        
                    rezultat_igralcev[igralec] = točke(štih[igralec]) 
                 

                      
                
                print()
                print("="*40)
                print(" "*11,"REZULTAT IGRALCEV"," "*11)
                print("="*40)
                # Izračun vsote točk
                rezultat_ekipe_1 = sum(rezultat_igralcev[igralec] for igralec in ekipa_1)
                rezultat_ekipe_2 = sum(rezultat_igralcev[igralec] for igralec in ekipa_2)

                imena_ekipa_1 = ", ".join(ekipa_1)
                imena_ekipa_2 = ", ".join(ekipa_2)

                for igralec in igralci:
                    print(f" {igralec} : {rezultat_igralcev[igralec]}")
                    
                print("-"*40)
                
                print(f"Ekipa 1 ({imena_ekipa_1}): {rezultat_ekipe_1}")
                print(f"Ekipa 2 ({imena_ekipa_2}): {rezultat_ekipe_2}")
                
                print("="*40)
                print()
                


if __name__ == "__main__":
    main()


