import numpy as np


def depth_map_to_point_cloud(depth_map, horizontal_fov_degrees, vertical_fov_degrees):
    """Convert depth map to point cloud.

    Parameters
    ----------
    depth_map : array_like
        2d depth map array
    horizontal_fov_degrees : float
        Horizontal field of view in degrees
    vertical_fov_degrees : float
        Vertical field of view in degrees

    Returns
    -------
    point_cloud : array_like
        Point cloud array -- each row is a coordinate triplet (x, y, z).
        Directions are: forward Z; Up -Y; Right X
    """

    nrows, ncols = depth_map.shape

    # Tangents of maximum elevation and azimuth angles (at the FOV edges)
    tan_max_elev = np.tan(np.radians(vertical_fov_degrees / 2))
    tan_max_azimuth = np.tan(np.radians(horizontal_fov_degrees / 2))

    def get_xyz(i, j):
        # Calculate point xyz-coordinates. `i` and `j` are depth map array indices.
        # Coordinates are: forward Z; Up -Y; Right X
        tan_theta_y = (i - nrows // 2) * tan_max_elev / (nrows // 2)
        tan_theta_x = (j - ncols // 2) * tan_max_azimuth / (ncols // 2)

        z = depth_map[i, j]
        x = z * tan_theta_x
        y = z * tan_theta_y

        return np.array([x, y, z])

    I, J = np.meshgrid(np.arange(nrows), np.arange(ncols), indexing='ij')
    mask = np.logical_not(np.isnan(depth_map)).flatten()
    # Only calculate points where depth_map has a numerical value
    point_cloud = get_xyz(I.flatten()[mask], J.flatten()[mask]).T

    return point_cloud

