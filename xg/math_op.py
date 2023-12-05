import numpy as np
from scipy.spatial import distance
from scipy.ndimage import gaussian_filter

def triangle_area(a:np.ndarray,b:np.ndarray,c:np.ndarray):
    """Calculates triangle area"""
    AB = b - a
    AC = c - a
    
    return abs(np.cross(AB,AC)) / 2

def point_inside_triangle(a:np.ndarray,b:np.ndarray,c:np.ndarray,point:np.ndarray):
    """Given 3 points that define the triangle (a,b,c), checks if point is inside the triangle."""
    AREA = triangle_area(a,b,c)
    area = 0
    area += triangle_area(a,b,point)
    area += triangle_area(point,b,c)
    area += triangle_area(a,point,c)
    
    return area == AREA

def point_inside_circle(point : np.ndarray,center : np.ndarray,radius : float):
    """Check if point is inside a circle with given radius"""

    dist = distance.euclidean(point,center)
    return dist < radius

def angle_between_vectors(p1 : np.ndarray,p2:np.ndarray,p3:np.ndarray):
    """Angle between the vectors formed by p1p2 and p1p3"""
    V1 = p1 - p2
    V2 = p1 - p3
    
    V1n = V1 / np.linalg.norm(V1)
    V2n = V2 / np.linalg.norm(V2)
    
    theta = np.arccos(np.dot(V1n,V2n))
    ang = theta * (180 / np.pi)
    return ang

def apply_gaussian_filter(Matrix : np.ndarray,sigma=1.,radius=1):
    return gaussian_filter(Matrix, sigma=sigma,radius=radius)