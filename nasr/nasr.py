import os

work_dir = "Not Set"
ref_point = "Not Set"
radius = "Not Set"


def menu():
    os.system("cls")
    print ""
    print ""
    print "***********************************************************************************"
    print "***  Automated Sector-File Enhanced Workflow (ASFEW) NASR Processing Menu       ***"
    print "***********************************************************************************"
    print ""
    print ""
    print "---   Current Settings---"
    print "Working Directory:      " + work_dir
    print "Reference Point:        " + ref_point
    print "Radius:                 " + radius
    print ""
    print "---       Menu        ---"
    print "[1] Set & Initialize Working Directory"
    print "[2] Set Reference Point"
    print "[3] Set Radius"
    print("[4] Download NASR from FAA")
    print("[5] Process Airway Data")
    print ""
    print ""


def write_settings():
    global work_dir
    global ref_point
    global radius
    with open("./settings.dat", "w") as settings:
        settings.write(work_dir + "\n")
        settings.write(ref_point + "\n")
        settings.write(radius + "\n")


def read_settings():
    with open("./settings.dat") as settings:
        global work_dir
        global ref_point
        global radius
        work_dir = settings.readline().strip()
        ref_point = settings.readline().strip()
        radius = settings.readline().strip()


def initialize():
    global work_dir
    if work_dir.strip().length() > 0:
        if os.path.exists(work_dir):
            if not os.path.exists(work_dir + "data\\"):
                os.mkdir(work_dir + "data\\")
            if not os.path.exists(work_dir + "output\\"):
                os.mkdir(work_dir + "output\\")


read_settings()
initialize()
menu()
option = int(input("Choose: "))

while option != 0:
    if option == 1:
        work_dir = raw_input("Enter path to working directory: ")
    elif option == 2:
        ref_point = raw_input("Enter fix or navaid for reference point: ")
    elif option == 3:
        radius = raw_input("Enter radius (integer): ")
    elif option == 4:
        pass
    elif option == 5:
        pass
    else:
        print ("invalid option")

    write_settings()
    read_settings()
    print
    menu()
    option = int(input("Choose: "))

