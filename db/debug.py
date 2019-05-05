import sqlite3

def main():
    cn = sqlite3.connect('sector.db')
    c = cn.cursor()

    # Load tables with data required from user
    c.execute("""SELECT * FROM high""")
    
    print c.fetchall()

    cn.close()

if __name__=="__main__":
    main()
