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

    def calcmaxmsa(self):
        #col values hardcoded, will need to change if spreadsheet changes
        cd = self.__df[['TRACT','MSA2013','RURAL','Mi2018']]
        cdtract = self.__df.set_index('TRACT')
        #print('cdtract')
        #print(cdtract.loc[int(self.__tract)])
        #print goes off here in rowdoesexist
        val = -1
        if self.rowdoesexist():
            self.__maxmsafound = True
            msastep = cdtract.loc[int(self.__tract)]
            if isinstance(msastep, pd.core.series.Series):
                #left with a series, only one possible Mi value
                self.__maxmsa = msastep.loc['Mi2018']
            else:
                #otherwise manip dataframe to get one val
                msastep = msastep.set_index('MSA2013')
                val = msastep.loc[int(self.__msa)]
                resultant = val.at['Mi2018']
                #could still be multiple
                if isinstance(resultant, list):
                    self.__maxmsa = resultant[0]
                else:
                    self.__maxmsa = resultant

    def getmaxmsa(self):
        return self.__maxmsa

    def getmaxmsastat(self):
        return self.__maxmsafound

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
        for n in self.__df.index:
            if self.__df.at[n,'TRACT'] == int(self.__tract):
                foundtract = True
        if not foundtract:
            return False
        matchingtracts = dftract.loc[int(self.__tract)]
        #print(matchingtracts)
        msavals = ''
        #print(matchingtracts.loc['MSA2013'])
        #if series just grab msa val
        if isinstance(matchingtracts, pd.core.series.Series):
            msavals = matchingtracts.loc['MSA2013']
            if int(self.__msa) == msavals:
                return True
            else:
                return False
        else:
            msavals = matchingtracts.at[int(self.__tract),'MSA2013']
        for n in msavals:
            if int(self.__msa) == n:
                return True
        return False
