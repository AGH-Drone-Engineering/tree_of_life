import matplotlib.pyplot as plt
import numpy as np
import math

start = np.array([0., 0.])
point = np.array([7., 3.])
distance=0.5

points_list=[]
points_list.append(start)
points_list.append(point)
points_list.append((1.,5.))
points_list.append((2.5, 4))
end = (10., 10.)
points_list.append(end)  # list of trees coords

def distance_between_points(p1,p2):
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
            print("Yes: ", p)
            return p
    return None
     
all_points_list = [(2,0.7),(1.2, 5), (2.9, 4), (3.5,4), (9, 6.7), (9, 8.8), (7, 3)]
all_points_list = np.concatenate((all_points_list, points_list))  # concatenate the two arrays
all_points_list = np.unique(all_points_list, axis=0)  # remove duplicate points


x = [xx[0] for xx in points_list]
y = [yy[1] for yy in points_list]
x_all = [xx[0] for xx in all_points_list]
y_all = [yy[1] for yy in all_points_list]

#move step by step
path=[]

for i in range(len(points_list)-1):

    step_point=np.copy(np.copy(points_list[i]))
    next_=np.copy(points_list[i+1])
    distance_=distance_between_points(step_point,next_)
    while distance_between_points(step_point, next_)>distance:
        found_point=check_if_is_close_to_any_point_in_list(np.copy(step_point),all_points_list, distance,np.copy(start))
        if found_point is not None:
            print(distance_between_vector_and_point(step_point,next_, found_point))
            angle_between_vectors=(get_angle_between_vectors(next_-step_point, found_point-step_point))
            if angle_between_vectors>0:

                theta = np.deg2rad(-90)
                versor=get_versor(step_point,next_,0.2)
                rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
                step_point+=np.dot(versor,rot)
                path.append(np.copy(step_point))
            else:
                
                theta = np.deg2rad(90)
                versor=get_versor(step_point,next_,0.2)
                rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
                step_point+=np.dot(versor,rot)
                path.append(np.copy(step_point))
            continue
        step_point+=get_versor(step_point,next_,0.2)
        path.append(np.copy(step_point))
    step_point=np.copy(next_)
    next_=np.copy(points_list[i+1])

x = [xx[0] for xx in path]
y = [yy[1] for yy in path]

plt.xlim(0, 10)
plt.ylim(0, 10)

plt.plot(x, y, '-', '-r')
plt.scatter(x, y, c='b', s=0.1)
plt.scatter(x_all, y_all, marker='o', c='g') 
plt.show()
