from setuptools import setup

setup(
	name = "md2stl",
	version = "0.1",
	author = "Vivien WALTER",
	author_email = "walter.vivien@gmail.com",
	description = (
	"Python tools to convert a MD simulation file into a .stl file ready to be 3d printed."
	),
	license = "GPL3.0",
	url='https://github.com/vivien-walter/md2stl',
	download_url = 'https://github.com/vivien-walter/md2stl/archive/v0.1.tar.gz',
	packages=[
	'md2stl'
	],
	install_requires=[
	'numpy',
	'numpy-stl',
	'MDAnalysis',
	'tqdm'
	]
)
