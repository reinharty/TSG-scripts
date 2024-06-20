import pandas as pd
from datetime import datetime

# Identifiziere ausgetretene Mitglieder die in der App noch Mitglied sind, um diese auf Nichtmitglied umzustellen.

dfApp = pd.read_excel(r'C:\Users\Yorrick\IdeaProjects\rewrite\app-austritte\App-Users.xlsx', sheet_name = r'Mitgliederverzeichnis')
dfAus = pd.read_csv(r'C:\Users\Yorrick\IdeaProjects\rewrite\app-austritte\austritte.csv', sep=";")
dfOut = pd.DataFrame(columns = ['nr', 'mail'])

setApp = set()
setAus = set()

for i in range(0, len(dfApp)):
    mitgliedsnummer = dfApp.iloc[i,26]

    if (pd.notnull(mitgliedsnummer)):
        setApp.add(int(mitgliedsnummer))

print("Teil 1 fertig")

for i in range(0, len(dfAus)):

    txt = (dfAus.iloc[i, 0])
    txt = int(txt[2:len(txt)])

    setAus.add(txt)

print("Teil 2 fertig")

setUnion = setApp.intersection(setAus)

print(setUnion)
