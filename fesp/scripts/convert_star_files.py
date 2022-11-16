#!/usr/bin/python
#
# AUTHOR: Steven Chou 
# (steven.chou@yale.edu)
#
# MCDB, Yale
# Created on: 04/04/2016
# Modified on: 05/02/2016
#
#

########################################################################
# References

'''
Not Available
'''

########################################################################
# Import modules

import sys, re, string, os, os.path, math, time, shutil


########################################################################
# Usage

if len(sys.argv) != 5:

  print('''
  
  Usage:''',sys.argv[0],''' input_star_file  output_star_dir  output_star_ext  binning_factor
  Notes:
         input_star_file  Input .star file. ALL the particles in all the images are in ONE .star file.
                          e.g., particles.star (after Clas2D or Class3D or Selection); _rlnAnglePsi will be read.
         output_star_dir  Output directory for all the .star files. ONE .star for each image.
                          e.g., pick_star_files
         output_star_ext  Output star file extension.
                          e.g., _pick.star  or  _ref.star                  
         binning_factor   Coordinate binning factor. >1: shrinking; =1: no change; <1: expanding
                          e.g., 2
         
         Put both .mrc and _pick.star files in NEW_Relion_Proj_Dir/Micrographs before working on Fesp or Relion!
         
         To display the coordinates (XY), Psi angle and FOM in images in Fesp:
             (1) Go to the directory holding both .mrc and .star files; Launch Fesp. 
                 In Fesp GUI: Open .mrc files; _pick.star and _ref files will be read and displayed automatically.
                  The two text boxes right to 'Save Ptcls' can be used to change Psi and FOM manually.
         
         
         To display the coordinates in images in Relion (4 STEPS):
             (1) [OPTIONAL]Import Micrographs:
                 Import => I/O: Input files: Micrographs/*.mrc;       Node type: 2D micrographs/tomographs
             (2) Save job settings for manual picking:
                 Manual picking => I/O; Display: (ptcl diameter, scaling, pixel size); ; Colors => Jobs => Save job settings  
             (3) Import Coordinates:         
                 Import => I/O: Input files: Micrographs/*_pick.star; Node type: 2D/3D particle coordinates
             (4) Display the coordinates on images:         
                 Import => Display: out: coords_suffix_pick.star
         Now, you can add particles w/ left click, delete them w/ middle click, and edit the file w/ right click.\n''')

  sys.exit()
 
 
########################################################################
# I/O files

input_file_star      = sys.argv[1]
output_star_dir      = sys.argv[2]
output_star_ext      = sys.argv[3]
binning_factor       = float(sys.argv[4])



if not os.path.exists (input_file_star):
    print("#### input_star_file: "+input_file_star+" does not exists.")
    exit (0)
    
if os.path.exists (output_star_dir):
    print("#### output_box_dir: "+output_star_dir+" exists. It'll be deleted first and then created again.")    
    try:
        shutil.rmtree(output_star_dir) 
    except OSError:
        pass
    os.system("mkdir "+output_star_dir)
else:
    os.system("mkdir "+output_star_dir)
    
print("***********************************************************************************************")
print("input file:  input data.star from 2DC;                    ", input_file_star)   
print("output dir:  output directory holding *.star;        ", output_star_dir)        
print("output ext:  output .star file extension;            ", output_star_ext)        
print("option:      binning factor (float);                 ", binning_factor)
print("***********************************************************************************************")    


########################################################################
# Main

max_col_num_in_inp     = 0

flag_data_particles             = 0
curr_ptcl_line_num             = 0 

col_no_rln_micName     = 0 
col_no_rln_clsNum      = 0
col_no_rln_coordX      = 0
col_no_rln_coordY      = 0
col_no_rln_angPsi      = 0
col_no_rln_angPsiPrior = 0


num_of_non_ptcl_lines_in_inp         = 0
num_of_ptcl_lines_in_inp           = 0   

