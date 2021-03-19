import numpy as np
from stl import mesh

##-\-\-\-\-\-\
## BASE FIGURES
##-/-/-/-/-/-/

"""Code for sphere creation taken from:
http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html
All credits go to the author"""

# -----------------------------------
# Get the vertices of the icosahedron
def _get_icosahedron_vertices():

    # Get the base variable
    t = (1 + np.sqrt(5)) / 2

    # Define the vertices
    vertices = np.array([
    [-1, t, 0],
    [1, t, 0],
    [-1, -t, 0],
    [1, -t, 0],

    [0, -1, t],
    [0, 1, t],
    [0, -1, -t],
    [0, 1, -t],

    [t, 0, -1],
    [t, 0, 1],
    [-t, 0, -1],
    [-t, 0, 1]
    ])

    # Normalise by length
    length = np.sqrt( np.sum(vertices**2, axis=1) )
    vertices = vertices / length[:,np.newaxis]

    return vertices

# --------------------------------
# Get the faces of the icosahedron
def _get_icosahedron_faces():

    # Define the faces
    faces = np.array([
    [0,11,5],
    [0,5,1],
    [0,1,7],
    [0,7,10],
    [0,10,11],

    [1,5,9],
    [5,11,4],
    [11,10,2],
    [10,7,6],
    [7,1,8],

    [3,9,4],
    [3,4,2],
    [3,2,6],
    [3,6,8],
    [3,8,9],

    [4,9,5],
    [2,4,11],
    [6,2,10],
    [8,6,7],
    [9,8,1]
    ])

    return faces

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ------------------------------------------------------------
# Get the middle point of the two triangles on the unit sphere
def _get_middle_point(vertices, a, b):

    # Sort the indices
    a, b = np.sort([a, b])

    # Get the points
    pa, pb = vertices[a], vertices[b]

    # Calculate the middle point
    mid_p = (pa + pb)/2

    # Correct by length
    len_p = np.sqrt( np.sum(mid_p**2) )
    mid_p = mid_p / len_p

    # Add the new point to the vertices
    new_index = len(vertices)
    vertices = np.vstack([vertices, mid_p])

    return new_index, vertices

# --------------------
# Refine the triangles
def _refine_sphere_triangles(vertices, faces):

    # Loop over all the triangles
    for vx,vy,vz in faces:

        # Define new points for the new triangles
        a, vertices = _get_middle_point(vertices, vx, vy)
        b, vertices = _get_middle_point(vertices, vy, vz)
        c, vertices = _get_middle_point(vertices, vz, vx)

        # Add the new face
        faces = np.vstack( [faces,
        np.array([vx, a, c]),
        np.array([vy, b, a]),
        np.array([vz, c, b]),
        np.array([a, b, c])
        ] )

    return vertices, faces

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -------------------
# Generate the sphere
def generate_sphere(**kwargs):

    # Extract the parameters
    resolution = kwargs.get('resolution',3)

    # Get the sphere vertices and faces
    vertices = _get_icosahedron_vertices()
    faces = _get_icosahedron_faces()

    # Refine the mesh
    if resolution > 0:

        # Repeat as much as needed
        for i in range(resolution):
            vertices, faces = _refine_sphere_triangles(vertices, faces)

    # Create the mesh
    sphere = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            sphere.vectors[i][j] = vertices[f[j],:]

    return sphere
