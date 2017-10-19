#!/usr/bin/env python

# import of numpy and matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

__author__ = "Mikkel Rath Pedersen"
__copyright__ = "Copyright 2015"
__license__ = "CC Attribution-ShareAlike 4.0 International"
__version__ = "1.0"
__maintainer__ = "Mikkel Rath Pedersen"
__email__ = "mrp@m-tech.aau.dk"

# Global variables
# size of the truck
truck_size = (50,40) 
# boxes (x size,y size,probability)
boxes = {1: (3,2,0.35), 2: (2,2,0.4), 3: (1,3,0.2), 4: (4,3,0.05)}
# colors of the boxes used for plotting 
box_colors = {1: [1,0,0],2: [0,1,0], 3: [0,0,1], 4: [1,0.5,0]} 
# list of placed boxes as tuples (box_id,x,y,rotated)
placed_boxes = [] 


def reset_truck():
    """Resets internal truck model"""
    global free_space 
    global occupied_space
    global support_space 
    global T
    global placed_boxes
    print("Resetting truck")
    placed_boxes = []
    # free space in the  current layer
    free_space = np.ones((truck_size[0],truck_size[1])) 
    # occupied space in the current layer
    occupied_space = np.zeros((truck_size[0],truck_size[1]))
    # space that is supported by the truck or other boxes 
    support_space = np.zeros((truck_size[0],truck_size[1]))
    # supported by the truck 
    support_space[:,0] = np.ones((truck_size[0]))
    # truck matrix only for plotting 
    T = np.ones((truck_size[0],truck_size[1],3)) 

def is_truck_empty():
    """Checks if the truck is currently empty"""
    return (free_space == 1).all()

def set_truck_size(x,y):
    """Sets a new width and height of the truck, and resets"""
    if not is_truck_empty():
        print("The truck is not empty, not resizing!")
        return False
    global truck_size
    truck_size = (x,y)
    print("Truck was resized to %d x %d"%(x,y))
    reset_truck()

def update_truck():
    """Updates internal truck model based on currently placed boxes"""
    global free_space
    global occupied_space
    global support_space
    global T
    for p in placed_boxes:
        # get start and end coordinates of the box in numpy coordinates
        if p[3]: # if rotated
            box_x = [p[1],p[1]+boxes[p[0]][1]] # x coordinate plus height of box
            box_y = [p[2],p[2]+boxes[p[0]][0]] # y coordinate plus width of box
        else: # if not rotated
            box_x = [p[1],p[1]+boxes[p[0]][0]]
            box_y = [p[2],p[2]+boxes[p[0]][1]]
        # update the occupied and free space
        free_space[box_x[0]:box_x[1],box_y[0]:box_y[1]] = 0
        occupied_space[box_x[0]:box_x[1],box_y[0]:box_y[1]] = 1
        # update the support space
        # remove support inside the box
        support_space[box_x[0]:box_x[1],box_y[0]:box_y[1]] = 0
        # update the support on top of box, if it's inside bounds 
        if not box_y[1] == truck_size[1]:
            sup_mask = occupied_space[box_x[0]:box_x[1],box_y[1]]==0
            support_space[box_x[0]:box_x[1],box_y[1]] = sup_mask
        # update the plotting matrix
        T[support_space==1] = [0.85,0.85,0.85]
        # add a colored box
        T[box_x[0]:box_x[1],box_y[0]:box_y[1]] = box_colors[p[0]] 
        
def get_next_box():
    """Gets the next box, based on probabilities"""
    r = np.random.rand(1)[0]
    b = 0
    if r <= boxes[1][2]: b = 1
    elif r <= boxes[1][2] +  boxes[2][2]: b = 2
    elif r <= boxes[1][2] +  boxes[2][2] +  boxes[3][2]: b = 3
    else: b = 4
    return (b, boxes[b][0], boxes[b][1])

def plot_truck(block=True):
    """Plots the current state of the truck"""
    T_rotated = np.rot90(T[::-1],3)
    plt.imshow(T_rotated,interpolation="nearest",origin="lower")
    ax = plt.gca()
    plt.axis([-1,truck_size[0],-1,truck_size[1]])
    ax.xaxis.set_ticks(range(truck_size[0]))
    ax.yaxis.set_ticks(range(truck_size[1]))
    plt.grid(True)
    ax.set_title("Filled %g %%" % (100*get_occupied_space_ratio()))
    ax.add_patch(Rectangle((-.5,-.5), truck_size[0], truck_size[1],fill=False))
    for b in placed_boxes:
        p = b[:]
        if p[3]: # if rotated 
            w = boxes[p[0]][1]
            h = boxes[p[0]][0]
        else:
            w = boxes[p[0]][0]
            h = boxes[p[0]][1]
        ax.add_patch(Rectangle((p[1]-0.5,p[2]-0.5), w, h, fill=False))
    plt.show(block)

def get_supported_in_column(column):
    """Gets supported indices in a given column"""
    try:
        sups = support_space[column,:]
    except IndexError:
        print("ERROR: column index not valid")
        return []
    return list(np.where(sups==1)[0])

def get_supported_in_row(row):
    """Gets supported indices in a given row"""
    try:
        sup = support_space[:,row]
    except IndexError:
        print("ERROR: row index not valid")
        return []
    return list(np.where(sup==1)[0])
    
def get_free_in_column(column):
    """Gets supported indices in a given column"""
    try:
        sup = free_space[column,:]
    except IndexError:
        print("ERROR: column index not valid")
        return []
    return list(np.where(sup==1)[0])

def get_free_in_row(row):
    """Gets supported indices in a given row"""
    try:
        sup = free_space[:,row]
    except IndexError:
        print("ERROR: row index not valid")
        return []
    return list(np.where(sup==1)[0])

def get_free_space_ratio():
    """Gets the percentage of free space"""
    free = np.count_nonzero(free_space)
    total = np.size(free_space)
    return free/float(total)

def get_occupied_space_ratio():
    """Gets the percentage of occupied space"""
    return 1.0-get_free_space_ratio()

def add_box(box_in,box_x,box_y,rotated=False):
    """Adds a box to the truck"""
    #print("Trying to add box: ",(box_in,box_x,box_y,rotated)
    # declare global variables
    global placed_boxes
    if rotated:
        box_size = box_in[1:3][::-1]
    else:
        box_size = box_in[1:3]
    # check if it is fully inside the truck
    is_inside = (box_x+box_size[0]<=truck_size[0] and box_y+box_size[1]<=truck_size[1])
    if not is_inside:
        print("ERROR: The box is not inside the truck!")


        return False
    # check that there is free space
    is_free = free_space[box_x:box_x+box_size[0],box_y:box_y+box_size[1]]==1
    #print(is_free
    if not is_free.all():
        print("ERROR: There is no room for this box here!")
        return False
    #check that it's supported by at least one pixel
    is_supported = support_space[box_x:box_x+box_size[0],box_y:box_y+box_size[1]]==1
    #print is_supported
    if not is_supported.any():
        print("ERROR: This box is not supported by something underneath!")
        return False
    # add to the list of placed boxes
    placed_boxes.append((box_in[0],box_x,box_y,rotated))
    update_truck()
    #print("Added box"
    return True

def usage():
    print("Hello, and welcome to the Truck Loading Simulator!")
    print("This is a module, and is not intended to be run on its own...")
    print("Instead, import it in your python file.")
    print("Bye bye!")
    
if __name__ == "__main__":
    usage()
else:
    reset_truck()
