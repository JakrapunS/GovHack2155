import requests
import pandas as pd
import json
from typing import Union

def prov_interface(
    series_id: int, 
    rows: int=100) -> dict:
    """
    Interface to PROV api using series id to search and limiting the number of rows

    Will return None if:
    - no search found. 

    """

    url = f'https://api.prov.vic.gov.au/search/query?rows={rows}&sort=Series_title%20asc&wt=json&q=(series_id%3A({series_id}))%20AND%20((record_form%3A%22Photograph%20or%20Image%22))'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP error status

    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)

    # slight error handling
    d = json.loads(response.text)

    if d['response']['numFound'] == 0:
        return None

    else: 
        return d

def update_link(
    link: str,
    size: tuple[int, int]) -> str:
    """
    Resizes the image
    
    """

    link_split = link.split("/")
    link_split[6] = f"!{size[0]},{size[1]}"

    return "/".join(link_split)

def make_data(
    series_id: str, 
    rows: int=100, 
    prefered_size: tuple[int, int]=(500,500)) -> pd.DataFrame:
    """
    Returns a dataframe with image links and descriptions from PROV. 

    Will return none if:
    - Empty search result.
    - No image file in result.  
    """


    data_dict = prov_interface(series_id)
    if data_dict is None:
        return None

    details = []
    for item in data_dict['response']['docs']:
        if "iiif-thumbnail" in item.keys():
            details.append({
                'link': update_link(item["iiif-thumbnail"], prefered_size),
                'description': item["presentation_text"]
            })

    if len(details) == 0:
        return None

    return pd.DataFrame(details)