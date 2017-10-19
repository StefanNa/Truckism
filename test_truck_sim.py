import trucksim as ts
import numpy as np
from sys import exit
# Since we know the dimensions of the boxes , this code simply takes
# the maximum width of any box , and increments the column number every time .

# Notice that a new box is only received once every iteration , and the return
# of the add_box function is used to check if it could be placed .

prev_height = 0 # layer where the last box was placed
full = False # is the truck full yet?
current_column = 0 # current column to place in
YSide=0
XSide=2
YUp=0
XUp=0
TruckY =40
TruckX=50
row=4
col=3


box = ts. get_next_box () # box = (ID , width , height )
if box[1] is 2:
     ts. add_box (box , XUp , YUp , False )
else:
    if box [2] is not 3:
        ts. add_box (box , XSide , YSide , True )
    else:
        ts. add_box (box , XSide , YSide , False )

while not full :
    box = ts. get_next_box () # box = (ID , width , height )
    # if box is taller than it is wide , lay it flat



    if box [2] is not 3 and box [1] is not 2: rotated = True
    else : rotated = False


    if box [1] is 2 and YUp<=(TruckY-2):

        ts. add_box (box , XUp , YUp , rotated )
        YUp += box[1]
    elif box [1] is 2 and YUp>(TruckY-2):
        XUp += 2
        YUp = col
        ts. add_box (box , XUp , YUp , rotated )
        YUp += box[1]
        col +=3
    print("XUp",XUp)
    print("Yup",YUp)

    if box [1] is not 2 and XSide<=(TruckX-4):

        ts. add_box (box , XSide , YSide , rotated )
        if rotated is True:
            XSide += box[2]
        else:
            XSide += box[1]
    elif box [1] is not 2 and XSide>(TruckX-4):
        YSide += 3
        #if XUp >= row:
        print("row:",row)
        XSide = row
        print("XSide1",XSide)
        row +=2
        ts. add_box (box , XUp , YUp , rotated )
        print("XSide2",XSide)
        if rotated is True:
            XSide += box[2]
        else:
            XSide += box[1]
    print("XSide",XSide)
    print("YSide",YSide)

    if XSide > 0.9*TruckX and YSide > 0.9*TruckY:
        full = True

    # if we cant place the box at current height , assume we have reached the top
#    if not ts. add_box (box , current_column , prev_height , rotated ):
#        current_column += 4 # increment the column
#        prev_height = 0 # reset the height
#        # if we cant place the box in the next column , assume we filled the truck
#        if not ts. add_box (box , current_column , prev_height , rotated ):
#            full = True
#        else :
#        # if we can , increment the height
#            if rotated : prev_height += box [1]
#            else : prev_height += box [2]
#    else :
## if we can , increment the height
#        if rotated : prev_height += box [1]
#        else : prev_height += box [2]

# print the fill degree of the truck to the terminal
print (" The truck is %g percent full !" % (ts. get_occupied_space_ratio ()*100))

ts. plot_truck ()
