Súbory:

    philisopher/phil_foreman.py - obsahuje implementáciu problemu večerajúcich filozofov z prednášky a cvičenia s použitím čašníka (foreman)
    powerplant/task1.pu - obsahuje implementáciu príkladu atómovej elektrárne 1 z cvičenia
    powerplant/task2.py - obsahuje implementáciu príkladu atómovej elektrárne 2 z cvičenia
    powerplant/lightswitch.py - obsahuje upravený lightswitch - vracia počet vlákien v zámku
    powerplant/barrier.py - obsahuje implementáciu bariéry s použitím synchronizačného objektu Event()
                        - tiež bola doplnená o funkciu wait - ktorá neinkrementuje counter, ale len čaká
                        - to sa využíva pri čakaní vlákien monitora - neovplyvňujú counter

Atómová elektráreň 2

    Úloha 1: Urobte analýzu, o aké typy synchronizačných úloh (prípadne ich modifikácie či kombinácie) sa v tejto úlohe jedná.
        Riešenie: 
            - ide o úlohu vzájomného vylúčenia procesov, kde operátori (monitori) predstavujú jednu kategóriu a čislá (senzory) druhú
            - úloha je špecifická v tom, že naraz môžu čitať viacerí operátori, ale aj viacero čidiel môže zapisovať naraz, keďže 
            každé čislo má vlastné miesto v pamäti do ktorého píše hodnoty
            - zámok teda existuje len nad celou pamäťou a to kvôli tomu, aby sme zabezpečili vzájomné vylúčenie procesov
            - takže buď čitatelia čítajú, alebo zapisovatelia zapisujú

    Úloha 2: Presne namapujte vami zvolené synchronizačné úlohy (primitívy) na jednotlivé časti zadania.
        Riešenie:
            - keďže operátori môžu čítať až po dodaní údajov od každého sensoru aspoň raz, použijeme synchronizačný vzor bariéra
            - tento vzor upravíme tak, aby inkrementovali počítadlo len sensory. Operátori budú len čakať na udalosť, ktorá
            nastane až po tom,  čo dokončia zápis všetky 3 senzory
            - operátor počas prechodu cez turniket zamkne zámok vypínačom tak, aby nebolo možné pre sensor dostať sa do pamäte
            a po vykonaní svojho kódu zámok uvoľní
            - senzor pred vstupom do turniketu uzamkne zámok pamäte a to tak, že operátori nebudú môcť vstúpiť
            - tým sa dosiahne to, že senzory sa budú na turnikete obiehať pred monitormi, ak bude práve nejaký zo senzorov zapisovať
            (teda ak bude držať zámok)
    
    Úloha 3: Pseudokód
        def init():
            pocet_senzorov = 3
            pocet_operatorov = 8
            lightswitch_operator = LightSwitch()
            lightswitch_senzor = LightSwitch()
            turniket = Semaphore(1)
            zamok_pamate = Semaphore(1)
            bariera = Barrier(pocet_senzorov)

        def operator(operator_id):
                // cakame dokym vsetky senzory nedodaju udaje
                bariera.wait()
                while True:
                    // prechod cez turniket
                    turniket.wait()
                    // zabranenie senzorom zapisovat
                    monitor_cnt = lightswitch_operator.lock(zamok_pamate)
                    // vyjdenie z turniketu
                    turniket.signal()
                    # zapis
                    trvanie_citania = rand(40, 50) milisekund
                    print(operator_id, trvanie_citania, monitor_cnt)
                    sleep(trvanie_citania)
                
                    # uvolenie pamate - ak je operator posledny, tak moze senzor zapisovat
                    lightswitch_operator.unlock(zamok_pamate)

        def sensor(sensor_id):
            while True:
                # cakaj na zapis
                sleep(rand(50, 60) milisekund)
                # zamkni turniket vypinacom - senzory mozu prechadzat
                pocet_senzorov = lightswitch_senzor.lock(turniket)
                # zamkni pamat - operator nemoze citat
                zamok_pamate.wait()
                # zapisuj
                trvanie_zapisu = rand(minimalny_cas, maximalny_cas) milisekund
                print(sensor_id, trvanie_zapisu, pocet_senzorov)
                sleep(trvanie_zapisu)
                # odomkni pamat
                zamok_pamate.signal()
        
                # odomkni turniket - ak je to posledny senzor, mozu prechadzat operatori
                lightswitch_senzor.unlock(turniket)
                # ak bol zapis uspesny, inkrementuj pocitadlo a cakaj
                bariera.incrementuj_a_cakaj()
                    