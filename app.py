##TODO:
#set up a logging schema
import os
import requests
import json
import pandas as pd
from flask import Flask, request, render_template, flash
from geocodeinfo import geocode_info
from countydatainfo import countydata
from boto.s3.connection import S3Connection
app = Flask(__name__)
app.secret_key = S3Connection(os.environ['SECRET_KEY'], os.environ['SECRET_KEY'])
@app.route('/')
def msi_lookup():
    return render_template("tract_search.html")

@app.route('/', methods=['POST'])
def msi_lookup_post():
    text = request.form['text']
    if text == "" or " ":
        flash('Please enter a valid address.')
    else:
        geodec = geocode_info(text)
        geodec.maniprequest(geodec.sendpost())
        if geodec.get_addr_status() == False:
            flash('Please check spelling for "' + geodec.get_addr() + '" and try again!')
        else:
            #call fxn for rest of shit
            returnval = dataframehandling(geodec)
            if returnval == -1:
                flash('"' + geodec.get_addr() + '" is not eligible.')
            else:
                flash('"' + geodec.get_addr() + '" is eligible, AMI: ' + str(returnval))
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
