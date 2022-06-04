import h5py
from time import sleep
import numpy as np
from PIL import Image
from matplotlib.pyplot import imshow
import depth_map_to_point_cloud
import pandas as pd
import matplotlib.pyplot as plt
import yaml


def h5py_parser(filename):
    """Parses the .hdf5 file into components

    Parameters
    ----------
    filename : Input model file .hdf5 format
    Returns
    -------
    depth_map : Numpy array contains XYZ
                coordinate values of 
                reflected object rays.
    intensity_map: Pixel intensity values of
                   given image in model file
    horizontal_fov: Horizontal field of view
    vertical_fov: Vertical field of view
    """

    content = h5py.File(filename, "r")
    depth_map = content["depth_map"][:]
    intensity_map = content["intensity_map"][:]
    horizontal_fov = content["depth_map"].attrs["horizontal_fov_deg"]
    vertical_fov = content["depth_map"].attrs["vertical_fov_deg"]
    return depth_map, intensity_map, horizontal_fov, vertical_fov


def csv_saver(depth_map, horizontal_fov, vertical_fov, out_file):
    """Parses and saves the XYZ coordinates of point cloud

    Parameters
    ----------
    depth_map : Numpy array contains XYZ
            coordinate values of 
            reflected object rays.
    horizontal_fov: Horizontal field of view
    vertical_fov: Vertical field of view
    """

    point_cloud = depth_map_to_point_cloud.depth_map_to_point_cloud(depth_map, horizontal_fov, vertical_fov)
    np.savetxt(out_file, point_cloud, delimiter=",", header="x,y,z", comments="")


def show_depth_map(csv_file,upper_thresh=12.0 ,lower_thresh=0.0):
    """Plots and shows the point cloud in x-y-z axes with
       specified range

    Parameters
    ----------
    csv_file : Input point cloud file .csv format
    upper_thresh: Z-axis threshold value that
                  limits the maximum number
    lower_thresh: Z-axis threshold value that
                  limits the minumum number
    """

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
    ax.set_title("Point Cloud")
    ax.scatter3D(xline, yline, zline, cmap='Greens');
    plt.show()


def yaml_reader(filename):
    """Reads and parses the Z-axis threshold values
       from a configuration file with .yaml extension

    Parameters
    ----------
    filename : Input model file .yaml format
    Returns
    -------
    upper_thresh: Z-axis threshold value that
                  limits the maximum number
    lower_thresh: Z-axis threshold value that
                  limits the minumum number
    """

    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.loader.SafeLoader)
        upper_thresh = data["UpperThreshold"]
        lower_thresh = data["LowerThreshold"]
        return upper_thresh, lower_thresh


def export_csv(csv_file, upper_thresh, lower_thresh):
    """Removes the outbound points w.r.t Z-axis min-max
    limit values

    Parameters
    ----------
    csv_file : Input point cloud file .csv format
    upper_thresh: Z-axis threshold value that
                  limits the maximum number
    lower_thresh: Z-axis threshold value that
                  limits the minumum number
    """

    df = pd.read_csv(csv_file)
    df = df[df['z'] < upper_thresh]
    df = df[df['z'] > lower_thresh]
    df.to_csv("./pcl_files/u"+str(upper_thresh)+"l"+str(lower_thresh)+".csv", encoding='utf-8', index=False)



########### Test Code ################

# h5py_file = "cuboid-sphere.hdf5"
# csv_file = "point_cloud_xyz.csv"
# yaml_file = "thresholds.yaml"
# depth_map, intensity_map, horizontal_fov, vertical_fov = h5py_parser(h5py_file)
# csv_saver(depth_map, horizontal_fov, vertical_fov, csv_file)
# upper_thresh, lower_thresh = yaml_reader(yaml_file)
# show_depth_map(csv_file, upper_thresh, lower_thresh)
# export_csv(csv_file, 9.2, 5.0)

