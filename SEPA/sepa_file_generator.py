#!/usr/bin/python
import pandas as pd
import datetime
import configuration
from schwifty import *

class SEPAPaymentGenerator:
 #todo alles mit config ersetzen
    filename = None
    df = None
    date = None
    text = None
    summe = None
    numLines = None
    counter = 0

    config = None

    iban = None
    bic = None
    name = None
    betrag = None

    def __init__(self, config: configuration.Configuration, dataFrame: pd.DataFrame):

        self.config = config

        self.date = datetime.date
        now = datetime.datetime.now()
        self.filename = now.strftime("%Y%m%d")+"-SEPA.xml"
        self.df = dataFrame
        self.summe = round(self.df['Betrag'].sum(), 2)
        self.numLines = len(self.df.index)
        self.counter = 0


    def extendBIC(self, bic: str):
        while (len(bic) < 11):
            bic += "X"
        return bic

    def generatePayments(self):
        now2 = datetime.datetime.now()
        now = now2.strftime("%Y-%m-%dT%H:%M:%S")
        text = '<?xml version="1.0" encoding="UTF-8"?><Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03"><CstmrCdtTrfInitn><GrpHdr>\n'
        text += '<MsgId>Proficash-' + now + '</MsgId><CreDtTm>' + now + '</CreDtTm><NbOfTxs>' + str(self.numLines) + '</NbOfTxs><CtrlSum>'+ str(self.summe) +'</CtrlSum>\n'
        text += '<InitgPty><Nm>' + self.config.iban_name + '</Nm></InitgPty></GrpHdr><PmtInf><PmtInfId>Proficash-' + now + '</PmtInfId><PmtMtd>TRF</PmtMtd><BtchBookg>true</BtchBookg>'
        text += '<NbOfTxs>' + str(self.numLines) + '</NbOfTxs><CtrlSum>' + str(self.summe) + '</CtrlSum>'
        text += '<PmtTpInf><InstrPrty>NORM</InstrPrty><SvcLvl><Cd>SEPA</Cd></SvcLvl></PmtTpInf><ReqdExctnDt>' + now2.strftime("%Y-%m-%d") + '</ReqdExctnDt><Dbtr><Nm>' + self.config.iban_name + '</Nm></Dbtr><DbtrAcct><Id><IBAN>' + self.config.iban + '</IBAN></Id></DbtrAcct><DbtrAgt><FinInstnId><BIC>' + self.config.bic + '</BIC></FinInstnId></DbtrAgt><ChrgBr>SLEV</ChrgBr>\n'

        for i in range(0, self.numLines):
            self.name = self.df.iloc[i, 1]
            self.iban = str(self.df.iloc[i, 2]).strip()
            self.bic = self.extendBIC(self.df.iloc[i, 3])
            self.betrag = self.df.iloc[i, 4]

            print(self.name)
            IBAN(self.iban).validate(True)
            BIC(self.bic).validate()

            text += '<CdtTrfTxInf><PmtId><InstrId>' + str(self.counter+1) + \
                    '</InstrId><EndToEndId>NOTPROVIDED</EndToEndId></PmtId><Amt><InstdAmt Ccy="EUR">' + \
                    "{:.2f}".format(float(self.betrag)) + '</InstdAmt></Amt><CdtrAgt><FinInstnId><BIC>' + \
                    self.bic + '</BIC></FinInstnId></CdtrAgt><Cdtr><Nm>' + self.name +'</Nm></Cdtr><CdtrAcct><Id><IBAN>' \
                    + self.iban +'</IBAN></Id></CdtrAcct><RmtInf><Ustrd>'+self.config.iban_message+' '+str(self.config.quarter)+'</Ustrd></RmtInf></CdtTrfTxInf>\n'
            self.counter += 1

        text += '</PmtInf></CstmrCdtTrfInitn></Document>'

        f = open(self.filename, "w", encoding="utf-8")
        f.write(text)
        f.close()

        print(text)
        return self.filename
