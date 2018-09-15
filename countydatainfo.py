import pandas as pd

class countydata():
    def __init__(self, userfilename):
        if len(userfilename) == 0:
            raise ValueError('ERROR: filename length must be greater than 0')
        self.__filename = userfilename
        self.__df = pd.read_pickle(userfilename)
        self.__tract = ""
        self.__msa = ""
        self.__maxmsafound = False
        self.__maxmsa = ""
        self.__countycode = ""

    def calcmaxmsa(self):
        #col values hardcoded, will need to change if spreadsheet changes
        cd = self.__df[['TRACT','MSA2013','RURAL','Mi2018','STATE COUNTY CODE']]
        cdtract = self.__df.set_index('TRACT')
        #print(cdtract)
        #print(cdtract.loc[int(self.__tract)])
        val = -1
        if self.rowdoesexist():
            #means max msa can be found now that we know it's in spreadsheet
            self.__maxmsafound = True
            msastep = cdtract.loc[int(self.__tract)]
            if isinstance(msastep, pd.core.series.Series):
                #left with a series, only one possible Mi value
                self.__maxmsa = msastep.loc['Mi2018']
                print('Max msa found: ' + str(self.__maxmsa))
            else:
                #otherwise manip dataframe to get one val
                msastep = msastep.set_index('MSA2013')
                val = msastep.loc[int(self.__msa)]
                #singular value, don't need to check countycode because there are no others in file
                if isinstance(val, pd.core.series.Series):
                    resultant = val.at['Mi2018']
                else:
                    #update me when table changes
                    #resultant = val.iat[0,6]
                    resultantfinder = val.loc[int(self.get_msa()),'STATE COUNTY CODE']
                    count = 0
                    found = False
                    #loop thru list, find matching one, record its pos then
                    #grab its Msi
                    for n in resultantfinder:
                        if n == self.__countycode:
                            found = True
                        elif not found:
                            count = count + 1
                    resultant = val.iat[count, 6]
                #could still be multiple
                if isinstance(resultant, list):
                    self.__maxmsa = resultant[0]
                    print('Max msa found: ' + str(self.__maxmsa))
                else:
                    self.__maxmsa = resultant
                    print('Max msa found: ' + str(self.__maxmsa))

    def getmaxmsa(self):
        return self.__maxmsa

    def getmaxmsastat(self):
        return self.__maxmsafound

    def set_countycode(self, val):
        if len(val) == 0:
            raise ValueError('ERROR: val must be assigned with a length greater than 0')
        self.__countycode = val

    def get_countycode(self):
        if len(self.__countycode) == 0:
            raise ValueError('ERROR: countycode must be assigned with a length greater than 0.')
        return self.__countycode

    def set_msa(self, val):
        if len(val) == 0:
            raise ValueError('ERROR: val must be greater than 0')
        self.__msa = val

    def set_tract(self, val):
        if len(val) == 0:
            raise ValueError('ERROR: val must be greater than 0')
        self.__tract = val

    def get_tract(self):
        if len(self.__tract) == 0:
            raise ValueError('ERROR: tract must be assigned with a length greater than 0.')
        return self.__tract

    def get_msa(self):
        if len(self.__msa) == 0:
            raise ValueError('ERROR: msa must be assigned with a length greater than 0.')
        return self.__msa

    def rowdoesexist(self):
        dftract = self.__df.set_index('TRACT')
        foundtract = False
        #for loop bc using at with invalid tract will throw error
        for n in self.__df.index:
            if self.__df.at[n,'TRACT'] == int(self.__tract):
                foundtract = True
        if not foundtract:
            #not in df
            return False
        #matching tracts have now been found
        matchingtracts = dftract.loc[int(self.__tract)]
        #print(matchingtracts)
        msavals = ''
        #print(matchingtracts.loc['MSA2013'])
        #if series just grab msa val
        #series means we've got it down to one already
        #print(matchingtracts)
        if isinstance(matchingtracts, pd.core.series.Series):
            msavals = matchingtracts.loc['MSA2013']
            if int(self.__msa) == msavals:
                print('Successfully found msa pair for tract ' + self.__tract)
                return True
            else:
                return False
        else:
            #slice out cols we dont need, index on msa since all tracts are same
            msastate = matchingtracts.loc[:,['MSA2013','STATE COUNTY CODE']].set_index('MSA2013')
            #print(msastate)
            #print(msastate)
            #get ndarray of state county codes to make sure you grab the right one
            foundmsa = False
            #check to see that MSA is in index before working off of it
            for n in msastate.index:
                if n == int(self.get_msa()):
                    foundmsa = True
            #know we can now index on msa
            if not foundmsa:
                return False
            msavalstest = msastate.at[int(self.__msa),'STATE COUNTY CODE']
            #print('MSAVALSTEST')
            #print(self.__msa)
            #if string we found it, otherwise if list there is more work to do
            if(isinstance(msavalstest, str)):
                print('row does exist for tract: ' +
                self.get_tract() + ' msa: ' + self.get_msa() +
                ' countycode: ' + self.get_countycode())
                return True
            else:
                for n in msavalstest:
                    if self.get_countycode() == n:
                        print('row does exist for tract: ' +
                        self.get_tract() + ' msa: ' + self.get_msa() +
                        ' countycode: ' + self.get_countycode())
                        return True
            print('did not find it')
            return False
            #statecodes = matchingtracts.loc['STATE COUNTY CODE']
            #print(statecodes)
            #msavals = matchingtracts.at[int(self.__tract),'MSA2013']
            '''
            for n in msavals:
                if int(self.__msa) == n:
                    print('Successfully found msa pair for tract ' + self.__tract)
                    return True
            return False
            '''
