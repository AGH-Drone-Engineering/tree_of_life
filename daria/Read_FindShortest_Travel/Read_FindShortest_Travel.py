import numpy as np

import pobierz_punkty_z_bazy_do_listy
import PuLP
import pid

#download points from database
latitude_longitude_color_list=pobierz_punkty_z_bazy_do_listy.download_points()
# print(latitude_longitude_color_list)

#create lists based on colors
white_points=list(xx for xx in latitude_longitude_color_list if xx[2] == 'white')#[xx for xx in latitude_longitude_color_list]
brown_points=list(xx for xx in latitude_longitude_color_list if xx[2] == 'brown')#[xx for xx in latitude_longitude_color_list]
gold_points=list(xx for xx in latitude_longitude_color_list if xx[2] == 'gold')#[xx for xx in latitude_longitude_color_list]

#print lists
print("white: ", list(white_points))
print("brown: ", list(brown_points))
print("gold:", list(gold_points))

#find shortest path
points_to_shoot:list = [[0.,0.,"white", "false"]]+brown_points+gold_points
print("points to shoot: ",points_to_shoot)
print(PuLP.main(points_to_shoot))

#get path to travel
pid.main(color_points=brown_points+gold_points, white_points=white_points, _start=np.array([0,0,"white", "false"]), distance=0.5)
