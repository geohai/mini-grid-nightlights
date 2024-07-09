def plot_isochrones(
    df,
    lat_col="y",
    lon_col="x",
    id_col="id",
    units="meters",
    mean_transport="driving",
    distance=1000,
    show_progress=False,
):
    """
    Plots isochrones for a given dataframe.
 
    Args:
        df (pd.DataFrame): A dataframe containing latitude and longitude values, and some unique identifier.
        lat_col (str, optional): The name of the column containing latitude values. Defaults to "y".
        lon_col (str, optional): The name of the column containing longitude values. Defaults to "x".
        id_col (str, optional): The name of the column containing unique identifiers. Defaults to "id".
        units (str, optional): The units of the isochrones. Defaults to "meters".
        mean_transport (str, optional): The type of transport to use for the isochrones. Defaults to "driving". Options are "driving", "walking", or "cycling".
        distance (int, optional): The distance of the isochrones. Defaults to 1_000.
        show_progress (bool, optional): Whether to show progress while processing. Defaults to False.
 
    Returns:
        gpd.GeoDataFrame: geopandas dataframe containing the isochrones
    """
    isochrones = []
    counter = 0
    mapbox_key = get_mapbox_token()
 
    for _, row in df.iterrows():
        counter += 1
        if show_progress and counter % 50 == 0:
            print(f"Finished {counter} out of {len(df)} locations.")
 
        lat = row[lat_col]
        lon = row[lon_col]
        coordinates = f"{lon},{lat}"
        url = f"https://api.mapbox.com/isochrone/v1/mapbox/{mean_transport}/{
            coordinates}?contours_{units}={distance}&polygons=true&access_token={mapbox_key}"
 
        try:
            response = requests.get(url)
            response.raise_for_status()
            response = response.json()    
            response["features"][0][id_col] = row[id_col]
            isochrones.append(response)
        except requests.exceptions.RequestException as e:
            print(
                f"Error occurred while retrieving isochrone data for {
                    row[id_col]}: {e}"
            )
 
    # Getting the geometry values from the isochrones and adding them to the df
    isochrones = [
        Polygon(feature["geometry"]["coordinates"][0][::-1])
        for isochrone in isochrones
        for feature in isochrone["features"]
    ]
 
    df["geometry"] = isochrones
 
    df = gpd.GeoDataFrame(df, geometry="geometry")
 
    return df

import yaml
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