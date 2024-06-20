import pandas as pd
import os

#quartal = int(input("Quartal: "))
filename = "Zeiten.xlsx" #input("Filename: ")

dfStunden = pd.read_excel(filename)

dfNAN = pd.DataFrame(columns=['Name', 'Gesamte Stunden'])
dfBA = pd.DataFrame(columns=['Name', 'Gesamte Stunden'])
dfHO = pd.DataFrame(columns=['Name', 'Gesamte Stunden'])
dfFU = pd.DataFrame(columns=['Name', 'Gesamte Stunden'])
dfLA = pd.DataFrame(columns=['Name', 'Gesamte Stunden'])
dfTU = pd.DataFrame(columns=['Name', 'Gesamte Stunden'])
dfTT = pd.DataFrame(columns=['Name', 'Gesamte Stunden'])

dfPerson = pd.DataFrame(columns=['Name', 'Datum', 'Titel', 'Stunden', 'Abteilung', 'Notiz', 'Eingereicht'])


namenDict = dict()
namenListe = []

dfZeilen = pd.DataFrame(columns=['Name', 'Datum', 'Titel', 'Stunden', 'Abteilung', 'Notiz', 'Eingereicht'])

# create a list of all names
for i in range(0, len(dfStunden)):
    name = dfStunden.iloc[i,0].replace("  ", " ").strip()
    abteilung = dfStunden.iloc[i,4]
    if name not in namenDict:
        namenListe.append([name,abteilung])
        namenDict[name] = i

namenListe.sort()
for i in range(0, len(namenListe)):
    print(namenListe[i])

# gesamte stunden berechnen
for i in range(0, len(namenListe)):
    nameTouple = namenListe[i]
    name = nameTouple[0]
    summeStunden = 0
    list_rows =[]
    for j in range(0, len(dfStunden)):
        stundenName = dfStunden.iloc[j,0].replace("  ", " ").strip().lower()
        if stundenName == name.lower():
            summeStunden += float(dfStunden.iloc[j,3])
            datum = dfStunden.iloc[j,1]
            titel = dfStunden.iloc[j,2]
            stunden = dfStunden.iloc[j,3]
            abteilung = dfStunden.iloc[j,4]
            notiz = dfStunden.iloc[j,5]
            eingereicht = dfStunden.iloc[j,6]
            row = [name, summeStunden]
            #row = [name, datum, titel, stunden, abteilung, notiz, eingereicht]
            #list_rows.append(row)

            #if abteilung == "LA":
            #    dfTrainer = pd.DataFrame(columns=['Name', 'Datum', 'Titel', 'Stunden', 'Abteilung', 'Notiz', 'Eingereicht'])
            #    dfTrainer.loc[len(dfLA)] = row
            #    dfTrainer.to_excel('LA/'+name+'.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')


    print(name, summeStunden)

    #Uebersicht fuer BA
    if nameTouple[1] == 'Basketball':
        dfBA.loc[len(dfBA)] = [name, summeStunden]
        dfBA.to_excel('BA.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
        #Uebersicht fuer HO
    elif nameTouple[1] == 'Hockey':
        dfHO.loc[len(dfHO)] = [name, summeStunden]
        dfHO.to_excel('HO.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
        #Uebersicht fuer FU
    elif nameTouple[1] == 'Fußball':
        dfFU.loc[len(dfFU)] = [name, summeStunden]
        dfFU.to_excel('FU.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    #Uebersicht fuer LA
    elif nameTouple[1] == 'Leichtathletik':
        dfLA.loc[len(dfLA)] = [name, summeStunden]
        dfLA.to_excel('LA.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    #Uebersicht fuer TT
    elif nameTouple[1] == 'Tischtennis':
        dfTT.loc[len(dfTT)] = [name, summeStunden]
        dfTT.to_excel('TT.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    #Uebersicht fuer LA
    elif nameTouple[1] == 'Turnen':
        dfTU.loc[len(dfTU)] = [name, summeStunden]
        dfTU.to_excel('TU.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    #Uebersicht fuer ohne Abteilung
    else:
        dfNAN.loc[len(dfNAN)] = [name, summeStunden]
        dfNAN.to_excel('OhneAbteilung.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')


    # alle eintraege einer person in ein eigenes sheet

os.mkdir("BA")
os.mkdir("HO")
os.mkdir("FU")
os.mkdir("LA")
os.mkdir("TT")
os.mkdir("TU")
os.mkdir("Ohne-Abteilung")

for i in range(0, len(namenListe)):
    nameTouple = namenListe[i]
    name = nameTouple[0]
    list_rows =[]
    for j in range(0, len(dfStunden)):
        stundenName = dfStunden.iloc[j,0].replace("  ", " ").strip().lower()
        if stundenName == name.lower():
            datum = dfStunden.iloc[j,1]
            titel = dfStunden.iloc[j,2]
            stunden = dfStunden.iloc[j,3]
            abteilung = dfStunden.iloc[j,4]
            notiz = dfStunden.iloc[j,5]
            eingereicht = dfStunden.iloc[j,6]
            row = [name, datum, titel, stunden, abteilung, notiz, eingereicht]
            list_rows.append(row)
            #print(row)
            dfPerson.loc[len(dfPerson)] = row

    if abteilung == "Basketball":
        dfPerson.to_excel('BA/'+name+'.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    elif abteilung == "Fußball":
        dfPerson.to_excel('FU/'+name+'.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    elif abteilung == "Hockey":
        dfPerson.to_excel('HO/'+name+'.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    elif abteilung == "Leichtathletik":
        dfPerson.to_excel('LA/'+name+'.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    elif abteilung == "Tischtennis":
        dfPerson.to_excel('TT/'+name+'.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    elif abteilung == "Turnen":
        dfPerson.to_excel('TU/'+name+'.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    else:
        dfPerson.to_excel('Ohne-Abteilung/'+name+'.xlsx', sheet_name="Uebersicht", index=False, engine='xlsxwriter')
    dfPerson = dfPerson.iloc[0:0]








#print(namen.keys())
#print(namen.values())
