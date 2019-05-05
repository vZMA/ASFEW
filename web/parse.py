from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    nav = 0
    intersection = 0
    def handle_data(self, data):
        if data[:7] == ';Navaid':
            self.nav += 1
            if self.nav == 1:
                f = open("data/vor.dat", "w")
                f.write(data)
                f.close()
            else:
                f = open("data/ndb.dat", "w")
                f.write(data)
                f.close()
        if data[:13] == ';Intersection':
            self.intersection += 1
            if self.intersection == 1:
                f = open("data/int.dat", "w")
                f.write(data)
                f.close()
            else:
                f = open("data/apt.dat", "w")
                f.write(data)
                f.close()
        if data[:5] == '[HIGH':
            f = open("data/high.dat", "w")
            f.write(data)
            f.close()
        if data[:4] == '[LOW':
            f = open("data/low.dat", "w")
            f.write(data)
            f.close()
    
parser = MyHTMLParser()
parser.feed(open("data/myfsim.dat").read())
