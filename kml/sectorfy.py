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
    mnt,sec = divmod(dd*3600,60)
    deg,mnt = divmod(mnt,60)
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

    def emit(self, handle):
        for i in range(len(self.points)-1):
            a = sct_coord(self.points[i])
            b = sct_coord(self.points[i+1])
            handle.write("%s %s %s\n" % (a.ljust(30), b.ljust(30), self.color))

class Text(object):
    def __init__(self, name, category, pos, color):
        self.name = name
        self.color = color
        self.category = category
        self.pos = pos

    def emit(self, handle):
        lat, lon = sct_coord(self.pos).split(" ")
        self.name = '"' + self.name + '"'
        handle.write("%s %s %s %s\n" % (self.name.ljust(40), lat.ljust(14), lon.ljust(14), self.color))

class Converter(object):
    def __init__(self, kml, feature, groupname):
        self.kml = kml
        self.name = groupname
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
        for child in self.kml.Document.iterchildren():
            self.dispatch(child, "root")

    def cleandb():
        cn = sqlite3.connect('../db/sector.db')
        c = cn.cursor()
        if self.feature == "@ASDE":
            c.execute("DELETE FROM sid WHERE name='%s'" % self.groupname)
            c.execute("DELETE FROM labels WHERE grouptitle='%s' and type='%s'" % self.groupname, "ASDE")
        cn.commit()
        cn.close()        

    def emit(self, handle):
        handle.write("[GEO]\n")
        for path in self.paths:
            path.emit(handle)

        handle.write("[LABELS]\n")
        for text in self.texts:
            text.emit(handle)

def main(args):
    if len(args) < 2:
        print "no input file specified"
        return 1

    out_file = "out.sct"
    kml_file = args[1]
    with open(kml_file) as inf, open(out_file, "w") as outf:
        kml = pykml.parser.parse(inf).getroot()
        name = str(kml.Document.name)
        base, extension = name.split(".")
        feature, groupname = name.split("_")
        conv = Converter(kml, feature, groupname)
        conv.cleandb
        conv.convert()
        conv.emit(outf)



        

if __name__ == "__main__":
    import sys
    main(sys.argv)
