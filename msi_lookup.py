##TODO:
#2.beautify with bootstrap
#3.deploy to server
#4.find some testcases!

import requests
import json
import pandas as pd
from flask import Flask, request, render_template, flash
from geocodeinfo import geocode_info
from countydatainfo import countydata

app = Flask(__name__)
app.secret_key = 'inobv secret key'
@app.route('/')
def msi_lookup():
    return render_template("tract_search.html")

@app.route('/', methods=['POST'])
def msi_lookup_post():
    text = request.form['text']
    geodec = geocode_info(text)
    geodec.maniprequest(geodec.sendpost())
    if geodec.get_addr_status() == False:
        return 'Please check spelling and try again! Return to the previous page'
    else:
        #call fxn for rest of shit
        returnval = dataframehandling(geodec)
        if returnval == -1:
            flash('Not Eligible')
        else:
            flash('Eligible, Max AMI: ' + str(returnval))
        return render_template("tract_search.html")

def dataframehandling(geocode):
    cd = countydata('countydata.pk1')
    cd.set_tract(geocode.get_tract())
    cd.set_msa(geocode.get_msa())
    cd.set_countycode(geocode.get_countycode())
    print('BOOOM! 1')
    print(cd.get_countycode())
    print('BOOOM! 2')
    cd.calcmaxmsa()
    if cd.getmaxmsastat() == False:
        return -1
    else:
        return cd.getmaxmsa()

#usual stuff
if __name__ == '__main__':
    app.run(debug=True)
