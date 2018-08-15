import requests
import json
class geocode_info():
    def __init__(self, useraddress):
        if len(useraddress) == 0:
            raise ValueError('ERROR: val must be greater than 0')
        #address/query for body of POST request
        self.address = useraddress
        #url to grab from
        self.posturl = 'https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx/GetGeocodeData'
        self.postheader = {'Content-Type': 'application/json; charset=utf-8'}
        self.payload = {'sSingleLine': self.address, 'iCensusYear': '2018'}
        self.tract = ""
        self.msa = ""
        self.addressfound = False

    def sendpost(self):
        r = requests.post(self.posturl, data = json.dumps(self.payload), headers = self.postheader)
        if r.status_code != 200:
            raise RunTimeError('POST request failed')
        return r.text

    def maniprequest(self, request):
        status = request.find('sStatus')
        if status != -1 and request[status + (len('sStatus') + 3)] == 'Y':
            self.addressfound = True
            self.tract = self.grab_tract(request)
            self.msa = self.grab_msa(request)

    def grab_tract(self, request_string):
        #vals hardcoded, if geodec changes them this needs to be redone
        tractlen = len('sTractCode')
        tractposition = request_string.find('sTractCode')
        pretract = request_string[tractposition + tractlen + 3: tractposition +
        tractlen + 10]
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
        return msa

    def set_msa(self, val):
        if len(val) == 0:
            raise ValueError('ERROR: val must be greater than 0')
        self.msa = val

    def set_tract(self, val):
        if len(val) == 0:
            raise ValueError('ERROR: val must be greater than 0')
        self.tract = val

    def get_tract(self):
        if len(self.tract) == 0:
            raise ValueError('ERROR: tract must be assigned with a length greater than 0.')
        return self.tract

    def get_msa(self):
        if len(self.msa) == 0:
            raise ValueError('ERROR: msa must be assigned with a length greater than 0.')
        return self.msa

    def get_addr_status(self):
        return self.addressfound
