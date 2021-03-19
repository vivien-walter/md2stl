from md2stl import loadFile, build3D, save3D

# Load the data
system_class = loadFile('structure.gro', resids=[1], hydrogens=False)

# Build the model
all_atoms = build3D(system_class, resolution=5)

# Save the model in file
save3D('test.stl', all_atoms)
