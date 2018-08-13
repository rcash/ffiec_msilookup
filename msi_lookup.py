##TODO:
#1.define types i.e. str() or int() for each function that needs it
#2.move non-flask functions into another file
#3.beautify with bootstrap
#4.deploy to server
#5.find some testcases!

import requests
import json
import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)
@app.route('/')
def my_form():
    return render_template("tract_search.html")
@app.route('/', methods=['POST'])

def my_form_post():
    text = request.form['text']
    vals = grabinfo(text)
    if not vals:
        return 'Please check spelling and try again! Return to the previous page'
    else:
        #call fxn for rest of shit
        if dataframehandling(vals) == -1:
            return 'No.'
        else:
            return 'Yes! Msi2018: ' + str(dataframehandling(vals))

def dataframehandling(tractandmsa):
    return getresponse(tractandmsa[0], tractandmsa[1])

def grabinfo(address):
    geopage = 'https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx/GetGeocodeData'
    #specify content type to get JSON back
    workingheader = {'Content-Type': 'application/json; charset=utf-8'}
    #change values for things we want
    payload = {'sSingleLine': address, 'iCensusYear': '2018'}
    #only need payload as a string-still use .dumps to take care of it
    r = requests.post(geopage, data=json.dumps(payload), headers=workingheader)
    #print(r.status_code)
    results = []
    if r.status_code != 200:
        print('POST REQUEST FAILED')
    else:
        print('successful POST request')
        result = r.text
        status = result.find('sStatus')
        #print(result[status + (len('sStatus') + 3)])
        if status != -1 and result[status + (len('sStatus') + 3)] == 'Y':
            print('Address found')
            tract = tract_manip(result)
            msa = msa_manip(result)
            print('tract: ' + tract)
            print('msa: ' + msa)
            #add to list
            results.append(tract)
            results.append(msa)
        else:
            #return empty list
            print('invalid address, please restart')
    return results

def tract_manip(result_string):
    tractlen = len('sTractCode')
    tractposition = result_string.find('sTractCode')
    pretract = result_string[tractposition + tractlen + 3: tractposition +
    tractlen + 10]
    #drop the 0
    tract = pretract.replace('.','')
    #drop any 0s in front according to how pandas indexes
    tract = int(tract)
    tract = str(tract)
    return tract

def msa_manip(result_string):
    msaposition = result_string.find('sMSACode')
    msalen = len('sMSACode')
    msa = result_string[msaposition + msalen + 3: msaposition + msalen + 8]
    msa = int(msa)
    msa = str(msa)
    return msa

def getresponse(tract, msa):
    filename = 'countydata.pk1'
    countydata = builddataframe(filename)
    cd = countydata[['TRACT','MSA2013','RURAL','Mi2018']]
    cdmsahead = cd
    cdmsahead = cdmsahead.set_index('TRACT')
    if tractandmsaincountydata(tract, msa, cd):
        print('BOOM! got to the last step')
        #tracts not unique, get right MSA as well
        msastep = cdmsahead.loc[int(tract)].set_index('MSA2013')
        resultant = msastep.at[int(msa),'Mi2018']
        if isinstance(resultant, list):
            #all will be same, just need one
            return resultant[0]
        else:
            return resultant
    else:
        return -1

#must be valid, add safety check later
def builddataframe(filename):
    return pd.read_pickle(filename)

def tractandmsaincountydata(trac, msa, cdo):
    cond1 = False;
    cond2 = False;
    for n in cdo['TRACT']:
        if n == int(trac):
            cond1 = True;
    for n in cdo['MSA2013']:
        if n == int(msa):
            cond2 = True;
    return cond1 & cond2

#usual stuff
if __name__ == '__main__':
    app.run()
