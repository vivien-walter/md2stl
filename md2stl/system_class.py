import numpy as np

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ------------------------
# Get the size of the atom
def _get_atom_size(atom_name):

    # All values in Angstrom
    all_radii = {
    'H':1.10,
    'C':1.70,
    'N':1.55,
    'O':1.52,
    'P':1.80,
    'S':1.80,
    }

    return all_radii[ atom_name ]

# -------------------------------------
# Merge all the positions of the system
def _merge_positions(system_positions):

    # Process all residues separately
    all_positions = []

    for resname in system_positions.keys():
        crt_positions = system_positions[resname]

        # Reshape the position array
        crt_positions = np.reshape(crt_positions, (crt_positions.shape[0]*crt_positions.shape[1],3))

        # Append the positions to the existing array
        all_positions.append(crt_positions)

    # Merge the arrays
    all_positions = np.concatenate( all_positions, axis=0 )

    return all_positions

##-\-\-\-\
## CLASSES
##-/-/-/-/

# --------------------------
# Class to define a molecule
class Molecule:
    def __init__(self, id, data):

        # Write the data
        self.id = id
        self.resname = data['resname']
        self.names = data['names']
        self.positions = data['positions']

        # Get the size array
        self.radii = np.array( [_get_atom_size(x) for x in self.names] )

# --------------------------------
# Class to define the whole system
class System:
    def __init__(self, molecule_data):

        # Process all the data
        self.molecules = {}
        for mol_ID in molecule_data.keys():
            self.molecules[ mol_ID ] = Molecule( mol_ID, molecule_data[ mol_ID ] )

    ##-\-\-\-\-\-\-\-\
    ## ACCESS FUNCTIONS
    ##-/-/-/-/-/-/-/-/

    # --------------------
    # Get the molecule IDs
    def getIDs(self):
        return np.array( list(self.molecules.keys()) )

    # ---------------------
    # Get all the positions
    def getPositions(self, single_array=False):

        # Process all the molecules
        all_positions = {}
        for id in self.getIDs():

            # Get the information
            crt_resname = self.molecules[id].resname
            crt_positions = self.molecules[id].positions

            # Add the resname to the dictionary if missing
            if crt_resname not in all_positions.keys():
                all_positions[crt_resname] = []

            # Add the positions to the dictionary
            all_positions[crt_resname].append( crt_positions )

        # Convert the lists to array
        for resname in all_positions.keys():
            all_positions[resname] = np.array( all_positions[resname] )

        # Return everything into a single array
        if single_array:
            return _merge_positions(all_positions)

        else:
            return all_positions

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -----------------------------------
# Load the data into the System class
def get_class(data):
    return System( data )
