##TODO:
#1.move non-flask functions into another file
#2.beautify with bootstrap
#3.deploy to server
#4.find some testcases!

import requests
import json
import pandas as pd
from flask import Flask, request, render_template
from geocodeinfo import geocode_info

app = Flask(__name__)
@app.route('/')
def my_form():
    return render_template("tract_search.html")
@app.route('/', methods=['POST'])

def my_form_post():
    text = request.form['text']
    geodec = geocode_info(text)
    geodec.maniprequest(geodec.sendpost())
    if geodec.get_addr_status() == False:
        return 'Please check spelling and try again! Return to the previous page'
    else:
        vals = []
        vals.append(geodec.get_tract())
        vals.append(geodec.get_msa())
        #call fxn for rest of shit
        if dataframehandling(vals) == -1:
            return 'No.'
        else:
            return 'Yes! Msi2018: ' + str(dataframehandling(vals))

def dataframehandling(tractandmsa):
    return getresponse(tractandmsa[0], tractandmsa[1])

def getresponse(tract, msa):
    filename = 'countydata.pk1'
    countydata = builddataframe(filename)
    cd = countydata[['TRACT','MSA2013','RURAL','Mi2018']]
    cdtract = countydata.set_index('TRACT')
    if rowdoesexist(cd, tract, msa):
        print('BOOM! got to the last step')
        #tracts not unique, get right MSA as well
        msastep = cdtract.loc[int(tract)].set_index('MSA2013')
        print(msastep)
        val = msastep.loc[int(msa)]
        resultant = val.at['Mi2018']
        if isinstance(resultant, list):
            #all will be same, just need one
            print('almost done, i am a list')
            print(type(resultant[0]))
            return resultant[0]
        else:
            print('almost done, i am single ;S')
            return resultant
    else:
        return -1

#must be valid, add safety check later
def builddataframe(filename):
    return pd.read_pickle(filename)

def rowdoesexist(df, tract, msa):
    dftract = df.set_index('TRACT')
    foundtract = False
    for n in df.index:
        if df.at[n,'TRACT'] == int(tract):
            foundtract = True
    if not foundtract:
        return False
    matchingtracts = dftract.loc[int(tract)]
    msavals = matchingtracts.at[int(tract),'MSA2013']
    for n in msavals:
        if int(msa) == n:
            return True
    return False

#usual stuff
if __name__ == '__main__':
    app.run(debug=True)