#### get the column numbers
sys.stdout.write("Collecting statistics from : %s \r" % (input_file_star ) )            
filehandle_inp_ptcls_star         = open(input_file_star,  "r")
while True :
    line_inp = filehandle_inp_ptcls_star.readline()

    if len(line_inp) == 0:     ## In fact, blank lines are "\n".
        break
    line_inp = line_inp.rstrip('\n')         ## remove "\n" 
    array_inp = re.split(r'\s+', line_inp)
    
    if max_col_num_in_inp < len(array_inp):
        max_col_num_in_inp = len(array_inp)
    
    if array_inp[0] == "data_particles":
            flag_data_particles  = 1  
        
    if flag_data_particles  == 0:
            #filehandle_out.write( "%s\n" % (line_inp))  
        num_of_non_ptcl_lines_in_inp = num_of_non_ptcl_lines_in_inp + 1
    elif flag_data_particles  == 1:
    
    
             if len(array_inp) < 12:
                 num_of_non_ptcl_lines_in_inp = num_of_non_ptcl_lines_in_inp + 1
                 if array_inp[0] == "_rlnMicrographName":
                     array_inp1 = re.split(r'#', array_inp[1])
                     col_no_rln_micName = int(array_inp1[1])
                 if array_inp[0] == "_rlnClassNumber":
                     array_inp1 = re.split(r'#', array_inp[1])
                     col_no_rln_clsNum = int(array_inp1[1])                 
                 if array_inp[0] == "_rlnCoordinateX":
                     array_inp1 = re.split(r'#', array_inp[1])
                     col_no_rln_coordX = int(array_inp1[1]) 
                 if array_inp[0] == "_rlnCoordinateY":
                     array_inp1 = re.split(r'#', array_inp[1])
                     col_no_rln_coordY = int(array_inp1[1]) 
                 if array_inp[0] == "_rlnAnglePsi":
                     array_inp1 = re.split(r'#', array_inp[1])
                     col_no_rln_angPsi = int(array_inp1[1])        
                 if array_inp[0] == "_rlnAnglePsiPrior":
                     array_inp1 = re.split(r'#', array_inp[1])
                     col_no_rln_angPsiPrior = int(array_inp1[1])                                    
                 if array_inp[0] == "_rlnAutopickFigureOfMerit":
                     array_inp1 = re.split(r'#', array_inp[1])
                     col_no_rln_autopickFom = int(array_inp1[1])
    else:
        num_of_ptcl_lines_in_inp = num_of_ptcl_lines_in_inp + 1
filehandle_inp_ptcls_star.close()
sys.stdout.flush()

print("max_col_num_in_inp                                   = "+str(max_col_num_in_inp)+ " ("+input_file_star+") ")     
print("_rlnMicrographName           column ID               = "+str(col_no_rln_micName)+" (will be used)")  
print("_rlnClassNumber              column ID               = "+str(col_no_rln_clsNum)+" (will be used)")          
print("_rlnCoordinateX              column ID               = "+str(col_no_rln_coordX)+" (will be used)")
print("_rlnCoordinateY              column ID               = "+str(col_no_rln_coordY)+" (will be used)")
print("_rlnAnglePsi                 column ID               = "+str(col_no_rln_angPsi)+" (will be used)")         
print("_rlnAnglePsiPrior            column ID               = "+str(col_no_rln_angPsiPrior)+" (will NOT be used)")  
print("_rlnAutopickFigureOfMerit    column ID               = "+str(col_no_rln_autopickFom)+" (will be used)")                           
print("***********************************************************************************************")
print("num_of_non_ptcl_lines_in_inp = "+str(num_of_non_ptcl_lines_in_inp))
print("num_of_ptcl_lines_in_inp     = "+str(num_of_ptcl_lines_in_inp))
print("***********************************************************************************************")

#### find and print
flag_data_particles             = 0
curr_ptcl_line_num             = 0

previous_micName           = "ppp"
micName                    = "ccc"

