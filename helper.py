import h5py
from time import sleep
import numpy as np
from PIL import Image
from matplotlib.pyplot import imshow
import depth_map_to_point_cloud
import pandas as pd
import matplotlib.pyplot as plt
import yaml
# %matplotlib inline

def h5py_parser(filename):
    content = h5py.File(filename, "r")
    depth_map = content["depth_map"][:]
    intensity_map = content["intensity_map"][:]
    horizontal_fov = content["depth_map"].attrs["horizontal_fov_deg"]
    vertical_fov = content["depth_map"].attrs["vertical_fov_deg"]
    return depth_map, intensity_map, horizontal_fov, vertical_fov

def csv_saver(depth_map, horizontal_fov, vertical_fov, out_file):
    point_cloud = depth_map_to_point_cloud.depth_map_to_point_cloud(depth_map, horizontal_fov, vertical_fov)
    np.savetxt(out_file, point_cloud, delimiter=",", header="x,y,z", comments="")

def show_depth_map(csv_file,upper_thresh=12.0 ,lower_thresh=0.0):
    df = pd.read_csv(csv_file)
    df = df[df['z'] < upper_thresh]
    df = df[df['z'] > lower_thresh]

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    xline = df['x']
    yline = df['y']
    zline = df['z']

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.scatter3D(xline, yline, zline, cmap='Greens');
    plt.show()

def yaml_reader(filename):
    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.loader.SafeLoader)
        upper_thresh = data["UpperThreshold"]
        lower_thresh = data["LowerThreshold"]
        return upper_thresh, lower_thresh

def export_csv(csv_file, upper_thresh, lower_thresh):
    df = pd.read_csv(csv_file)
    df = df[df['z'] < upper_thresh]
    df = df[df['z'] > lower_thresh]
    #print(df)
    df.to_csv("u"+str(upper_thresh)+"l"+str(lower_thresh)+".csv", encoding='utf-8', index=False)



########### Test Code ################
# h5py_file = "cuboid-sphere.hdf5"
# csv_file = "point_cloud_xyz.csv"
# yaml_file = "thresholds.yaml"
# depth_map, intensity_map, horizontal_fov, vertical_fov = h5py_parser(h5py_file)
# csv_saver(depth_map, horizontal_fov, vertical_fov, csv_file)
# upper_thresh, lower_thresh = yaml_reader(yaml_file)
# show_depth_map(csv_file, upper_thresh, lower_thresh)
# export_csv(csv_file, 9.2, 5.0)

