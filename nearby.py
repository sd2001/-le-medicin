import geocoder
from serpwow.google_search_results import GoogleSearchResults
import json
ipad=geocoder.ip('me')
serpwow = GoogleSearchResults("883CB6B9970E4AE1858E3381DF8F0674")

def hospital_search(place):
    q="Good hospitals near "+place
    l=place+","+str(ipad[0])
    params = {
    "q" : q,
    "location":l,
    "hl" : "en",
    }    

    # retrieve the Google search results as JSON
    result_json = serpwow.get_json(params)
    names=result_json['local_results']
    return names  
    
    
    
def pharmacy_search(place):
    q="Good Medical shops near "+place
    l=place+","+str(ipad[0])
    params = {
    "q" : q,
    "location":l,
    "hl" : "en",
    }    

    # retrieve the Google search results as JSON
    result_json = serpwow.get_json(params)
    names=result_json['local_results']
    return names  
    
    