import MDAnalysis as md
import numpy as np

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ------------------------------------
# Turn the input selection into a text
def _get_selection(selection, selection_type = 'resname'):

    # Convert the input if it is not a list or tuple
    if isinstance(selection, str) or isinstance(selection, int):
        selection = [selection]

    # Convert into string
    # Single element
    if len(selection) == 1:
        selection_text = selection_type + ' ' + str( selection[0] )

    # List of several elements
    else:
        selection_text = '(' + selection_type + ' ' + str(selection[0])

        for item in selection[1:]:
            selection_text += ' or ' + selection_type + ' ' + str(item)

        selection_text += ')'

    return selection_text

# --------------------------------------------
# Select the molecules to extract specifically
def _select_molecules(system, **kwargs):

    # Read the argument
    add_hydrogen = kwargs.get('hydrogens', True)
    text_selection = kwargs.get('selection', None)
    resname_selection = kwargs.get('resnames', None)
    name_selection = kwargs.get('names', None)
    resid_selection = kwargs.get('resids', None)

    # Check if a text selection has been given
    if text_selection is not None:
        selection = system.select_atoms(text_selection)

    # Check if any other type of selection is given
    elif resname_selection is not None or name_selection is not None or resid_selection is not None:

        # Initialise the text selection
        text_selection = ''

        # Add residue name selection
        if resname_selection is not None:
            text_selection += _get_selection(resname_selection, selection_type='resname')

        # Add atom name selection
        if name_selection is not None:

            # Add separator if needed
            if text_selection != '':
                text_selection += ' and '

            # Add the text
            text_selection += _get_selection(name_selection, selection_type='name')

        # Add the residue id selection
        if resid_selection is not None:

            # Add separator if needed
            if text_selection != '':
                text_selection += ' and '

            # Add the text
            text_selection += _get_selection(resid_selection, selection_type='resid')

        # Remove the hydrogen if requested
        if not add_hydrogen:
            text_selection += ' and not type H'

        # Get the selection
        selection = system.select_atoms(text_selection)

    # Select everything otherwise
    else:

        # Remove the hydrogen if requested
        if not add_hydrogen:
            text_selection = 'not type H'
        else:
            text_selection = 'all'

        selection = system.select_atoms(text_selection)

    return selection

# ---------------------------------------------------
# Read the given selection to extract the information
def _read_selection(selection):

    # Get the list of all residue ids
    list_resids = np.unique( selection.resids )

    # Loop over all the IDs
    all_data = {}
    for id in list_resids:

        # Extract the residue name
        crt_resname = selection.resnames[ selection.resids == id ][0]

        # Extract the atom names
        crt_names = np.copy( selection.types[ selection.resids == id ] )

        # Extract the atom positions
        crt_positions = np.copy( selection.positions[ selection.resids == id ] )

        # Add to the dictionary
        all_data[ id ] = {
        'resname' : crt_resname,
        'names' : crt_names,
        'positions' : crt_positions
        }

    return all_data

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------
# Open the MD file
def open_file(structure_file, **kwargs):

    # Load the system from the file
    system = md.Universe(structure_file)

    # Refine the selection if required
    selection = _select_molecules(system, **kwargs)

    # Extract the information from the selection
    data = _read_selection(selection)

    return data
