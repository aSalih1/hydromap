"""Main module."""
import string
import random
import ipyleaflet


class Map(ipyleaflet.Map):

    def __init__(self, center=[20, 0], zoom=2, **kwargs) -> None:

        if "scroll_weel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(center=center, zoom=zoom, **kwargs)

        
        if "layers_control" not in kwargs:
            kwargs["layers_control"] = True

        if "layers_draw_control" not in kwargs:
            kwargs["layers_draw_control"] = True

        if kwargs["layers_draw_control"]:
            self.add_draw_control()

       
        if kwargs["layers_control"]:
            self.add_layers_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True
        
        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()


    def add_search_control(self, position="topleft", **kwargs):
        """Adds a search control to the map.

        Args:
            Kwargs: keyword arguments to pass to the search control.
        """  
        if "url" not in kwargs:
            kwargs["url"] = 'https://nominatim.openstreetmap.org/search?format=json&q={s}'


            search_control = ipyleaflet.SearchControl(position=position, **kwargs)
            self.add_control(search_control)

    def add_draw_control(self, **kwargs):
        """Adds a draw control to the map.

        Args:
            kwargs: keyword arguments to pass to the draw control.
        """  
        draw_control = ipyleaflet.DrawControl(**kwargs)
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 1.0
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 1.0
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 1.0
            }
        }
        self.add_control(draw_control)
            
    def add_layers_control(self, position="topright", **kwargs):

        """Adds layers control to the map.
        Args:
                kwargs: keyword arguments to pass to the layers control.
        """
        
        layers_control = ipyleaflet.LayersControl(position=position, **kwargs)
        self.add_control(layers_control)

    def add_fullscreen_control(self, position="topleft"):
        """Adds a fullscreen control to the map.

        Args:
            kwargs: keyword arguments to pass to the fullscreen control

        """
        
        fullscreen_control = ipyleaflet.FullScreenControl(position=position)
        self.add_control(fullscreen_control)


    def add_tile_later(self, url, name, attribution="", **kwargs):
        """Adds a tile layer to the map.

        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """    
        tile_layer = ipyleaflet.TileLayer(
            url=url,
            name=name,
            attribution=attribution, **kwargs
        )
        self.add_layer(tile_layer)


    def add_basemap(self, basemap, **kwargs):

        import xyzservices.providers as xyz

        if basemap.lower() == "roadmap":
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_later(url, name=basemap, **kwargs)
        elif basemap.lower() == "hybrid":
            url = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_later(url, name=basemap, **kwargs)
        else:
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_later(url, name=basemap.name, attribution=attribution, **kwargs)
            except:
                raise ValueError(f"Basemap '{basemap}' not found.")

    def add_geojson(self, data, name='GeoJSON', **Kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (dict): The GeoJSON data.
        """  

        if isinstance(data, str):
            import json
            with open(data, "r") as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data=data, name=name, **Kwargs)
        self.add_layer(geojson)

    def add_shp(self, data, name='Shapefile', **Kwargs):
        """Adds a shapefile layer to the map.

        Args:
            data (str): The path to the shapefile.
        """  
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **Kwargs)  
        

def generate_random_string(length=9, upper=False, digits=False, punctuation=False):
    """Generates a random string of a given length.

    Args: 
        length (int, optional): The length of the string to generate. Default to 10.
        upper (bool, optional): Whether to include uppercase letters. Defaults to False.
        digits (bool, optional): Wether to include digits. Defaults to False.
        punctuation (bool, optional): Wether to include punctuation. Defaults to False.

    Returns:
        str: The generated string.
    """  

    letters = string.ascii_lowercase
    if upper:
        letters += string.ascii_uppercase
    if digits:
        letters += string.digits
    if punctuation:
        letters += string.punctuation
        
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def generate_lucky_number(length=1):
    """Generate a lucky number with a specified number length.

    Args:
        length (int, optional):The length of number to generate. Defaults to 1.

    Returns:
        int: The generated number.
    """  

    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return int(result_str)