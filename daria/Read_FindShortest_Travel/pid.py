import matplotlib.pyplot as plt
import numpy as np
import math

# start = np.array([0., 0.])
# point = np.array([7., 3.])
# distance=0.5

# points_list=[]
# points_list.append(start)
# points_list.append(point)
# points_list.append((1.,5.))
# points_list.append((2.5, 4))
# end = (10., 10.)
# points_list.append(end)  # list of trees coords

def distance_between_points(p1,p2):
    # _p1=np.array([float(p1[0]),float(p1[1])])
    # _p2=np.array([float(p2[0]),float(p2[1])])
    return np.linalg.norm(p1-p2)

def distance_between_vector_and_point(v_start,v_end, point):
    
    return np.linalg.norm(np.cross(v_end-v_start, v_start-point))/np.linalg.norm(v_end-v_start)

def get_angle_between_vectors(vector_1,vector_2):
    return math.atan2(vector_1[1],vector_1[0])-math.atan2(vector_2[1],vector_2[0])

def get_versor(p1,p2, dx):
    return (p2-p1)/distance_between_points(p1,p2)*dx

def check_if_is_close_to_any_point_in_list(point,all_points_list_, distance_, exclude):
    for p in all_points_list_:
        if distance_between_points(point,exclude)<distance_:
            continue
        if distance_between_points(p,point)<distance_:
            # print("Close to point:", p)
            return p
    return None

