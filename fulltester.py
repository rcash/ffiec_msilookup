from geocodeinfo import geocode_info
from countydatainfo import countydata
import requests
import json
import sys

def main():
    #geodec = geocode_info('2701 wynfrey dr Prattville, AL 36067')
    geodec = geocode_info('349 County Road 24, International Falls, MN 56649')
    #print(geodec.get_addr_status())
    result = geodec.sendpost()
    geodec.maniprequest(result)
    if geodec.get_addr_status() == False:
        print('Address not found, please try again')
        sys.exit(0)
    else:
        print('geodec tract: ' + geodec.get_tract())
        print('geodec msa: ' + geodec.get_msa())
    cd = countydata('static/countydata.pk1')
    cd.set_tract(geodec.get_tract())
    cd.set_msa(geodec.get_msa())
    cd.set_countycode(geodec.get_countycode())
    cd.calcmaxmsa()
    print(cd.getmaxmsastat())
    print(cd.getmaxmsa())
main()
