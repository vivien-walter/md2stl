# md2stl

![Version](https://img.shields.io/badge/version-0.1-f39f37)

## General

### Description

* Version: 0.1
* Author: Vivien WALTER
* Contact: walter.vivien@gmail.com

**md2stl** is a Python 3.x module with different tools that can be used to generate a .stl file ready to be 3d printed from a molecular dynamic (MD) simulation input file.

### Compatibility

md2stl relies on [MDAnalysis](https://www.mdanalysis.org) in order to open and process the simulation files.

The extensive list of all the simulation file formats which can be opened by md2stl can be found at [this link](https://userguide.mdanalysis.org/stable/formats/index.html).

### Release statement

The current version released on GitHub (v0.1) do not include the production of bonds between atoms or molecules. The different tests conducted have shown that the resulting 3d printed structures are too brittle.

It is therefore recommended to increase the size of the atoms to form strong connection between the different atoms or molecules. Read the documentation below for more details on how to increase the size of the atoms.

## Table of contents

1. [Installation](#installation)
  * [Requirements](#install_requires)
  * [Installation using the setup.py script](#install_howto)
2. [How-to use the module](#howto_tutorial)
  * [Load the simulation file](#howto_extract)
  * [Convert into 3D meshes](#howto_mesh)
  * [Save into a .stl file](#howto_save)
3. [API](#module_API)
  * [Functions](#module_functions)
     * [loadFile](#load_file)
     * [build3D](#build_3d)
     * [save3D](#save_3d)
  * [Classes](#module_classes)
     * [System](#system_class)
     * [Molecule](#molecule_class)

---

## Installation <a name="installation"></a>

### Requirements <a name="install_requires"></a>

The following modules are required to run md2stl:

* MDAnalysis
* NumPy
* numpy-stl
* tqdm

If you install the module using the setup.py script, you do NOT need to install first the module above.

### Installation using the setup.py script <a name="install_howto"></a>

1. Download the module folder on the github repo

- Installation in a **Terminal-based** environment

  2. Open a terminal in the module folder
  3. (Opt.) Start your virtualenv if you use one
  4. Type and run the command

     ```sh
     > python3 setup.py install
     ```

- Installation in an **Anaconda** environment

  2. Open Anaconda and go to your Environments
  3. Select the environment you want to install the module into
  4. Click on the arrow next to the name of the environment and select Open a Terminal
  5. Navigate to the module folder
  6. Type and run the command

  ```sh
  > python3 setup.py install
  ```

## How to use the module <a name="howto_tutorial"></a>

An example is provided in the *_examples* folder, both as .py script and as a Jupyter Notebook.

### Load the simulation file <a name="howto_extract"></a>

The first step of the conversion is to load the content of the simulation file. For this purpose, md2stl relies on the module MDAnalysis. Check [their website](https://userguide.mdanalysis.org/stable/formats/index.html) for the details on the supported file formats.

The content of the files are imported using the function **loadFile()**

```python
molecules = loadFile('path_to_file.pdb', hydrogen = False, resids=1)
```

Along with the path to the file to load, several optional arguments can be specified:

* *hydrogen=*, to specify if hydrogen atoms should be included or not. Default is True.
* *selection=*, to input a comprehensive text selection (e.g. 'resnames DPPC and not type P'). The different keywords that can be used can be found on the [MDAnalysis documentation](https://docs.mdanalysis.org/stable/documentation_pages/selections.html). Using *selection=* overrides the other selectors listed below.
* *resnames=*, to specify a list of residue names to select.
* *names=*, to specify a list of atom names to select.
* *resids=*, to specify a list of residue IDs to select.

If nothing is specified, all the atoms will be loaded.

The output of the function is an instance of the class System defined in md2stl. Read the API below for more information on the function and the class.

### Convert into 3D meshes <a name="howto_mesh"></a>

Once the desired molecules have been extracted, they can be converted into a collection of 3D meshes to represent the system as a 3d object. This is done using the function **build3D()**, which relies on the module numpy-stl for the production of the meshes.

```python
system_3d = build3D(molecules, resolution=5, scale=150)
```
Along with the instance of the System class to process, several optional arguments can be specified:

* *resolution=*, to specify the order of refining to use on the atom spheres. Recommandations are to use between 3 (low) and 6 (high). Default is 3.
* *scale=*, to specify the maximal size of the system along a given axis. The value has to be provided in millimetres. Default is 100mm.
* *axis=*, to specify the axis to use for the max length of the system: 0 is X, 1 is Y and 2 is Z. The length is then used to calculate the convertion factor to match the specified scale. Default will take whatever longest length is found.
* *sphere_scale=*, to specify an additional size factor for the size of the atom spheres. Default is 1.

The output of the function is an instance of the class Mesh defined in numpy-stl. Read the API below for more information on the function.

### Save into a .stl file <a name="howto_save"></a>

Once the 3d meshes have been constructed in the previous step, they can be saved in an .stl file using the function **save3D()**.

```python
save3D('path_to_file.stl', system_3d)
```

## API <a name="module_API"></a>

### Functions <a name="module_functions"></a>

The following functions are defined in md2stl

- **loadFile()** <a name="load_file"></a>

The function loadFile() is used to open a simulation file and extract the content to be later processed into a 3d object. The function can be typically used as:

```python
system_class = loadFile('path_to_file.pdb', hydrogens=False, resids=[1,2,5])
```

The function is based on MDAnalysis to open and read the content of the simulation files. The complete list of file formats that can be used can be found at [this link](https://userguide.mdanalysis.org/stable/formats/index.html).

*Input(s)*

Name | Type | Description
---|---|---
`structure_file` | Path-like string | Simulation file to open.
`hydrogens=` | Boolean | (Opt.) Keep the hydrogen atoms. Default is False.
`selection=` | String | (Opt.) Text selection to apply on the system file. Override the other selectors listed below. Default is all.
`resnames=` | String or List of strings | (Opt.) List of the residue names to keep in the representation. Default is all.
`names=` | String or List of strings | (Opt.) List of the atom names to keep in the representation. Default is all.
`resids=` | Integer or List of integers | (Opt.) List of the residue IDs to keep in the representation. Default is all.

*Output(s)*

Name | Type | Description
---|---|---
`system_class` | System class instance | System containing all the molecules of the system and the relevant information.

The *selection=* optional argument is based on MDAnalysis own syntax for molecule and atom selections. Description of the different keywords and tutorials can be found on [their website](https://docs.mdanalysis.org/stable/documentation_pages/selections.html).

- **build3D()** <a name="build_3d"></a>

The function build3D() is used to process the System class instance obtained through the loadFile() function and create a 3D space filled with atoms. The function can be typically used as:

```python
all_atoms = build3D(system_class, resolution=5, scale=150)
```

*Input(s)*

Name | Type | Description
---|---|---
`system_class ` | System class instance | System containing all the molecules of the system and the relevant information.
`resolution=` | Integer | (Opt.) Level of refining for the spheres used for the atom. Default is 3.
`scale=` | Float | (Opt.) Desired max length in millimetre of the object along the given axis. Default is 100.
`axis=` | Integer | (Opt.) Axis to use for the max length of the system: 0 is X, 1 is Y and 2 is Z. Default will take whatever longest length is found.
`sphere_scale=` | Float | (Opt.) Additional scale factor for the size of the atom spheres. Default is 1.

*Output(s)*

Name | Type | Description
---|---|---
`all_atoms` | Mesh class instance | Collection of meshes to be exported into a .stl file later.

The function **do not** produce any bond between atoms, as our first tests have shown that using smaller atoms and bonds for the structure would lead to brittle 3d printed objects. It is recommended to increase the value of *sphere_scale=* to generate connections between atoms and molecules in the same system.

The production of spheres is based on the tutorial and script from [Andreas Kahler](http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html). Details on the use of the *resolution=* argument can be found on his website.

The Mesh class used as an output here is a class defined in the module numpy-stl. Please read the documentation [there](https://github.com/WoLpH/numpy-stl) for more details on the class.

- **save3D()** <a name="save_3d"></a>

The function save3D() is used to save the Mesh class instance obtained through the build3D() function and create a into a .stl file ready to be 3d printed. The function can be typically used as:

```python
save3D('path_to_file.stl', all_atoms)
```

*Input(s)*

Name | Type | Description
---|---|---
`filename` | Path-like string | Path and name of the file to be saved. Extension should be .stl.
`all_atoms ` | Mesh class instance | Collection of meshes to be saved in the .stl file.


### Classes <a name="module_classes"></a>

The following classes are defined in md2stl

- **System** <a name="system_class"></a>

System is a class containing all the molecules extracted from the simulation file and their different properties relevant for 3D printing. The class attributes and methods are listed below:

**Attribute(s)**

Name | Type | Description
---|---|---
`system.molecules ` | List of Molecule class instances | Collection of all the molecules extracted from the simulation file. Each molecule is represented via an instance of the Molecule class defined below.

**Method(s)**

1. *system.getIDs()*

 Return the list of all the molecule IDs stored in the System class. The list is provided as a NumPy array.

2. *system.getPositions(single_array=)*

 Return the positions of all the atoms in the system. If single\_array is True, a single NumPy array of the shape (N atoms, 3) is returned for all molecules together. If single\_array is False, a dictionary of all the residue names containing each a NumPy array of the shape (N molecules, N atoms per molecule, 3) is returned.

- **Molecule** <a name="molecule_class"></a>

Molecule is a class containing all the different properties of a molecule relevant for 3D printing. The class attributes are listed below:

**Attribute(s)**

Name | Type | Description
---|---|---
`molecule.id` | Integer | ID of the molecule in the system, as given by MDAnalysis.
`molecule.resname` | String | Name of the molecule in the system, as given by MDAnalysis.
`molecule.names` | Array of String | Collection of all the types of the atoms making the molecule, e.g. C, N, O. Shape of the array is (N atoms, ).
`molecule.positions` | Array of Float | Collection of all the 3D positions of the atoms making the molecule. Shape of the array is (N atoms, 3).
`molecule.radii` | Array of Float | Collection of all the radii of the atoms making the molecule. Shape of the array is (N atoms, ).

The radii of the atoms are attributed based on their type (*molecule.names*) and their corresponding [Van der Waals radii](https://en.wikipedia.org/wiki/Van_der_Waals_radius).
