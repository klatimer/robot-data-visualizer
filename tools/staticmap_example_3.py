# Using modified version of staticmap

from staticmap import Line
import tools.static_map # This overrides a few class functions

m = tools.static_map.StaticMap(600, 600, 80)

southwest = [-83.721154, 42.287215]
northeast = [-83.710182, 42.293970]

coordinates = [southwest, northeast]
line_outline = Line(coordinates, 'white', 6)
line = Line(coordinates, '#D2322D', 4)

m.add_line(line_outline)
m.add_line(line)

image = m.render()
image.save('umich.png') # No lines drawn
