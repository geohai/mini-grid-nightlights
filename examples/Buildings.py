import yaml
import pandas as pd
import geopandas as gpd
import os
from shapely.geometry import Polygon
import folium
import requests
from sklearn.cluster import DBSCAN
from geopy.distance import geodesic
import simplekml
import osmnx as ox
from tqdm import tqdm
import numpy as np
from shapely.ops import transform 
from functools import partial
import pyproj

 
def get_mapbox_token(config_path: str = "user_config.yml") -> str:

    """

    Gets the MapBox token in the user_config.yml file in a OS agnostic manner.

    Args:

        config_path (str, optional): A full or relative path to the user_config

        containing (among other things) the user's MapBox token. Defaults to

        "user_config.yml".

    Returns:

        str: The MapBox token

    """

    if not os.path.isabs(config_path):

        config_path = os.path.join(os.path.dirname(__file__), config_path)

    with open(config_path, "r") as stream:

        data = yaml.safe_load(stream)

    return data["mapbox_token"]


def search_google_for_supermarkets(lat, lon, edge_length_meters):

    '''

    Function to search google for supermarkets

    Args:

        lat: latitude

        lon: longitude

        edge_length_meters: edge length in meters

    Returns:

        counter: number of supermarkets

        '''
 
    googlemaps_key = get_googlemaps_key()

    api_key = googlemaps_key
 
    gmaps = googlemaps.Client(key=api_key)
 
    # Define a location (latitude and longitude) and radius (in meters)

    location = (lat, lon)  # San Francisco coordinates as an example

    radius = edge_length_meters # Taking the edge length gives us a circle with that radius from the centre of the hexagon. This would include an additional area around the hexagon.
 
    # Specify the type of places you want to search for (e.g., 'restaurant', 'park', 'museum', etc.)

    place_type = 'supermarket'
 
    # Perform the nearby search

    places = gmaps.places_nearby(

        location=location,

        radius=radius,

        type=place_type

    )
 
    counter = 0

    # Extract and print the places of interest

    for place in places['results']:

        counter += 1
 
    # Check if there are more results and retrieve them using pagetoken

    while 'next_page_token' in places:

        next_page_token = places['next_page_token']

        time.sleep(2)  # Add a delay of 2 seconds to avoid INVALID_REQUEST error
 
        places = gmaps.places_nearby(

            location=location,

            radius=radius,

            type=place_type,

            page_token=next_page_token

        )
 
        # Extract and print the places of interest from the current page of results

        for place in places['results']:

            counter += 1
 
    return counter

# Create the rows that are going to go into the data frame that I'm going to use for each hexagon.
# Create a for loop to run through the first 10 hexagons
import osmnx as ox

