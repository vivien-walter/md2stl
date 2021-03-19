import stl

from md2stl.build_structure import build_atoms, scale_system
from md2stl.extract_molecules import open_file
from md2stl.system_class import get_class

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## MD SIMULATION MANIPULATION
##-/-/-/-/-/-/-/-/-/-/-/-/-/

# -----------------------
# Load the structure file
def loadFile(structure_file, **kwargs):

    """Function to load a simulation file and extract the system to render.
    The list of compatible files can be found at https://userguide.mdanalysis.org/stable/formats/index.html

    INPUT(S):
    - structure_file {path-like str} : Simulation file to open.
    - hydrogens {bool} : (Opt.) Keep the hydrogen atoms. Default is False.
    - selection {str} : (Opt.) Text selection to apply on the system file. Override the other selectors listed below. Default is all.
    - resnames {str or list of str} : (Opt.) List of the residue names to keep in the representation. Default is all.
    - names {str or list of str} : (Opt.) List of the atom names to keep in the representation. Default is all.
    - resids {int or list of int} : (Opt.) List of the residue IDs to keep in the representation. Default is all.

    OUTPUT(S):
    - system_class {System class instance} : System containing all the molecules of the system and the relevant information.
    """

    # Open the simulation file to extract the informations
    data = open_file(structure_file, **kwargs)

    # Convert the data into a system class
    system_class = get_class(data)

    return system_class

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## PRODUCTION OF THE 3D ELEMENTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# --------------------------------------------------------------
# Convert the 3d positions and atom types into a 3d construction
def build3D(system_class, **kwargs):

    """Function to build the 3D objects based on the given system.

    INPUT(S):
    - system_class {System class instance} : System containing all the molecules of the system and the relevant information. Typically extracted using the function loadFile.
    - scale {float} : (Opt.) Desired max length in millimetre of the object along the given axis. Default is 100.
    - axis {int} : (Opt.) Axis to use for the max length of the system: 0 is X, 1 is Y and 2 is Z. Default will take whatever longest length is found.
    - sphere_scale {float} : (Opt.) Additional scale factor for the size of the atom spheres. Default is 1.
    OUTPUT(S):
    - all_atoms {Mesh class instance} : Collection of meshes to be exported.
    """

    # Rescale the system to the desired size
    new_class, system_factor = scale_system(system_class, **kwargs)

    # Build the particles
    all_atoms = build_atoms(new_class, system_factor, **kwargs)

    return all_atoms

# --------------------------------
# Save the 3d meshes in a stl file
def save3D(filename, system_3d):

    """Function to save the 3D objects in a .stl file.

    INPUT(S):
    - filename {path-like str} : Path and name of the file to be saved. Extension should be .stl.
    - system_3d {Mesh class instance} : Collection of meshes to be exported.
    """

    # Save in file
    system_3d.save(filename, mode=stl.Mode.ASCII)
