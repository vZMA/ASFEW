import re
from math import *

# process NASR legacy data to produce sector file formatted data
# concatenate ATS.txt and AWY.txt, then put combined.txt into the /input folder
# this can be improved by automating the above step
# output will be written to /output/hi.dat and /output/lo.dat
# one intermediate file is created for convenience

def within(lastFixLat, lastFixLon, thisFixLat, thisFixLon):
    if haversine(lastFixLat, lastFixLon) and haversine(thisFixLat, thisFixLon):
        return True

def haversine(lat, lon):
    dir1 = lat[-1:]
    dir2 = lon[-1:]
    (dd1, mm1, ss1) = re.split("-", lat[:-1])
    (dd2, mm2, ss2) = re.split("-", lon[:-1])

    latdec = dms2dec(dd1, mm1, ss1, dir1)
    londec = dms2dec(dd2, mm2, ss2, dir2)
    latref = 26.7827425
    lonref = -80.6914325

    latdec, londec, latref, lonref = map(radians, [latdec, londec, latref, lonref])

    dlon = lonref - londec
    dlat = latref - latdec
    a = sin(dlat/2)**2 + cos(latdec) * cos(latref) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    if 3956 * c < 1000:
        return True
    else:
        return False

def dms2dec(dd, mm, ss, dir):
    if dir == "N" or dir == "E":
        sign = 1
    else:
        sign = -1

    return sign * (int(dd) + float(mm) / 60 + float(ss) / 3600)

nasr = "input/combined.txt"
intermediate = "output/AWY.int"
hi = "output/hi.dat"
lo = "output/lo.dat"

out = open(intermediate, "w")

with open(nasr) as fp:
    line = fp.readline()
    while line:
        if line[0:4] == "AWY2" or line[0:4] == "ATS2":
            out.write(line)
        line = fp.readline()

fp.close()
out.close()

lastFix = ""
thisFix = ""
airway = ""
lastAirway = ""
thisCoordLat = ""
thisCoordLon = ""
lastCoordLat = ""
lastCoordLon = ""

outHi = open(hi, "w")
outLo = open(lo, "w")

with open(intermediate) as fp:
    line = fp.readline()
    while line:
        if line[0:4] == "ATS2":
            airway = line[6:18].strip()
            fixType = line[65:90].strip()
            aidName = line[142:146].strip()
            fixName = line[25:30].strip()
            thisCoordLat = line[109:123].strip()
            thisCoordLon = line[123:137].strip()
        else:
            airway = line[4:9].strip()
            fixType = line[45:59].strip()
            aidName = line[116:120].strip()
            fixName = line[15:20].strip()
            thisCoordLat = line[83:97].strip()
            thisCoordLon = line[97:111].strip()

        if fixType == "VORTAC":
            thisFix = aidName
        elif fixType == "VOR/DME":
            thisFix = aidName
        elif fixType == "VOR":
            thisFix = aidName
        elif fixType == "NDB":
            thisFix = aidName
        elif fixType == "NDB/DME":
            thisFix = aidName
        elif fixType == "REP-PT":
            thisFix = fixName
        elif fixType == "WAY-PT":
            thisFix = fixName
        else:
            line = fp.readline()
            continue

        if airway == lastAirway:
            #this continues a previous airway
            if within(lastCoordLat, lastCoordLon, thisCoordLat, thisCoordLon):
                if airway[0:1] == "J" or airway[0:1] == "Q" or airway[0:1] == "B" or airway[0:1] == "A" or airway[0:1] == "M" or airway[0:1] == "G" or airway[0:1] == "Y" or airway[0:1] == "L" or airway[0:1] == "R":
                    outHi.write(airway + "\t" + lastFix + "\t" + lastFix + "\t" + thisFix + "\t" + thisFix + "\n")
                else:
                    outLo.write(airway + "\t" + lastFix + "\t" + lastFix + "\t" + thisFix + "\t" + thisFix + "\n")
            lastFix = thisFix
            lastCoordLat = thisCoordLat
            lastCoordLon = thisCoordLon
        else:
            #this is a new airway definition
            lastAirway = airway
            lastFix = thisFix
            lastCoordLat = thisCoordLat
            lastCoordLon = thisCoordLon

        line = fp.readline()

outHi.close()
outLo.close()
fp.close()
