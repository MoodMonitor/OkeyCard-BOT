import random
import math
from functools import partial
import time
import os

import openpyxl


def CzyIstnieje(nazwa1):
    global nazwa, wb
    nazwa = nazwa1
    if os.path.exists(nazwa1)==True:
        wb = openpyxl.load_workbook(nazwa1)
    else:
        wb = openpyxl.Workbook()

def Excel(nazwaa,ilosc, wynik, czas, lista):
    CzyIstnieje("wyniki.xlsx")
    n = 1
    sheet = wb.active
    while sheet.cell(row = n, column = 1).value != None:
        n = n+1

    sheet.cell(row=n, column=1).value = nazwaa
    sheet.cell(row=n, column=2).value = ilosc
    sheet.cell(row=n, column=3).value = wynik
    sheet.cell(row=n, column=4).value = czas
    sheet.cell(row=n, column=5).value = lista
    wb.save(nazwa)


def DodajKarte(karty, aktualne, kart):
    if kart != 19:
        kart+=1
        if len(aktualne) != 5:
            a = random.choice(karty)
            aktualne.append(a)
            karty.remove(a)
            return karty, aktualne, kart

def Zaczynamy():
    karty = []
    pomoc = []
    aktualne = []
    kart = -5
    punkty = 0
    for i in range(1,9):
        karty.append(str(i) + "C")
        pomoc.append(str(i) + "C")
    for i in range(1,9):
        karty.append(str(i) + "N")
        pomoc.append(str(i) + "N")
    for i in range(1,9):
        karty.append(str(i) + "Z")
        pomoc.append(str(i) + "Z")
    for i in range(5):
        karty, aktualne, kart = DodajKarte(karty, aktualne, kart)
    return karty, pomoc, aktualne, punkty

def prawiebingo(aktualne):
    c = []
    n = []
    z = []
    gitc = []
    gitn = []
    gitz = []
    for i in aktualne:
        if i[1] == "C":
            c.append(int(i[0]))
        elif i[1] == "N":
            n.append(int(i[0]))
        elif i[1] == "Z":
            z.append(int(i[0]))
    if len(c) >= 2:
        a = sorted(c)
        for i in range(1, len(a)):
            if a[i] - a[i-1] == 1 or a[i] - a[i-1] == 2:
                if str(a[i]) + "C" not in gitc:
                    gitc.append(str(a[i]) + "C")
                if str(a[i-1]) + "C" not in gitc:
                    gitc.append(str(a[i-1]) + "C")
    if len(n) >= 2:
        a = sorted(n)
        for i in range(1, len(a)):
            if a[i] - a[i-1] == 1 or a[i] - a[i-1] == 2:
                if str(a[i]) + "N" not in gitn:
                    gitn.append(str(a[i]) + "N")
                if str(a[i-1]) + "N" not in gitn:
                    gitn.append(str(a[i-1]) + "N")
    if len(z) >= 2:
        a = sorted(z)
        for i in range(1, len(a)):
            if a[i] - a[i-1] == 1 or a[i] - a[i-1] == 2:
                if str(a[i]) + "Z" not in gitz:
                    gitz.append(str(a[i]) + "Z")
                if str(a[i - 1]) + "Z" not in gitz:
                    gitz.append(str(a[i - 1]) + "Z")
    return gitc, gitn, gitz


def bingo(odw, lista):
    c = []
    n = []
    z = []
    bingo = []
    for i in lista:
        if i[1] == "C":
            c.append(int(i[0]))
        elif i[1] == "N":
            n.append(int(i[0]))
        elif i[1] == "Z":
            z.append(int(i[0]))
    if len(c) >= 3:
        licz = 0
        a = sorted(c, reverse= odw)
        for i in range(1, len(a)):
            if math.fabs(a[i] - a[i - 1]) == 1:
                licz += 1

                if a[i] not in bingo:
                    bingo.append(a[i])
                if a[i - 1] not in bingo:
                    bingo.append(a[i - 1])

                if licz == 2:
                    return [str(s) + "C" for s in bingo]
            else:
                licz = 0
                bingo = []

    elif len(n) >= 3:
        licz = 0
        a = sorted(n, reverse= odw)
        for i in range(1,len(a)):
            if math.fabs(a[i] - a[i - 1]) == 1:
                licz+= 1

                if a[i] not in bingo:
                    bingo.append(a[i])
                if a[i-1] not in bingo:
                    bingo.append(a[i-1])

                if licz == 2:
                    return [str(s) + "N" for s in bingo]
            else:
                licz = 0
                bingo = []
    elif len(z) >= 3:
        licz = 0
        a = sorted(z, reverse= odw)
        for i in range(1, len(a)):
            if math.fabs(a[i] - a[i - 1]) == 1:
                licz += 1

                if a[i] not in bingo:
                    bingo.append(a[i])
                if a[i - 1] not in bingo:
                    bingo.append(a[i - 1])

                if licz == 2:
                    return [str(s) + "Z" for s in bingo]
            else:
                licz = 0
                bingo = []
    return 0

