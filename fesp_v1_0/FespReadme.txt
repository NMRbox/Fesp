

#############################################################
INTRODUCTION:
Fesp: Filament End and Single Particle Picker

INPUT FILES:  
    Protein_001_s2.mrc       (image file -------------------- uneditable --- required)
    Protein_001_s2_fesp.star (coordinate file --------------- editable ----- optional)    
    Protein_001_s2_pick.star (alternative coordinate file --- editable ----- optional)
    Protein_001_s2_ref.star  (reference coordinate file ----- uneditable --- optional)
    ...

The .mrc & .star files can be read into Fesp via either the File menu or the command line.
If the _fesp.star exists, the corresponding _pick.star will be ignored.   
    
OUTPUT FILES: 
    Protein_001_s2_fesp.star (edited coordinate file)
    ...

RELION STAR FILE FORMAT:

data_

loop_ 
_rlnCoordinateX #1 
_rlnCoordinateY #2 
_rlnClassNumber #3 
_rlnAnglePsi #4 
_rlnAutopickFigureOfMerit #5 
  1864.000000  1672.000000	   8 	107.123456     3.253871 

#############################################################
USAGES:
[*] Open files: 
    Change to the directory holding .mrc (and .star) files, then type 'fesp *.mrc'.
    An alternative way to open files is to use the 'File' menu (might be slow).    
    Micrographs (required; *.mrc)
    Coordinates (optional; *_fesp.star/*_pick.star and *_ref.star) 
    All the coordinates are in Relion .star format. See the example for details. 
[*] Pick a particle: 
    Left click.
[*] Move a particle: 
    Left hold and drag.
[*] Delete a particle: 
    Shift and left click.
[*] Delete a cluster of particles: 
    Ctrl then right hold and drag.
[*] Navigate the picked particles one by one: 
    Click on a particle on the left panel, then hit 'space bar (PgUp)/left arrow (PgDn)'.
[*] Change the sizes of squares (_ref.star) and circles (_fesp.star/_pick.star): 
    Use the two text boxes on the left side of the "Resize" button.
[*] Change micrograph contrast:
    Choose a different sigma value.
[*] Display the in-plane rotation angle psi: 
    Use the "Psi" button or middle click to toggle between displaying and hiding.
[*] Display the picked particles: 
    Use the "Box" button or middle click to toggle between displaying and hiding.
[*] Calculate psi: 
    Left click, then hold 'Alt' and right click around (not on) the particle.
[*] Estimate psi: 
    Use the text box on the right side of the 'Psi' button.
[*] Change the box color (FOM): 
    Use the right most text box.
    [>=5: green; >=4 yellow; >=3: orange; >=2: magenta >=1: red; others: white]
[*] Read initial settings: 
    Put 'FespSettings.txt' in your working directory (in priority) or home directory.
    
    
#############################################################
REQUIRED 3RD-PARTY PACKAGES: 
1. Python 
2. NumPy 
3. wxPython
4. Imaging (Mac Only)


#############################################################
TESTED PLATFORM:
Red Hat Enterprise Linux 7.5 (GCC 4.8.5)
MacOS (10.13.4)


#############################################################
INSTALLATION PROCEDURES (using conda or miniconda): 
# Load miniconda module
module load miniconda
# Create a conda environment named FespEnv
conda create -yn FespEnv numpy python=2
# Activate FespEnv
conda activate FespEnv
# Install wxPython
conda install -y wxpython=4
# Deactivate FespEnv
conda deactivate

nedit ~/.cshrc &
# Append sth like this to the file.
# On Linux
# Fesp
alias fesp.py "module load miniconda; conda activate FespEnv; python /prog/local/Fesp/fesp_v1_0/fesp.py"
alias fesp    "module load miniconda; conda activate FespEnv; python /prog/local/Fesp/fesp_v1_0/fesp.py"
or
alias fesp.py "~/conda_envs/FespEnv/bin/python /prog/local/Fesp/fesp_v1_0/fesp.py"
alias fesp    "~/conda_envs/FespEnv/bin/python /prog/local/Fesp/fesp_v1_0/fesp.py"

# On Mac
# Fesp
alias fesp.py "source /Users/username/opt/miniconda3/etc/profile.d/conda.csh; conda init tcsh; conda deactivate; conda activate FespEnv;
/Users/username/opt/miniconda3/envs/FespEnv/bin/pythonw /prog/local/Fesp/fesp_v1_0/fesp.py"
alias fesp    "source /Users/username/opt/miniconda3/etc/profile.d/conda.csh; conda init tcsh; conda deactivate; conda activate FespEnv;
/Users/username/opt/miniconda3/envs/FespEnv/bin/pythonw /prog/local/Fesp/fesp_v1_0/fesp.py"

# If you get an "ImportError: The _imaging C module is not installed" on mac, 
# (1) try "rm -rf /prog/local/Fesp/fesp_v1_0/PIL/*.pyc /prog/local/Fesp/fesp_v1_0/PIL/*.so"
# (2) if it still didn't work, try to install Imaging using /Users/username/opt/miniconda3/envs/FespEnv/bin/python (see below).


#############################################################
INSTALLATION PROCEDURES (from source code):
# To avoid conflicts, comment the lines releated to EMAN2 and others in your .cshrc file first.

1. Installing Python
mkdir /prog/local/Fesp
cd /prog/local/Fesp
ls
tar -zxvf Python-2.7.6.tgz 
ls
cd Python-2.7.6
ls
#./configure --prefix=/prog/local/Fesp/Python --enable-framework=/prog/local/Fesp/Python
./configure --prefix=/prog/local/Fesp/Python
make
make install
nedit ~/.cshrc &
Append sth like this to the file.
# Python 2.7.6
setenv PATH /prog/local/Fesp/Python/bin:$PATH 
source ~/.cshrc


2. Installing NumPy
cd /prog/local/Fesp
tar -zxvf numpy-1.8.1.tar.gz
ls 
cd numpy-1.8.1
# for Xcode 4.2
#setenv CC clang
#setenv CXX clang++
#setenv FFLAGS -ff2c
/prog/local/Fesp/Python/bin/python setup.py build
/prog/local/Fesp/Python/bin/python setup.py install
# This will install NumPy in the Python site-packages directory.
nedit ~/.cshrc &
Append sth like this to the file.
# NumPy 1.8.1
# It has been copied to Python site-packages directory.


3. Installing wxPython
# I tried 2.8, 2.9 and 3.0; only 3.0 can be compiled!
cd /prog/local/Fesp
tar -jxvf wxPython-src-3.0.0.0.tar.bz2
ls 
cd wxPython-src-3.0.0.0
ls
cd wxPython
/prog/local/Fesp/Python/bin/python build-wxpython.py --build_dir=../bld 
/prog/local/Fesp/Python/bin/python build-wxpython.py --build_dir=../bld --install
# This will install wxPython in the Python site-packages directory.
nedit ~/.cshrc &
Append sth like this to the file.
# wxPython 3.0.0.0
# It has been copied to Python site-packages directory.

4. Installing Imaging
tar -xvf Imaging-1.1.7.tar
cd Imaging-1.1.7
python setup.py clean
rm -f *.so PIL/*.so
python setup.py build_ext -i
python selftest.py
python setup.py build
python setup.py install
nedit ~/.cshrc &
Append sth like this to the file.
# Imaging 1.1.7
# It has been copied to Python site-packages directory.

5. Installing Fesp
cd /prog/local/Fesp
tar -zxvf fesp.tar.gz
cd fesp
ls
nedit ~/.cshrc &
Append sth like this to the file.
# Fesp
alias fesp.py "/prog/local/Fesp/Python/bin/python /prog/local/Fesp/fesp/fesp.py"
alias fesp    "/prog/local/Fesp/Python/bin/python /prog/local/Fesp/fesp/fesp.py"

source ~/.cshrc
fesp


#############################################################
LICENSES:
Fesp has not been licensed yet. Feel free to redistribute/modify it.


#############################################################
DECLARATIONS:
Some codes were inspired by SamViewer.

