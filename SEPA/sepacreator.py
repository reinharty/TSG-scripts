#!/usr/bin/python
import pandas as pd
from math import ceil
from SEPA import configuration
import datetime
import os
from SEPA.sepa_file_generator import SEPAPaymentGenerator
from SEPA.zipper import zipadd


class SEPACreator:

    # depends on format and positions of columns in input file
    quartal_dict = {1:7, 2:9, 3:11, 4:13}
    abteilungen_dict = {"Abteilung BA": "Basketball", "Abteilung FU": "Fussball", "Abteilung HO": "Hockey",
                        "Abteilung LA": "Leichtathletik", "Abteilung TT": "Tischtennis", "Abteilung TU": "Turnen", "Gesamtverein": "Gesamtverein"}

    config = abteilung = timestamp = input_excel_file = output_names_file = None
    row_list = []

    sepafile_name = ""

    #dataFramePayments = pd.DataFrame(columns=['Abteilung', 'Name', 'IBAN', 'BIC', 'Betrag'])
    dataFramePayments = None
    dataFrameNames = pd.DataFrame(columns=['Abteilung', 'Name'])

    def __init__(self, config: configuration.Configuration):

        self.config = config
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d")

        self.input_excel_file = pd.read_excel(str(self.config.path_to_input_folder + self.config.input_filename), sheet_name=str(self.config.sheet_name))
        self.output_names_file = "" + self.timestamp + "-" + self.config.output_names_file + ".csv"

        print(str(self.input_excel_file.iloc[2, 0]))
        print(self.abteilungen_dict.get(self.input_excel_file.iloc[2,0], "unbekannt"))

    def createListOfRows(self):

        abteilung = None

        for i in range(2,len(self.input_excel_file.index)):

            ## passt die zwischengespeicherte Abteilung an und speichert die aktuelle Abteilung in "abteilung"
            a = (self.abteilungen_dict.get(self.input_excel_file.iloc[i,0], "unbekannt"))
            if (a != "unbekannt"):
                abteilung = a

            #QUARTAL
            a = (self.input_excel_file.iloc[i,self.quartal_dict.get(self.config.quarter)])#setzt das Quartal
            iban = self.input_excel_file.iloc[i,1]
            if a != 0 and pd.notna(a) and pd.notna(iban) and (iban != "mit Lizenz" or iban != "ohne Lizenz") and iban != "IBAN" and ("Zwischensumme" not in self.input_excel_file.iloc[i,0]):
                #zum aufrunden
                a = ceil(a * 100) / 100.0
                self.row_list.append((abteilung, self.input_excel_file.iloc[i,0], iban, str(self.input_excel_file.iloc[i,2]).upper(), a))

    def createPaymentsDataFrame(self):
        self.dataFramePayments = pd.DataFrame(self.row_list, columns=['Abteilung', 'Name', 'IBAN', 'BIC', 'Betrag'])

        print(self.dataFramePayments)
        print(self.dataFramePayments['Betrag'].sum())

    def createUebungsleiterliste(self):
        self.output_names_file = "" + self.timestamp + "-" + self.config.output_names_file +".xlsx"

        # Zeilen herausfiltern, bei denen 'Abteilung' == 'Gesamtverein' ist
        df_filtered = self.dataFramePayments[self.dataFramePayments['Abteilung'] != 'Gesamtverein']
        df_filtered.to_excel(self.output_names_file, index=False, columns=['Abteilung', 'Name'], engine='xlsxwriter')

    def createSEPAxml(self):
        z = SEPAPaymentGenerator(self.config, self.dataFramePayments)
        self.sepafile_name = z.generatePayments()

    def createBegleitzettel(self):
        self.row_list.append((None, None, None, "Gesamtbetrag", self.dataFramePayments['Betrag'].sum()))
        df = pd.DataFrame(self.row_list, columns=['Abteilung', 'Name', 'IBAN', 'BIC', 'Betrag'])
        df.to_excel('Begleitzettel.xlsx', index=False, engine='xlsxwriter')

    def createZip(self):
        try:
            os.remove("Überweisungen_Übungsleiter.zip") #remove zip of a prior run
        finally:
            zipadd("Überweisungen_Übungsleiter.zip", self.sepafile_name)
            zipadd("Überweisungen_Übungsleiter.zip", self.output_names_file)
            zipadd("Überweisungen_Übungsleiter.zip", "Begleitzettel.xlsx")
            print("Created Überweisungen_Übungsleiter.zip")

    def run(self):
        self.createListOfRows()
        self.createPaymentsDataFrame()
        self.createUebungsleiterliste()
        self.createSEPAxml()
        self.createBegleitzettel()
        self.createZip()

        print("Finished SEPA run")