from copy import deepcopy
import numpy as np
from stl import mesh
from tqdm import tqdm

from md2stl.make_objects import generate_sphere

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ----------------------------
# Get the limits of the system
def _get_system_sizes(system):

    # Extract the min and max position of the system in all axis
    all_positions = system.getPositions(single_array=True)

    # Get the min and max values for each axis
    xlength = np.amax(all_positions[:,0]) - np.amin(all_positions[:,0])
    ylength = np.amax(all_positions[:,1]) - np.amin(all_positions[:,1])
    zlength = np.amax(all_positions[:,2]) - np.amin(all_positions[:,2])

    return [xlength, ylength, zlength]

# --------------------------------------
# Rescale the object by the given factor
def _rescale_objet(object, factor):

    object.x *= factor
    object.y *= factor
    object.z *= factor

    return object

# -------------------------------------
# Move the object to the given location
def _move_objet(object, new_position):

    object.x += new_position[0]
    object.y += new_position[1]
    object.z += new_position[2]

    return object

# -----------------------------------------------
# Rescale all the system to fit in the given unit
def _rescale_system(system, f):

    # Make a copy of the system
    new_system = deepcopy(system)

    # Process all the molecules
    for mol_ID in new_system.molecules.keys():
        new_system.molecules[mol_ID].positions = new_system.molecules[mol_ID].positions * f

    return new_system

# --------------------------------------------------
# Add the atom at the given position after rescaling
def _add_atom(sphere, positions, radius):

    # Copy the unit sphere
    atom = mesh.Mesh(sphere.data.copy())

    # Rescale the sphere
    atom = _rescale_objet(atom, radius)

    # Move the sphere
    atom = _move_objet(atom, positions)

    return atom

# ---------------------------------
# Populate the space with the atoms
def _populate_atoms(system, sphere):

    # Initialise the 3d space
    all_atoms = []

    # Loop over all the molecules
    for mol_ID in tqdm(system.molecules.keys()):

        # Get the current atom and positions
        crt_positions = system.molecules[mol_ID].positions
        crt_radii = system.molecules[mol_ID].radii

        # Loop over all the atoms
        for atom_ID in range(crt_positions.shape[0]):

            # Get the new object
            new_atom = _add_atom( sphere, crt_positions[atom_ID], crt_radii[atom_ID])

            # Append the new object
            all_atoms.append( new_atom.data.copy() )

    # Merge the meshes together
    all_atoms = mesh.Mesh(np.concatenate(all_atoms))

    return all_atoms

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------
# Rescale the system
def scale_system(system, **kwargs):

    # Get the arguments
    scale = kwargs.get('scale', 100)
    axis = kwargs.get('axis', None)

    # Get the limits of the system
    max_lengths = _get_system_sizes(system)

    # Select the length to scale by
    if axis is None:
        length = np.amax(max_lengths)
    else:
        length = max_lengths[axis]

    # Calculate the scaling factor
    f = scale / length

    # Rescale the positions
    new_system = _rescale_system(system, f)

    return new_system, f

# ------------------------------
# Build the atoms for the system
def build_atoms(system, system_factor, **kwargs):

    # Get the arguments
    sphere_scale = kwargs.get('sphere_scale', 1)

    # Get the unit sphere
    unit_sphere = generate_sphere(**kwargs)

    # Rescale the base sphere
    total_factor =  sphere_scale * system_factor * .7 # .7 is an arbitrary normalisation factor
    unit_sphere = _rescale_objet(unit_sphere, total_factor)

    # Fill the space with the atoms
    all_atoms = _populate_atoms(system, unit_sphere)

    return all_atoms
