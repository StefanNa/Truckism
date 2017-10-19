import trucksim as ts
import numpy as np
from sys import exit

#ts.set_truck_size(100,100)

# Since we know the dimensions of the boxes , this code simply takes
# the maximum width of any box , and increments the column number every time .
# Notice that a new box is only received once every iteration , and the return
# of the add_box function is used to check if it could be placed .

prev_height = 0 # layer where the last box was placed
full = False # is the truck full yet?
current_column = 0 # current column to place in

TruckX=50
TruckY=40
ts.set_truck_size(TruckX, TruckY)

UpX=0
SideX=2
UpY=0
SideY=0

flag1=0
flag2=0
flag3=0
flag4=0
flag5=0

while not full :
    box = ts. get_next_box () # box = (ID , width , height )
    if box[1] is 1 and flag1 is 0 :
        box1=box
        flag1=1
        print("BOX size",box[1],box[2],"stored on 1")
        box = ts. get_next_box () # box = (ID , width , height )
    if box[1] is 1 and flag2 is 0 :
        box2=box
        flag2=1
        print("BOX size",box[1],box[2],"stored on 2")
        box = ts. get_next_box () # box = (ID , width , height )
    if box[1] is 1 and flag3 is 0 :
        box3=box
        flag3=1
        print("BOX size",box[1],box[2],"stored on 3")
        box = ts. get_next_box () # box = (ID , width , height )
    if box[1] is 3 and flag4 is 0 :
        box4=box
        flag4=1
        print("BOX size",box[1],box[2],"stored on 4")
        box = ts. get_next_box () # box = (ID , width , height )
    if box[1] is 2 and flag5 is 0 :
        box5=box
        flag5=1
        print("BOX size",box[1],box[2],"stored on 5")
        box = ts. get_next_box () # box = (ID , width , height )
    print("BOX",box[0],box[1],box[2])
    # if box is taller than it is wide , lay it flat
    if box [2] is not 3: rotated = True
    else : rotated = False


    if box[1] is 2:
    # if we cant place the box at current height , assume we have reached the top
        if UpY%2 is not 0 and flag4 is 1:
            if not ts. add_box (box4 , UpX , UpY , True ):
                UpX += 2 # increment the column

                UpY = SideY+3 # reset the height
                # if we cant place the box in the next column , assume we filled the truck
                if not ts. add_box (box , UpX , UpY , rotated ):
                    full = True
                else :
                    # if we can , increment the height
                    if rotated : UpY += box [1]
                    else : UpY += box [2]
                    print("UPY",UpY)
                    print("UPX",UpX)
            else :
                # if we can , increment the height
                UpY += 3
                print("UPY",UpY)
                print("UPX",UpX)

        else:
            if not ts. add_box (box , UpX , UpY , rotated ):
                UpX += 2 # increment the column

                UpY = SideY+3 # reset the height
                # if we cant place the box in the next column , assume we filled the truck
                if not ts. add_box (box , UpX , UpY , rotated ):
                    full = True
                else :
                    # if we can , increment the height
                    if rotated : UpY += box [1]
                    else : UpY += box [2]
                    print("UPY",UpY)
                    print("UPX",UpX)
            else :
                # if we can , increment the height
                if rotated : UpY += box [1]
                else : UpY += box [2]
                print("UPY",UpY)
                print("UPX",UpX)

    else:
        if not ts. add_box (box , SideX , SideY , rotated ):
            SideY += 3 # increment the column
            SideX = UpX+2 # reset the height
            # if we cant place the box in the next column , assume we filled the truck
            if not ts. add_box (box , SideX , SideY , rotated ):
                full = True
            else :
                # if we can , increment the height
                if rotated : SideX += box [2]
                else : SideX += box [1]
                print("SideY",SideY)
                print("SideX",SideX)
        else :
            # if we can , increment the height
            if rotated : SideX += box [2]
            else : SideX += box [1]
            print("SideY",SideY)
            print("SideX",SideX)


# print the fill degree of the truck to the terminal
print (" The truck is %g percent full !" % (ts. get_occupied_space_ratio ()*100))

ts. plot_truck ()
