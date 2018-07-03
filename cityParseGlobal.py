### Author: Matthew Phelps, Updated: July 2 2018
###         IT Application Development Intern
###         iTek Center, Red Wolves skill team
###         Ford Motor Company

from myUtil.AddressImporter import AddressImporter
from myUtil.Configuration import Configuration
from myUtil.Address import Address
from myUtil import Timer
from myUtil.GTNAddressLookup import GTNAddressLookup
from myUtil.IncompleteGlobalDealerAddresses import IncompleteGlobalDealerAddresses
from myUtil.CompleteGlobalDealerAddresses import CompleteGlobalDealerAddresses
import pandas as pd
import numpy as np

## File configuration (edit the class to change file locations, names, or excel sheets)
config = Configuration()


## Create Virtual GTN Address Book
approvedAddressesDataFrame = pd.read_excel(pd.ExcelFile(config.approvedGTNAddrExcel), config.approvedGTNSheetName)
ai = AddressImporter()
addressBook = ai.loadGTNApprovedAddressesCitiesAndCountries(approvedAddressesDataFrame)

# (In)complete address lists setup
myTimer = Timer.Timer()
myTimer.start('Instantiate Incomplete/Complete and load, copy, and add new columns')
incomplete = IncompleteGlobalDealerAddresses(config)
complete = CompleteGlobalDealerAddresses(config)
complete.copyIncompleteAddrDFasTemplateAndAddColumns(incomplete.incompleteAddrDF)
myTimer.end()

## Begin iteration over address list

myTimer.start('Iteration and lookup')
for index, addressData in complete.completeAddrDF.iterrows():
    lookup = GTNAddressLookup()

    thisAddr = Address(city=addressData.loc['City'],
                               countryName=addressData.loc['Country Name'],
                               add1=addressData.loc['Address 1'],
                               add2=addressData.loc['Address 2'],
                               postalCode=addressData.loc['Postal Code'])
    '''
    # City
    for addressElement in [thisAddr.city, thisAddr.add1, thisAddr.add2]:
        cityFoundFromLookup = lookup.lookupCity(addressElement,addressBook)
        if cityFoundFromLookup:
            complete.completeAddrDF[index][['City']] = cityFoundFromLookup
            break
    '''
myTimer.end()
