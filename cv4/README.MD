Súbory:
philisopher/phil_foreman.py - obsahuje implementáciu problemu večerajúcich filozofov z prednášky a cvičenia s použitím čašníka (foreman)
powerplant/task2.py - obsahuje implementáciu príkladu atómovej elektrárne 2 z cvičenia

Atómová elektráreň 2
    Úloha 1: Urobte analýzu, o aké typy synchronizačných úloh (prípadne ich modifikácie či kombinácie) sa v tejto úlohe jedná.
        Riešenie: 
            a) pri čakaní vlákien operátora na aspoň jeden zápis každého čidla môžme použiť vzor jednoduchej bariéry.
            Ak všetky vlákna čidiel aspoň raz zapíšu, bariéra sa otvorí a operátori môžu pristúpiť k dátam.
            b) 

vzajomne vylucenie - uloha
bariera - vzor ... mechanizmy
kategorie, kto ma prioritu (ak niekto ma)
pseudokod
pozor aby neprislo k vyhladoveniu cislo