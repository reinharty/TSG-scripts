#!/usr/bin/python
import configuration
from SEPA.sepacreator import SEPACreator

quartal = int(input("Quartal: "))
filename = input("Filename: ")

config = configuration.Configuration(quartal, filename)

s = SEPACreator(config)
s.run()