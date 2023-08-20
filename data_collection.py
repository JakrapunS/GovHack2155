import requests
import pandas as pd
import json
from typing import Union

def prov_serial_interface(
    series_id: int, 
    rows: int=100) -> Union[dict, None]:
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

def prov_kw_interface(
    keyword: str,
    rows: int=100,
)-> Union[dict, None]:
    """
    Interface to PROV api using keyword to search and limiting the number of rows

    Will return None if:
    - no search found. 

    """
    
    url = f'https://api.prov.vic.gov.au/search/query?rows={rows}&wt=json&q=(text%3A%22{keyword}%22)%20AND%20((record_form%3A%22Photograph%20or%20Image%22))'
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

def section_link_builder(id: str):
    return f"https://prov.vic.gov.au/archive/{id}"

def make_data(
    search_key: Union[int, str], 
    rows: int=100, 
    prefered_size: tuple[int, int]=(500,500)) -> pd.DataFrame:
    """
    Returns a dataframe with image links and descriptions from PROV. 

    Will return none if:
    - Empty search result.
    - No image file in result.  
    """

    if isinstance(search_key, str):
        data_dict = prov_kw_interface(search_key)
    elif isinstance(search_key, int):
        data_dict = prov_serial_interface(search_key)
    else:
        return None

    if data_dict is None:
        return None

    details = []
    for item in data_dict['response']['docs']:
        if "iiif-thumbnail" in item.keys():
            details.append({
                'link': update_link(item["iiif-thumbnail"], prefered_size),
                'description': item["presentation_text"],
                'archive_link': section_link_builder(item["_id"]),
            })

    if len(details) == 0:
        return None

    return pd.DataFrame(details)