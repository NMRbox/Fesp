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

if len(sys.argv) != 4:

  print(('''
  
  Usage:''',sys.argv[0],''' input_ptcls_star  output_ptcls_star  binning_factor
  Notes:
         input_ptcls_star   Input particles.star file. ALL the particles in all the images are in ONE .star file.
                            e.g., particles.star (after Clas2D or Class3D or Selection); 
         output_ptcls_star  Output particles.star file. ALL the particles in all the images are in ONE .star file.
                            e.g., pick_star_files                  
         binning_factor     Coordinate binning factor. >1: shrinking; =1: no change; <1: expanding
                            e.g., 2\n'''))

  sys.exit()
 
 
########################################################################
# I/O files

input_ptcls_star      = sys.argv[1]
output_ptcls_star     = sys.argv[2]
binning_factor        = float(sys.argv[3])



if not os.path.exists (input_ptcls_star):
    print(("#### input_star_file: "+input_ptcls_star+" does not exists."))
    exit (0)
   
if os.path.exists (output_ptcls_star):
    print(("#### output_box_dir: "+output_ptcls_star+" exists. It'll be deleted first and then created again."))    
    try:
        shutil.rmtree(output_ptcls_star) 
    except OSError:
        pass
    os.system("ls "+output_ptcls_star)
else:
    os.system("ls "+output_ptcls_star)
 
print("***********************************************************************************************")
print(("input file:  input particles.star from 2DC; ", input_ptcls_star))   
print(("output file:  output particles.star;        ", output_ptcls_star))                
print(("option:      binning factor (float);        ", binning_factor))
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
col_no_rln_autopickFom = 0

num_of_non_ptcl_lines_in_inp         = 0
num_of_ptcl_lines_in_inp           = 0   

#### get the column numbers
sys.stdout.write("Collecting statistics from : %s \r" % (input_ptcls_star ) )            
filehandle_inp_ptcls_star         = open(input_ptcls_star,  "r")
while True :
    line_inp = filehandle_inp_ptcls_star.readline()

    if len(line_inp) == 0:     ## In fact, blank lines are "\n".
        break
    line_inp = line_inp.rstrip('\n')         ## remove "\n" 
    array_inp = re.split(r'\s+', line_inp)
    
    if max_col_num_in_inp < len(array_inp):
        max_col_num_in_inp = len(array_inp)
    
    if array_inp[0] == "data_images" or array_inp[0] == "data_" or array_inp[0] == "data_particles":
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

print(("max_col_num_in_inp                                   = "+str(max_col_num_in_inp)+ " ("+input_ptcls_star+") "))     
print(("_rlnMicrographName           column ID               = "+str(col_no_rln_micName)+" (will NOT be used)"))  
print(("_rlnClassNumber              column ID               = "+str(col_no_rln_clsNum)+" (will NOT be used)"))          
print(("_rlnCoordinateX              column ID               = "+str(col_no_rln_coordX)+" (will be used)"))
print(("_rlnCoordinateY              column ID               = "+str(col_no_rln_coordY)+" (will be used)"))
print(("_rlnAnglePsi                 column ID               = "+str(col_no_rln_angPsi)+" (will NOT be used)"))         
print(("_rlnAnglePsiPrior            column ID               = "+str(col_no_rln_angPsiPrior)+" (will NOT be used)"))  
print(("_rlnAutopickFigureOfMerit    column ID               = "+str(col_no_rln_autopickFom)+" (will NOT be used)"))                           
print("***********************************************************************************************")
print(("num_of_non_ptcl_lines_in_inp = "+str(num_of_non_ptcl_lines_in_inp)))
print(("num_of_ptcl_lines_in_inp     = "+str(num_of_ptcl_lines_in_inp)))
print("***********************************************************************************************")

#### find and print
flag_data_particles             = 0
curr_ptcl_line_num             = 0


filehandle_inp_ptcls_star     = open(input_ptcls_star,  "r")
filehandle_out_ptcls_star     = open(output_ptcls_star,  "w")
while True:
    line_inp_ptcls_star = filehandle_inp_ptcls_star.readline()
    
    #previous_micName = micName 
    
    if len(line_inp_ptcls_star) == 0:     ## In fact, blank lines are "\n".
        break
    line_inp_ptcls_star = line_inp_ptcls_star.rstrip('\n')         ## remove "\n" 
    line_inp_ptcls_star = line_inp_ptcls_star         ## sometimes data lines start from beginning; sometimes not.    
    array_inp_ptcls_star = re.split(r'\s+', line_inp_ptcls_star)  ## This command splits both string and spacing!!!

    
    if array_inp_ptcls_star[0] == "data_images" or array_inp_ptcls_star[0] == "data_" or array_inp_ptcls_star[0] == "data_particles":
            flag_data_particles  = 1 
         
    if flag_data_particles  == 1 and len(array_inp_ptcls_star) > 12:          
        curr_ptcl_line_num         = curr_ptcl_line_num          + 1
        sys.stdout.write("Working on particle #: %s \r" % (curr_ptcl_line_num ) )
        sys.stdout.flush()
        micName = array_inp_ptcls_star[col_no_rln_micName]
        clsNum = array_inp_ptcls_star[col_no_rln_clsNum]        
        coordX = array_inp_ptcls_star[col_no_rln_coordX]  
        coordY = array_inp_ptcls_star[col_no_rln_coordY]  
        angPsi = array_inp_ptcls_star[col_no_rln_angPsi]  
        #autopickFom = array_inp_ptcls_star[col_no_rln_autopickFom]          
        #print "zzzzzzzzzzzzzz"
        for idx in range(len(array_inp_ptcls_star)):
           if   idx == col_no_rln_coordX :
                filehandle_out_ptcls_star.write( " %11.6f" % ( int(float(coordX)/binning_factor )) )
           elif idx == col_no_rln_coordY:
                filehandle_out_ptcls_star.write( " %11.6f" % ( int( float(coordY)/binning_factor )) )               
           else:
                filehandle_out_ptcls_star.write( " %s" % (array_inp_ptcls_star[idx]) )           
        filehandle_out_ptcls_star.write( "\n" % () )        
    else:
        filehandle_out_ptcls_star.write( "%s\n" % (line_inp_ptcls_star) )
        
        
filehandle_out_ptcls_star.close()     
filehandle_inp_ptcls_star.close() 

########################################################################
# Closing more files

print("\n  DONE! Please check the output files! \n") 
print("***********************************************************************************************")


         
         
         
         
         
         
         
         
         
         
         