if run_buildings_df:
 
      df = pd.DataFrame()
 
      # h3 index 
      h3_index = []
 
      # Road stats 
      residential = []
      service = []
      unclassified = []
      secondary = []
      tertiary = []
      path = []
      trunk = []
      trunk_link = []
 
      # Building Stats
      no_buildings = []
      no_houses = []
      no_commercial = []
      no_industrial = []
      no_hotels = []
      no_apartments = []
      no_retail = []
      no_educational = []
 
      error_list = []
 
      for i in range(0, len(hex_customers_population["geometry"])-1):
 
            # Show the progress every 100 hexagons
            if i % 100 == 0:
                  print("Downloaded Street Map data for", i, " number of hexagons")
 
            hexagon_polygon = hex_customers_population["geometry"][i]
            try: 
                  streets_buildings = ox.features.features_from_polygon(hexagon_polygon, 
                                                                        tags={"highway":['secondary', 'residential', 'tertiary', 'unclassified','service', 'trunk', 'trunk_link', 'path'],
                                                                              "building":True}
                                                                        )
            except: 
                  print("Error with hexagon", i)
                  error_list.append(i)
                  continue
 
            h3_index = [h3_index, hex_customers_population["h3"][i]]
 
            if (streets_buildings.columns == "highway").any():
                  tmp1 = streets_buildings["highway"].value_counts()
                  if (tmp1.keys() == "residential").any():
                        if i == 0:
                              residential = tmp1["residential"]
                        else:
                              residential = 0
                  else:
                        residential = 0
 
                  if (tmp1.keys() == "service").any():
                        service = tmp1["service"]
                  else:
                        service = 0
 
                  if (tmp1.keys() == "unclassified").any():
                        unclassified = tmp1["unclassified"]
                  else:
                        unclassified = 0
 
                  if (tmp1.keys() == "secondary").any():
                        secondary = tmp1["secondary"]
                  else:
                        secondary = 0
 
                  if (tmp1.keys() == "tertiary").any():
                        tertiary = tmp1["tertiary"]
                  else:
                        tertiary = 0
 
                  if (tmp1.keys() == "path").any():
                        path = tmp1["path"]
                  else:
                        path =  0
 
                  if (tmp1.keys() == "trunk").any():
                        trunk = tmp1["trunk"]
                  else:
                        trunk = 0
                  if (tmp1.keys() == "trunk_link").any():
                        trunk_link = tmp1["trunk_link"]
                  else:
                        trunk_link = 0
            else:
                  residential  = 0
                  service      = 0
                  unclassified = 0
                  secondary    = 0
                  tertiary     = 0
                  path         = 0
                  trunk        = 0
                  trunk_link   = 0
 
            # Do the same for the buildings
            if (streets_buildings.columns == "building").any():
                  tmp2 = streets_buildings["building"].value_counts()
                  if (tmp2.keys() == "yes").any():
                        no_buildings = tmp2["yes"]
                  else:
                        no_buildings = 0
 
                  if (tmp2.keys() == "house").any():
                        no_houses = tmp2["house"]
                  else:
                        no_houses = 0
 
                  if (tmp2.keys() == "commercial").any():
                        no_commercial = tmp2["commercial"]
                  else:
                        no_commercial = 0
 
                  if (tmp2.keys() == "industrial").any():
                        no_industrial = tmp2["industrial"]
                  else:
                        no_industrial = 0
 
                  if (tmp2.keys() == "hotel").any():
                        no_hotels = tmp2["hotel"]
                  else: 
                        no_hotels = 0
 
                  if (tmp2.keys() == "apartments").any():
                        no_apartments = tmp2["apartments"]
                  else:
                        no_apartments = 0
 
                  if (tmp2.keys() == "retail").any():
                        no_retail = tmp2["retail"]
                  else:
                        no_retail = 0
 
                  if (tmp2.keys() == "school").any():
                        no_educational = tmp2["school"]
                  else:
                        no_educational = 0
 
            else:
                  no_buildings   = 0
                  no_houses      = 0
                  no_commercial  = 0
                  no_industrial  = 0
                  no_hotels      = 0
                  no_apartments  = 0
                  no_retail      = 0
                  no_educational = 0
 
            
            tmp = pd.DataFrame({"h3": hex_customers_population["h3"][i],
                              "Residential Roads": residential,
                              "Service Roads": service,
                              "Unclassified Roads": unclassified,
                              "Secondary Roads": secondary,
                              "Tertiary Roads": tertiary,
                              "Path Roads": path,
                              "Trunk Roads": trunk,
                              "Trunk Link Roads": trunk_link,
                              "No. Buildings": no_buildings,
                              "No. Houses": no_houses,
                              "No. Commercial": no_commercial,
                              "No. Industrial": no_industrial,
                              "No. Hotels": no_hotels,
                              "No. Apartments": no_apartments,
                              "No. Retail": no_retail,
                              "No. Educational": no_educational,
            }, index=[i])
 
            df = pd.concat([df,tmp])
      df["Total Buildings"] = df["No. Buildings"] + df["No. Houses"] + df["No. Commercial"] + df["No. Industrial"] + df["No. Hotels"] + df["No. Apartments"] + df["No. Retail"] + df["No. Educational"]
      df["Total Roads"] = df["Residential Roads"] + df["Service Roads"] + df["Unclassified Roads"] + df["Secondary Roads"] + df["Tertiary Roads"] + df["Path Roads"] + df["Trunk Roads"] + df["Trunk Link Roads"]
      df.to_csv(os.path.join(output_folder, "buildings_and_roads_kenya_copia.csv"), index=False