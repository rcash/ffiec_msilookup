##TODO:
#beautify
#add CDN, local as fallback
#set up a logging schema

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
        flash('Please check spelling and try again! Return to the previous page')
    else:
        #call fxn for rest of shit
        returnval = dataframehandling(geodec)
        if returnval == -1:
            flash('Not Eligible')
        else:
            flash('Eligible, Max AMI: ' + str(returnval))
    return render_template("tract_search.html")

def dataframehandling(geocode):
    cd = countydata('static/countydata.pk1')
    cd.set_tract(geocode.get_tract())
    cd.set_msa(geocode.get_msa())
    cd.calcmaxmsa()
    if cd.getmaxmsastat() == False:
        return -1
    else:
        return cd.getmaxmsa()

#usual stuff
if __name__ == '__main__':
    app.run(debug=True)