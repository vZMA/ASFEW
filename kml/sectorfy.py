import pykml.parser
import sqlite3

COLORS = {
    "@Runway": "Runway",
    "@Taxiway": "Taxiway",
    "@Building": "Building",
    "@TLabel": "TXWM",
    "@OLabel": "TXWM",
    "@RLabel": "RWM"
}


def decdeg2dms(dd):
    mnt, sec = divmod(dd * 3600, 60)
    deg, mnt = divmod(mnt, 60)
    return deg, mnt, sec


def sct_coord(coord):
    if coord == (0, 0):
        return ZERO_COORD
    else:
        lat = decdeg2dms(abs(float(coord[1])))
        lon = decdeg2dms(abs(float(coord[0])))
        lats = "N%03i.%02i.%06.3f" % lat
        lons = "W%03i.%02i.%06.3f" % lon
        return lats.ljust(14) + ' ' + lons.ljust(14)


class Path(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.points = []
        self.coordlist = []

    # def emit(self, handle):
    #     for i in range(len(self.points) - 1):
    #         a = sct_coord(self.points[i])
    #         b = sct_coord(self.points[i + 1])
    #         handle.write("%s %s %s\n" % (a.ljust(30), b.ljust(30), self.color))

    def coords(self):
        for i in range(len(self.points) - 1):
            a, b = sct_coord(self.points[i]).split(" ")
            c, d = sct_coord(self.points[i + 1]).split(" ")
            self.coordlist.append((a, b, c, d))


class Text(object):
    def __init__(self, name, category, pos, color):
        self.name = name
        self.color = color
        self.category = category
        self.pos = pos

    def coords(self):
        lat, lon = sct_coord(self.pos).split(" ")
        return lat.ljust(14), lon.ljust(14)


class Converter(object):
    def __init__(self, kml, feature, name):
        self.kml = kml
        self.name = name
        self.feature = feature
        self.paths = []
        self.regions = []
        self.texts = []

    def parse_coords(self, data):
        points = []
        try:
            coords = data.coordinates.text.strip()
            coords = coords.split(" ")
            for coord in coords:
                lat, lon, alt = coord.split(",")
                points.append((lat, lon))
        except ValueError:
            pass
        finally:
            return points

    def path(self, name, data):
        color, name = name.split("_")
        obj = Path(name, COLORS[color])
        obj.points = self.parse_coords(data)
        self.paths.append(obj)

    def point(self, name, category, data):
        lon, lat, alt = str(data.coordinates).split(",")
        color, name = name.split("_")
        obj = Text(name, category, (lon, lat), COLORS[color])
        self.texts.append(obj)

    def dispatch(self, item, name):
        if item.tag.endswith("Folder"):
            for child in item.iterchildren():
                self.dispatch(child, str(item.name))

        elif item.tag.endswith("Placemark"):
            for child in item.iterchildren():
                if child.tag.endswith("LineString"):
                    self.path(str(item.name), child)
                elif child.tag.endswith("Point"):
                    self.point(str(item.name), name, child)

    def convert(self):
        cn = sqlite3.connect('../db/sector.db')
        c = cn.cursor()

        if self.feature == "@ASDE":
            c.execute("DELETE FROM sid WHERE name='%s' AND type='%s'" % (self.name, 'ASDE'))
            c.execute("DELETE FROM labels WHERE grouptitle='%s' and type='%s'" % (self.name, 'ASDE'))
        if self.feature == "@BoundHi":
            pass
        if self.feature == "@BoundLo":
            pass
        if self.feature == "@Bound":
            pass
        if self.feature == "@Geo":
            pass

        cn.commit()
        cn.close()
        for child in self.kml.Document.iterchildren():
            self.dispatch(child, "root")
        self.emit()

    def emit(self):
        cn = sqlite3.connect('../db/sector.db')
        c = cn.cursor()

        if self.feature == "@ASDE":
            for path in self.paths:
                path.coords()
                loop = 0
                for coord in path.coordlist:
                    loop += 1
                    c.execute("INSERT INTO sid VALUES ('%s',%i,'%s','%s','%s','%s','%s','%s','%s')" % (self.name, loop, coord[0], coord[1], coord[2], coord[3], path.color, path.name, 'ASDE'))
            for text in self.texts:
                lat, lon = text.coords()
                c.execute("INSERT INTO labels VALUES ('%s','%s','%s','%s','%s','','%s')" % (self.name, text.name, lat, lon, text.color, "ASDE"))
        if self.feature == "@BoundHi":
            pass
        if self.feature == "@BoundLo":
            pass
        if self.feature == "@Bound":
            pass
        if self.feature == "@Geo":
            pass

        # name
        # sequence
        # lat1
        # lon1
        # lat2
        # lon2
        # color
        # comment
        # type



        cn.commit()
        cn.close()

def main(args):
    if len(args) < 2:
        print "no input file specified"
        return 1

    kml_file = args[1]
    with open(kml_file) as inf:
        kml = pykml.parser.parse(inf).getroot()
        name = str(kml.Document.name)
        base, extension = name.split(".")
        feature, group = base.split("_")
        conv = Converter(kml, feature, group)
        conv.convert()


if __name__ == "__main__":
    import sys

    main(sys.argv)
