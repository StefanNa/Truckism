import trucksim as ts
import numpy as np
from sys import exit

#ts.set_truck_size(100,100)

# Since we know the dimensions of the boxes , this code simply takes
# the maximum width of any box , and increments the column number every time .
# Notice that a new box is only received once every iteration , and the return
# of the add_box function is used to check if it could be placed .

full = False # is the truck full yet? CORRESPONDS TO THE FIRST FILLING WHILE LOOP

#DEFINE TRUCK SIZE (works for even numbers)
TruckX=50
TruckY=40
ts.set_truck_size(TruckX, TruckY)

#Postion of filling up Blocks vertically
UpX=0
UpY=0
#Postion of filling up Blocks horizontally
#starts at 2 to leave space for one horizontal column
SideX=2
SideY=0

#Flag to know if generated box is used or replaced by one from stock
flag0=0

#Flags for stock of 5 blocks
flag1=0
flag2=0
flag3=0
flag4=0
flag5=0

#while loop to fill up truck as follows
#idea is to fill up vertically with 2x2 blocks
#while filling up horizontally with blocks turned to have hight of 3
while not full :
    #checks if one block has been exchanged for another to reuse it instantly
    if flag0 is 1:
        box=box5
        flag0=0
    else:
        #generates a new box
        box = ts. get_next_box () # box = (ID , width , height )

    #stores boxes of size 3x1 in spot 1 to 3 to fill rows
    #stores boxes of size 3x2 in spot 4 to compensate for uneven high columns
    #stores any replaced box in spot 5 to be instantly reused next round
    #makes sure we always have needed blocks in stock
    if box[1] is 1 and flag1 is 0 :
        box1=box
        flag1=1
        print("BOX size",box[1],box[2],"stored on 1")
        box = ts. get_next_box () # box = (ID , width , height )
    elif box[1] is 1 and flag2 is 0 :
        box2=box
        flag2=1
        print("BOX size",box[1],box[2],"stored on 2")
        box = ts. get_next_box () # box = (ID , width , height )
    elif box[1] is 1 and flag3 is 0 :
        box3=box
        flag3=1
        print("BOX size",box[1],box[2],"stored on 3")
        box = ts. get_next_box () # box = (ID , width , height )
    elif box[1] is 3 and flag4 is 0 :
        box4=box
        flag4=1
        print("BOX size",box[1],box[2],"stored on 4")
        box = ts. get_next_box () # box = (ID , width , height )

    print("BOX",box[0],box[1],box[2])
    # if box is not 3 high, turn it (does it for 2x2 aswell but that does not matter)
    if box [2] is not 3: rotated = True
    else : rotated = False

    #if box height is 2
    if box[1] is 2:
    # if the height of the column is uneven we can not fill up all the way to we add a 3x2 if possible
        if UpY%2 is not 0 and flag4 is 1: #modulo is ued for that
            #tries to place the 3x2 box and ensures we continue if not possible
            if not ts. add_box (box4 , UpX , UpY , True ):
                UpX += 2 # increment the column

                UpY = SideY+3 # set height of new column to be 3 higher than where the row is placed
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
                # if we can , we increment the height
                UpY += 3
                print("COL Insertation triggered:")
                print("UPY",UpY)
                print("UPX",UpX)
                box5=box
                flag0=1

        else:
            #if the position is even, we stak up until we reach the top and move to the next column then
            if not ts. add_box (box , UpX , UpY , rotated ):
                UpX += 2 # increment the column

                UpY = SideY+3 # reset the height in next column
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

    else: #Box is not 2x2
        #CHECKS HOW CLOSE TO THE TRUCKS EDGE WE ARE
        #IF WE ARE 3 BLOCKS CLOSE TO THE EDGE WE FILL UP WITH 3x1 Blocks
        if SideX >= TruckX-3 and SideX is not TruckX and flag1 is 1:
            #filling continues until we reach the edge or are out of blocks (unlikely but possible)
            while SideX is not TruckX:
                #if stock 1 is available use it
                if flag1 is 1:
                    if not ts. add_box (box1 , SideX , SideY , False ):
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
                            break
                    else :
                        # if we can , increment the height
                        SideX += 1
                        print("ROW Insertation1 triggered:")
                        print("SideY",SideY)
                        print("SideX",SideX)
                        flag1=0
                        box5=box
                        flag0=1

                #if stock 2 is available use it
                elif flag2 is 1:
                    if not ts. add_box (box2 , SideX , SideY , False ):
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
                            break
                    else :
                        # if we can , increment the height
                        SideX += 1
                        print("ROW Insertation2 triggered:")
                        print("SideY",SideY)
                        print("SideX",SideX)
                        flag2=0
                        box5=box
                        flag0=1

                #if stock 3 is available use it
                elif flag3 is 1:
                    if not ts. add_box (box3 , SideX , SideY , False ):
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
                            break
                    else :
                        # if we can , increment the height
                        SideX += 1
                        print("ROW Insertation3 triggered:")
                        print("SideY",SideY)
                        print("SideX",SideX)
                        flag3=0
                        box5=box
                        flag0=1
                elif flag1 is 0 and flag2 is 0 and flag3 is 0:
                    box5=box
                    if not ts. add_box (box5 , SideX , SideY , rotated ):
                        SideY += 3 # increment the column
                        SideX = UpX+2 # reset the height
                        # if we cant place the box in the next column , assume we filled the truck
                        if not ts. add_box (box5 , SideX , SideY , rotated ):
                            full = True
                        else :
                            # if we can , increment the height
                            if rotated : SideX += box [2]
                            else : SideX += box [1]
                            flag0=0
                            print("NO BOX IN 1 2 3")
                            print("SideY",SideY)
                            print("SideX",SideX)
                            break
                    else :
                        # if we can , increment the height
                        if rotated : SideX += box [2]
                        else : SideX += box [1]
                        print("SideY",SideY)
                        print("SideX",SideX)
                        break



        #blocks are not close to the side of the truck so we keep on stacking
        else:
            #attempts to put box in row and in case we fill perfectly moves on
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





ts.get_free_in_row(SideY)


print("SideY",SideY)
print("SideX",SideX)
print("UpY",UpY)
print("UpX",UpX)

# print the fill degree of the truck to the terminal
print (" The truck is %g percent full !" % (ts. get_occupied_space_ratio ()*100))

ts. plot_truck ()
