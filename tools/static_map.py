# Modification to the original staticmaps API, which can be found at
# https://github.com/komoot/staticmap/blob/master/staticmap/staticmap.py

from staticmap import StaticMap
from PIL import Image
from math import sqrt, log, tan, pi, cos, ceil, floor, atan, sinh

def _lon_to_x(lon, zoom):
    """
    transform longitude to tile number
    :type lon: float
    :type zoom: int
    :rtype: float
    """
    if not (-180 <= lon <= 180):
        lon = (lon + 180) % 360 - 180

    return ((lon + 180.) / 360) * pow(2, zoom)


def _lat_to_y(lat, zoom):
    """
    transform latitude to tile number
    :type lat: float
    :type zoom: int
    :rtype: float
    """
    if not (-90 <= lat <= 90):
        lat = (lat + 90) % 180 - 90

    return (1 - log(tan(lat * pi / 180) + 1 / cos(lat * pi / 180)) / pi) / 2 * pow(2, zoom)

def render_without_features(self, zoom=None, center=None):
    """
    render static map with all map features that were added to map before
    :param zoom: optional zoom level, will be optimized automatically if not given.
    :type zoom: int
    :param center: optional center of map, will be set automatically from markers if not given.
    :type center: list
    :return: PIL image instance
    :rtype: Image.Image
    """

    if not self.lines and not self.markers and not self.polygons and not (center and zoom):
        raise RuntimeError("cannot render empty map, add lines / markers / polygons first")

    if zoom is None:
        self.zoom = self._calculate_zoom()
    else:
        self.zoom = zoom

    if center:
        self.x_center = _lon_to_x(center[0], self.zoom)
        self.y_center = _lat_to_y(center[1], self.zoom)
    else:
        # get extent of all lines
        extent = self.determine_extent(zoom=self.zoom)

        # calculate center point of map
        lon_center, lat_center = (extent[0] + extent[2]) / 2, (extent[1] + extent[3]) / 2
        self.x_center = _lon_to_x(lon_center, self.zoom)
        self.y_center = _lat_to_y(lat_center, self.zoom)

    image = Image.new('RGB', (self.width, self.height), self.background_color)

    self._draw_base_layer(image)
    # This is what draws the features in the original class
    # self._draw_features(image)

    return image

# Register the new method in the orignal class
# StaticMap.__dict__["render"] = render_without_features
# setattr(StaticMap, "render", "render_without_features")
StaticMap.render = render_without_features