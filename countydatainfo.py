import pandas as pd

class countydata():
    dataframe
    def __init__(self, userfilename):
        if len(userfilename) == 0:
            raise ValueError('ERROR: filename length must be greater than 0')
        self.__filename = userfilename
        self.__df = read_pickle(userfilename)
        self.__tract = ""
        self.__msa = ""
        self.__maxmsafound = False
        self.__maxmsa = ""

    def getmaxmsa(self):
        #col values hardcoded, will need to change if spreadsheet changes
        cd = countydata[['TRACT','MSA2013','RURAL','Mi2018']]
        cdtract = countydata.set_index('TRACT')
        if self.rowdoesexist():
            self.__maxmsafound = True
            msastep = cdtract.loc[int(self.__tract)].set_index('MSA2013')
            val = msastep.loc[int(self.__msa)]
            resultant = val.at['Mi2018']
            if isinstance(resultant, list):
                self.__maxmsa = resultant[0]
            else:
                self.__maxmsa = resultant

    def rowdoesexist(self):
        dftract = self.__df.set_index('self.__tract')
        foundtract = False
        for n in self.__df.index:
            if self.__df.at[n,'TRACT'] == int(self.__tract):
                foundtract = True
        if not foundtract:
            return False
        matchingtracts = dftract.loc[int(self.__tract)]
        msavals = matchingtracts.at[int(self.__tract),'MSA2013']
        for n in msavals:
            if int(self.__msa) == n:
                return True
        return False

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
