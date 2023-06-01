import numpy as np

import pobierz_punkty_z_bazy_do_listy
import PuLP
import pid

def optimalize_points(start_point):
    #download points from database
    # print("here")
    latitude_longitude_color_list=pobierz_punkty_z_bazy_do_listy.download_points()
    # print("here")
    # print(latitude_longitude_color_list)

    #create lists based on colors
    white_points=list(xx for xx in latitude_longitude_color_list if xx[2] == 'white')#[xx for xx in latitude_longitude_color_list]
    brown_points=list(xx for xx in latitude_longitude_color_list if xx[2] == 'brown')#[xx for xx in latitude_longitude_color_list]
    gold_points=list(xx for xx in latitude_longitude_color_list if xx[2] == 'gold')#[xx for xx in latitude_longitude_color_list]

    #print lists
    # print("white: ", list(white_points))
    # print("brown: ", list(brown_points))
    # print("gold:", list(gold_points))

    #find shortest path
    points_to_shoot:list = [(start_point)]+brown_points+gold_points
    # print("points to shoot: ",points_to_shoot)
    points_to_shoot=PuLP.main(points_to_shoot)
    # print(points_to_shoot)

    #get path to travel
    # print(points_to_shoot.index(start_point))
    from collections import deque
    items=deque(points_to_shoot)
    items.rotate(-1* points_to_shoot.index(start_point))
    # print(list(items))
    # exit()
    return pid.main(color_points=list(items)[1:], white_points=white_points, _start=np.array(start_point), distance=0.00005, print_route=False)

    
if __name__=="__main__":

    print(optimalize_points(start_point=[50.06296, 19.91573,"white", "false"]))