#get path
def main(color_points, white_points, _start=[0.,0.,"white", "false"], distance=0.5):
    start=np.array([float(_start[0]),float(_start[1])])
    all_points_list=np.copy(color_points+white_points)
    all_points_list = np.unique(all_points_list, axis=0)  # remove duplicate points
    _color_points=np.copy(color_points).tolist()
    _color_points.append(start)
    _color_points.append(start)

    
    x_color = [float(xx[0]) for xx in color_points]
    y_color = [float(yy[1]) for yy in color_points]
    x_all = [float(xx[0]) for xx in all_points_list]
    y_all = [float(yy[1]) for yy in all_points_list]

    # plt.scatter(x_all, y_all, marker='o', c='yellow') 
    
    # color_now='brown'
    # plt.scatter([float(xx[0]) for xx in color_points if xx[2]==color_now], [float(yy[1]) for yy in color_points if yy[2]==color_now], marker='o', c=color_now) 
    
    # color_now='gold'
    # plt.scatter([float(xx[0]) for xx in color_points if xx[2]==color_now], [float(yy[1]) for yy in color_points if yy[2]==color_now], marker='o', c=color_now) 

    
    BBox = (min(x_all), max(x_all), min(y_all), max(y_all))
    # plt.scatter(x_color, y_color, marker='o', c='g') 
     

    #move step by step
    path_points=[]
    tmp_all_points_list=[np.array([float(xx[0]),float(xx[1])]) for xx in all_points_list]
    # len_tmp_all_points_list=len(tmp_all_points_list)
    
    step_point=np.copy(start)
    next_=np.array([float(color_points[0][0]),float(color_points[0][1])])
    for i in range(len(_color_points)-1):

        # step_point=np.array([float(color_points[i][0]),float(color_points[i][1])])
        # next_=np.array([float(color_points[i+1][0]),float(color_points[i+1][1])])
        
        # distance_=distance_between_points(step_point,next_)
        # print("step_point:",step_point)
        # print("next:",next_)
        while distance_between_points(step_point, next_) > distance:
            found_point=check_if_is_close_to_any_point_in_list(np.copy(step_point), tmp_all_points_list, distance, np.copy(start))
            

            if found_point is not None:
                # print(distance_between_vector_and_point(step_point,next_, found_point))
                angle_between_vectors=(get_angle_between_vectors(next_-step_point, found_point-step_point))
                if angle_between_vectors>0:

                    theta = np.deg2rad(-90)
                    versor=get_versor(step_point,next_,0.1)
                    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
                    step_point+=np.dot(versor,rot)
                    path_points.append(np.copy(step_point))
                else:
                    
                    theta = np.deg2rad(90)
                    versor=get_versor(step_point,next_,0.1)
                    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
                    step_point+=np.dot(versor,rot)
                    path_points.append(np.copy(step_point))
                continue
            step_point+=get_versor(step_point,next_,0.1)
            path_points.append(np.copy(step_point))
    

        
        ################ UNCOMMENT THIS TO SEE EVERY STEP #################
        # plt.scatter(x_all, y_all, marker='o', c='yellow') 
        # color_now='brown'
        # plt.scatter([float(xx[0]) for xx in color_points if xx[2]==color_now], [float(yy[1]) for yy in color_points if yy[2]==color_now], marker='o', c=color_now) 
        # color_now='gold'
        # plt.scatter([float(xx[0]) for xx in color_points if xx[2]==color_now], [float(yy[1]) for yy in color_points if yy[2]==color_now], marker='o', c=color_now) 
        # x = [xx[0] for xx in path_points]
        # y = [yy[1] for yy in path_points]
        # plt.xlim(BBox[0]-(BBox[1]-BBox[0])/10, BBox[1]+(BBox[1]-BBox[0])/10)
        # plt.ylim(BBox[2]-(BBox[3]-BBox[2])/10, BBox[3]+(BBox[3]-BBox[2])/10)
        # plt.scatter(x, y, c='b', s=0.1)
        # # plt.scatter(x_color, y_color, marker='o', c='g') 
        # plt.show()
        ####################################################################


        #in this place we are close enough to aim
        #rotate dog and shoot
        # if i<len(color_points):
        #     # print("-------- COLOR OF POINT NOW IS:", color_points[i][2],"--------")
        # else:
        #     print("-------- END OF TRAVEL --------")
            
        # step_point=np.copy(next_)
        next_=np.array([float(_color_points[i+1][0]),float(_color_points[i+1][1])])

    
    x = [xx[0] for xx in path_points]
    y = [yy[1] for yy in path_points]

    plt.xlim(BBox[0]-(BBox[1]-BBox[0])/10, BBox[1]+(BBox[1]-BBox[0])/10)
    plt.ylim(BBox[2]-(BBox[3]-BBox[2])/10, BBox[3]+(BBox[3]-BBox[2])/10)

    plt.scatter(x_all, y_all, marker='o', c='yellow') 
    color_now='brown'
    plt.scatter([float(xx[0]) for xx in color_points if xx[2]==color_now], [float(yy[1]) for yy in color_points if yy[2]==color_now], marker='o', c=color_now) 
    color_now='gold'
    plt.scatter([float(xx[0]) for xx in color_points if xx[2]==color_now], [float(yy[1]) for yy in color_points if yy[2]==color_now], marker='o', c=color_now) 
    # plt.plot(x, y, '-', '-r')
    plt.scatter(x, y, c='b', s=0.1)
    # plt.scatter(x_all, y_all, marker='o', c='g') 
    plt.show()

    return path_points

# if __name__ == "__main__":
#     main([[1.0, 5.0, 'brown', 'false'], [7.0, 3.0, 'brown', 'false'], [10.0, 10.0, 'brown', 'false'], [2.5, 4.0, 'gold', 'false']], [[2.9, 4.0, 'white', 'false'], [1.2, 5.0, 'white', 'false'], [0.0, 0.0, 'white', 'false'], [9.0, 8.8, 'white', 'false'], [9.0, 6.7, 'white', 'false'], [2.0, 0.7, 'white', 'false'], [9.0, 6.7, 'white', 'false']])

# , [3.5, 4.0, 'white', 'false']


#TODO
#check points where dog can be blocked (maybe random angle should be applied or repeating steps should be checked)
#how should start and end point look like? how dog should behave?