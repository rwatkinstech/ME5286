# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
# Note: It is not required to keep a copy of this file, your python script is saved with the station
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
RDK = Robolink()

# Notify user:
print('To edit this program:\nright click on the Python program, then, select "Edit Python script"')

# Program example:
item = RDK.Item('base')
if item.Valid():
    print('Item selected: ' + item.Name())
    print('Item posistion: ' + repr(item.Pose()))

print('Items in the station:')
itemlist = RDK.ItemList()
print(itemlist)

raise Exception('Program not edited.')
