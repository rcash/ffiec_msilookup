import requests
import json
class geocode_info():
    def __init__(self, useraddress):
        if len(useraddress) == 0:
            raise ValueError('ERROR: val must be greater than 0')
        #address/query for body of POST request
        self.__address = useraddress
        #url to grab from
        self.__posturl = 'https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx/GetGeocodeData'
        self.__postheader = {'Content-Type': 'application/json; charset=utf-8'}
        self.payload = {'sSingleLine': self.__address, 'iCensusYear': '2018'}
        self.__tract = ""
        self.__msa = ""
        self.__countycode = ""
        self.__addressfound = False

    def sendpost(self):
        r = requests.post(self.__posturl, data = json.dumps(self.payload), headers = self.__postheader)
        if r.status_code != 200:
            raise RunTimeError('POST request failed')
        print('Successful post request with query: ' + self.__address)
        return r.text

    def maniprequest(self, request):
        status = request.find('sStatus')
        if status != -1 and request[status + (len('sStatus') + 3)] == 'Y':
            self.__addressfound = True
            self.__tract = self.grab_tract(request)
            self.__msa = self.grab_msa(request)
            self.__countycode = self.grab_countycode(request)
            print('Tract and MSA found-tract: ' + self.__tract + ' msa: ' + self.__msa)
            print('countycode: ' + self.__countycode)
        #need to use countycode, not state code!!!
    def grab_countycode(self, request):
        countylen = len('sCountyCode')
        countyposition = request.find('sCountyCode')
        #county code will always be length 3, verified
        precountystart = countyposition + countylen + 3
        precounty = request[precountystart: precountystart + 3]
        #find two letter state sStateAbbr
        stateabbrlen = len('sStateAbbr')
        stateabbrposition = request.find('sStateAbbr')
        # +2 at end for the 2 letter code
        stateabbr = request[stateabbrposition + stateabbrlen + 3:
        stateabbrposition + stateabbrlen + 3 + 2]
        #add em up
        return stateabbr + precounty


    def grab_tract(self, request):
        #vals hardcoded, if geodec changes them this needs to be redone
        tractlen = len('sTractCode')
        tractposition = request.find('sTractCode')
        pretract = request[tractposition + tractlen + 3: tractposition +
        tractlen + 3 + 7] #7 is Msa string len init
        #drop the 0
        tract = pretract.replace('.','')
        #drop any 0s in front according to how pandas indexes
        tract = int(tract)
        tract = str(tract)
        return tract

    def grab_msa(self, result_string):
        #vals hardcoded, if geodec changes them this needs to be redone
        msaposition = result_string.find('sMSACode')
        msalen = len('sMSACode')
        msa = result_string[msaposition + msalen + 3: msaposition + msalen + 8]
        msa = int(msa)
        msa = str(msa)
        if msa == '99999':
            return '00000'
        return msa

    def set_msa(self, val):
        if len(val) == 0:
            raise ValueError('ERROR: val must be greater than 0')
        self.__msa = val

    def set_tract(self, val):
        if len(val) == 0:
            raise ValueError('ERROR: val must be greater than 0')
        self.__tract = val

    def set_countycode(self, val):
        if len(val) == 0:
            raise ValueError('ERROR: val must be greater than 0')
        self.__countycode = val

    def get_tract(self):
        if len(self.__tract) == 0:
            raise ValueError('ERROR: tract must be assigned with a length greater than 0.')
        return self.__tract

    def get_msa(self):
        if len(self.__msa) == 0:
            raise ValueError('ERROR: msa must be assigned with a length greater than 0.')
        return self.__msa

    def get_countycode(self):
        if len(self.__countycode) == 0:
            raise ValueError('ERROR: countycode must be assigned with a length greater than 0.')
        return self.__countycode

    def get_addr_status(self):
        return self.__addressfound

    def get_addr(self):
        return self.__address

    def set_addr(self, val):
        if len(val) == 0:
            raise ValueError('ERROR: val must be greater than 0')
        self.__address = val