def mozliwebinga(lista, odw):
    c = []
    n = []
    z = []
    binga = []
    for i in lista:
        if i[1] == "C":
            c.append(i)
        elif i[1] == "N":
            n.append(i)
        elif i[1] == "Z":
            z.append(i)

    licz = 0
    a = sorted(c, reverse= odw)
    tym = []
    flaga = 0
    for i in range(0, len(a)-1):
        if flaga == 1:
            flaga = 0
            continue
        if math.fabs(int(a[i+1][0]) - int(a[i][0])) == 1:
            licz+=1
            if a[i] not in tym:
                tym.append(a[i])

            if licz == 2:
                tym.append(a[i+1])
                binga.append(tym)
                tym = []
                licz = 0
                flaga = 1
        else:
            licz = 0
            tym = []

    licz = 0
    a = sorted(n, reverse= odw)
    tym = []
    flaga = 0
    for i in range(0, len(a)-1):
        if flaga == 1:
            flaga = 0
            continue
        if math.fabs(int(a[i+1][0]) - int(a[i][0])) == 1:
            licz+=1
            if a[i] not in tym:
                tym.append(a[i])

            if licz == 2:
                tym.append(a[i+1])
                binga.append(tym)
                tym = []
                licz = 0
                flaga = 1
        else:
            licz = 0

    licz = 0
    a = sorted(z, reverse= odw)
    tym = []
    flaga = 0
    for i in range(0, len(a)-1):
        if flaga == 1:
            flaga = 0
            continue
        if math.fabs(int(a[i+1][0]) - int(a[i][0])) == 1:
            licz+=1
            if a[i] not in tym:
                tym.append(a[i])

            if licz == 2:
                tym.append(a[i+1])
                binga.append(tym)
                tym = []
                licz = 0
                flaga = 1
        else:
            licz = 0

    return binga


def Usun(karta, karty, pomoc, aktualne, kart):
    aktualne.remove(karta)
    pomoc.remove(karta)
    try:
        karty, aktualne, kart = DodajKarte(karty, aktualne, kart)
    except:
        pass
    return karty, pomoc, aktualne, kart

def BingoPsuje(odw, pomoc, aktualne, punkty): #Czy bingo psuuje
    lista = []
    for i in list(pomoc):
        lista.append(i)
    d1 = len(mozliwebinga(lista, False))
    a = bingo(odw, aktualne)
    if a!= 0:
        for i in a:
            lista.remove(i)
    d2 = len(mozliwebinga(lista, False))
    if math.fabs(d1 - d2) >= 2 and punkty + d2*100 + 100 < 400:
        return 1
    else:
        return 0

def BingoPsuje2(odw, pomoc, aktualne): #Czy bingo psuuje
    lista = []
    for i in list(pomoc):
        lista.append(i)
    d1 = len(mozliwebinga(lista, False))
    a = bingo(odw, aktualne)
    if a!= 0:
        for i in a:
            lista.remove(i)
    d2 = len(mozliwebinga(lista, False))
    if math.fabs(d1 - d2) >= 2:
        return 1
    else:
        return 0


def rozwbingo(pomoc, el):
    lista = []
    for i in pomoc:
        lista.append(i)
    dl = len(mozliwebinga(lista, False))
    try:
        lista.remove(str(el))
    except:
        print("hij")
        return

    if len(mozliwebinga(lista, False)) < dl:
        return 1 #Rozwala bingo
    else:
        return 0 #Nie rozwala binga