filehandle_inp_ptcls_star     = open(input_file_star,  "r")
while True:
    line_inp_ptcls_star = filehandle_inp_ptcls_star.readline()
    
    previous_micName = micName 
    
    if len(line_inp_ptcls_star) == 0:     ## In fact, blank lines are "\n".
        break
    line_inp_ptcls_star = line_inp_ptcls_star.rstrip('\n')         ## remove "\n" 
    line_inp_ptcls_star = line_inp_ptcls_star         ## sometimes data lines start from beginning; sometimes not.    
    array_inp_ptcls_star = re.split(r'\s+', line_inp_ptcls_star)  ## This command splits both string and spacing!!!

    
    if array_inp_ptcls_star[0] == "data_particles":
            flag_data_particles  = 1 
         
    if flag_data_particles  == 1:   
      if len(array_inp_ptcls_star) > 12:          
        curr_ptcl_line_num         = curr_ptcl_line_num          + 1
        sys.stdout.write("Working on particle #: %s \r" % (curr_ptcl_line_num ) )
        sys.stdout.flush()
        micName = array_inp_ptcls_star[col_no_rln_micName]
        clsNum = array_inp_ptcls_star[col_no_rln_clsNum]        
        coordX = array_inp_ptcls_star[col_no_rln_coordX]  
        coordY = array_inp_ptcls_star[col_no_rln_coordY]  
        angPsi = array_inp_ptcls_star[col_no_rln_angPsi]  
        autopickFom = array_inp_ptcls_star[col_no_rln_autopickFom]          
        
        path_micName = re.split(r'\/', micName)
        array_splitext_micName = os.path.splitext(path_micName[-1])
        path_output_file_star = output_star_dir+"/"+array_splitext_micName[0]+output_star_ext

        if not os.path.exists (path_output_file_star):
            filehandle_out_star = open(path_output_file_star, "a+")
            filehandle_out_star.write( "%s\n" % (""))
            filehandle_out_star.write( "%s\n" % ("data_"))
            filehandle_out_star.write( "%s\n" % (""))
            filehandle_out_star.write( "%s\n" % ("loop_ "))
            filehandle_out_star.write( "%s\n" % ("_rlnCoordinateX #1 "))
            filehandle_out_star.write( "%s\n" % ("_rlnCoordinateY #2 "))
            filehandle_out_star.write( "%s\n" % ("_rlnClassNumber #3 "))
            filehandle_out_star.write( "%s\n" % ("_rlnAnglePsi #4 "))
            filehandle_out_star.write( "%s\n" % ("_rlnAutopickFigureOfMerit #5 "))
            filehandle_out_star.close()
                        
        filehandle_out_star = open(path_output_file_star, "a+")
        #array_coordX_int= re.split(r'\.', coordX) 
        #array_coordY_int= re.split(r'\.', coordY)
        filehandle_out_star.write( "%13.6f%13.6f%13d%13f%13.6f\n" % (float(coordX)/binning_factor, float(coordY)/binning_factor, int(clsNum), float(angPsi), float(autopickFom) ))
        
        filehandle_out_star.close()
        
filehandle_inp_ptcls_star.close()     


########################################################################
# Closing more files

print("\n  DONE! Please check the output files! \n") 
print("***********************************************************************************************")

print('''
   Put both .mrc and _pick.star files in NEW_Relion_Proj_Dir/Micrographs before working on Fesp or Relion!

   To display the coordinates (XY), Psi angle and FOM in images in Fesp:
       (1) Go to the directory holding both .mrc and .star files; Launch Fesp. 
              In Fesp GUI: Open .mrc files; _pick.star and _ref files will be read and displayed automatically.
              The two text boxes right to 'Save Ptcls' can be used to change Psi and FOM manually.

   
   To display the coordinates in images in Relion (4 STEPS):
       (1) [OPTIONAL]Import Micrographs:
              Import => I/O: Input files: Micrographs/*.mrc;        Node type: 2D micrographs/tomographs
       (2) Save job settings for manual picking:
              Manual picking => I/O; Display: (ptcl diameter, scaling, pixel size); ; Colors => Jobs => Save job settings  
       (3) Import Coordinates:     
              Import => I/O: Input files: Micrographs/*_pick.star; Node type: 2D/3D particle coordinates
       (4) Display the coordinates on images:           
              Import => Display: out: coords_suffix_pick.star
   Now, you can add particles w/ left click, delete them w/ middle click, and edit the file w/ right click.\n''')
         
         
         
         
         
         
         
         
         
         
         