def algorytm2R(pomoc, aktualne): #glebokosc 2 ~43%
    punkty = {}
    for i in aktualne:
        punkty[str(i)] = 0


    for i in aktualne:
        ######PRZYGOTOWANIE
        lista1 = list(aktualne)
        lista1.remove(i)

        lista2 = list(pomoc)
        lista2.remove(i)
        #############

        for j in lista2:
            lista1.append(j)
            if bingo(False, lista1) != 0:
                punkty[i]+= 100

            for q in lista1:

                lista3 = list(lista1)
                lista3.remove(q)

                lista4 = list(lista2)
                lista4.remove(q)

                for r in list(lista4):
                    lista3.append(r)
                    if bingo(False, lista3) != 0:
                        punkty[i] += 100

                    lista3.remove(r)



            lista1.remove(j)

    min = punkty[list(punkty)[0]]
    zap = []
    for i in list(punkty):
        if punkty[i] == min:
            zap.append(i)
        if punkty[i] > min:
            min = punkty[i]
            zap = []
            zap.append(i)

    if len(zap)!= 1:
        for i in zap:
            if rozwbingo(pomoc, i) != 1:
                return i, sorted(punkty, key=punkty.get,reverse=True)
    else:
        return zap[0], sorted(punkty, key=punkty.get,reverse=True)

    cz,n,z = prawiebingo(aktualne)
    for i in zap:
        if i in cz or i in n or i in z:
            zap.remove(i)
    return random.choice(zap), sorted(punkty, key=punkty.get,reverse=True)
    #print(zap, punkty)
    #return sorted(punkty, key=punkty.get,reverse=True)

def Wyniki():
    import ast
    CzyIstnieje("wyniki.xlsx")
    sheet = wb.active
    wyn = {}
    n = 33
    while sheet.cell(row=n, column=1).value != None:
        n = n + 1
    for i in range(33,n):
        lista = sheet.cell(row=i, column=5).value
        lista2 = ast.literal_eval(lista)
        for i in lista2:
            try:
                wyn[i[0]]+=1
            except:
                wyn[i[0]] = 0
                wyn[i[0]]+=1
    wyn2 = {}
    wyn3 = {}
    suma = 0
    suma2 = 0
    for i in sorted(wyn):
        #wyn2[i] = wyn[i]
        suma+=wyn[i]
        suma2+=i*wyn[i]
        m = 100*i
        m = int(m/10)
        try:
            wyn3["(" + str(m/10) + ", " + str((m/10) + 0.1) + ")"]+=wyn[i]
        except:
            wyn3["(" + str(m/10) + ", " + str((m/10) + 0.1) + ")"] = wyn[i]
        try:
            wyn2[m][i] = wyn[i]
        except:
            wyn2[m] = {}
            wyn2[m][i] = wyn[i]
    print("ILOŚ GIER(100 Zestawów): ", suma)
    print("ÓGÓLNA ŚREDNIA: ", suma2/suma)
    print("PRZEDZIAŁY: ", wyn3)
    for i in wyn2:
        print(wyn2[i])

    CzyIstnieje("wyniki2.xlsx")
    sheet = wb.active
    n = 2
    while sheet.cell(row=n, column=1).value != None:
        n = n + 1
    sheet.cell(row=n, column=1).value = suma
    sheet.cell(row=n, column=2).value = suma2/suma
    sheet.cell(row=n, column=3).value = str(wyn3)
    m = 4
    for i in wyn2:
        sheet.cell(row=n, column=m).value = str(wyn2[i])
        m+=1
    wb.save("wyniki2.xlsx")



def Testy():
    ilosc = 0
    wygrane = 0
    kart = 0
    pkt = {}

    karty, pomoc, aktualne, punkty = Zaczynamy()

    licznik = 0

    for q in range(5):
        czas = time.time()

        wyniki = []
        for i in range(10):
            while ilosc != 100:
                karty, pomoc, aktualne, punkty, ilosc, wygrane, kart, pkt = pruba4(karty, pomoc, aktualne, punkty, ilosc, wygrane, kart,pkt)
            lista = []
            dd = {}
            lista.append(wygrane/100)
            for i in sorted(pkt):
                dd[i] = pkt[i]
            lista.append(dd)
            wyniki.append(lista)
            wygrane = 0
            ilosc = 0
            pkt = {}
            licznik+=1
            print(licznik)

        suma = 0
        for i in wyniki:
            suma += i[0]

        print("WYNIKI: ", wyniki)
        print("ŚREDNIA: ",suma/len(wyniki))
        print("CZAS ALGORYTMU: ", time.time() - czas)

        Excel("Algorytm glebokoscR 2", "1000x5", suma / len(wyniki), time.time() - czas, str(wyniki))


Wyniki()
#Testy()
