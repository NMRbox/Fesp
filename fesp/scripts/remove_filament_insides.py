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
Not available
'''

########################################################################
# Import modules

import sys, re, string, os, os.path, math, time, shutil
from datetime import datetime

########################################################################
# Usage

if len(sys.argv) != 8:

  print(('''
  
  Usage:''',sys.argv[0],''' input_star_dir  input_star_ext  output_star_dir  output_star_ext  distance_range  angle_range  binning_factor 
  Notes:
         input_star_dir   Input directory holding _xxxx.star files. ONE .star for each image.
                          e.g., xxxx_star_dir
         input_star_ext   Output star file extension.
                          e.g., _pick.star                                   
         output_star_dir  Output directory for all the _yyyy.star files. ONE .star for each image.
                          e.g., yyyy_star_dir
         output_star_ext  Output star file extension.
                          e.g., _pick.star                 
         distance_range   Distance range in pixels for detecting the two particles on the same filament, usu. 3x diamerter.
                          e.g., 100
         angle_range      Angle range in degrees for detecting the two particles on the same filament, usu. 10-20 degrees.
                          e.g., 15                    
         binning_factor   Coordinate binning factor. >1: shrinking; =1: no change; <1: expanding
                          e.g., 2
         
         Put both .mrc and _pick.star files in NEW_Relion_Proj_Dir/Micrographs before working on Fesp or Relion!
         
         To display the coordinates in images in Relion (4 STEPS):
             (1) [OPTIONAL]Import Micrographs:
                 Import => I/O: Input files: Micrographs/*.mrc;       Node type: 2D micrographs/tomographs
             (2) Save job settings for manual picking:
                 Manual picking => I/O; Display: (ptcl diameter, scaling, pixel size); ; Colors => Jobs => Save job settings  
             (3) Import Coordinates:         
                 Import => I/O: Input files: Micrographs/*_pick.star; Node type: 2D/3D particle coordinates
             (4) Display the coordinates on images:         
                 Import => Display: out: coords_suffix_pick.star
         Now, you can add particles w/ left click, delete them w/ middle click, and edit the file w/ right click.\n'''))

  sys.exit()
 
 
########################################################################
# I/O files

input_star_dir       = sys.argv[1]
input_star_ext       = sys.argv[2]
output_star_dir      = sys.argv[3]
output_star_ext      = sys.argv[4]
distance_range       = int(sys.argv[5])   
angle_range          = int(sys.argv[6]) 
binning_factor       = float(sys.argv[7])


if not os.path.exists (input_star_dir):
    print(("#### input_star_dir: "+input_star_dir+" does not exists."))
    exit (0)
num_of_inp_star_files = 0
for inp_file in os.listdir(input_star_dir):
    if inp_file.endswith(input_star_ext):
        num_of_inp_star_files = num_of_inp_star_files + 1
if num_of_inp_star_files == 0:
    print(("#### no _xxxx.star files were found in: "+input_star_dir))
    exit (0)  
  
if os.path.exists (output_star_dir):
    print(("#### output_box_dir: "+output_star_dir+" exists. It'll be deleted first and then created again."))    
    try:
        shutil.rmtree(output_star_dir) 
    except OSError:
        pass
    os.system("mkdir "+output_star_dir)
else:
    os.system("mkdir "+output_star_dir)
    
print("***********************************************************************************************")
print(("input dir:   input directory holding *_xxxx.star;    ", input_star_dir, " has ", num_of_inp_star_files, " files")) 
print(("inpput ext:  input .star file extension;             ", input_star_ext))
print(("output dir:  output directory holding *_yyyy.star;   ", output_star_dir))        
print(("output ext:  output .star file extension;            ", output_star_ext))        
print(("option:      distance range (integer);               ", distance_range))
print(("option:      angle range (integer);                  ", angle_range))
print(("option:      binning factor (float);                 ", binning_factor))
print("***********************************************************************************************")    

col_no_rln_micName     = 0 
col_no_rln_clsNum      = 0
col_no_rln_coordX      = 0
col_no_rln_coordY      = 0
col_no_rln_angPsi      = 0
col_no_rln_angPsiPrior = 0

num_of_ptcls_in_curr_mic = 0

num_of_detected_fil_insides_in_curr_mic = 0
num_of_detected_fil_insides_in_all_mics = 0

num_of_inp_star_files    = 0
curr_inp_star_file_num   = 0

num_of_non_ptcl_lines_in_inp         = 0
num_of_ptcl_lines_in_inp           = 0

max_col_num_in_inp = 0      

timestring = datetime.now().strftime("%Y%m%d_%H%M%S")
filehandle_out_log         = open("remove_filement_insides_"+timestring+".log",  "w")

for inp_file in os.listdir(input_star_dir):
    curr_inp_star_file_num = curr_inp_star_file_num + 1
    sys.stdout.write("Working on file #: %s \r" % (curr_inp_star_file_num) )
    sys.stdout.flush()
    
    num_of_detected_fil_insides_in_curr_mic = 0
    num_of_ptcls_in_curr_mic = 0
    ptclListInCurrMic2d = []
    
    if inp_file.endswith(input_star_ext):
      filehandle_inp_ptcls_star         = open(input_star_dir+"/"+inp_file,  "r")
      while True :
        line_inp = filehandle_inp_ptcls_star.readline()

        if len(line_inp) == 0:     ## In fact, blank lines are "\n".
            break
        line_inp = line_inp.rstrip('\n')     ## remove "\n" 
        array_inp = re.split(r'\s+', line_inp)
        
        if max_col_num_in_inp < len(array_inp):
            max_col_num_in_inp = len(array_inp)

        if len(array_inp) < 5:
            num_of_non_ptcl_lines_in_inp = num_of_non_ptcl_lines_in_inp + 1
            #if array_inp[0] == "_rlnMicrographName":
            #   array_inp1 = re.split(r'#', array_inp[1])
            #   col_no_rln_micName = int(array_inp1[1])        
            if array_inp[0] == "_rlnCoordinateX":
                array_inp1 = re.split(r'#', array_inp[1])
                col_no_rln_coordX = int(array_inp1[1]) 
            if array_inp[0] == "_rlnCoordinateY":
                array_inp1 = re.split(r'#', array_inp[1])
                col_no_rln_coordY = int(array_inp1[1]) 
            if array_inp[0] == "_rlnClassNumber":
                array_inp1 = re.split(r'#', array_inp[1])
                col_no_rln_clsNum = int(array_inp1[1])                  
            if array_inp[0] == "_rlnAnglePsi":
                array_inp1 = re.split(r'#', array_inp[1])
                col_no_rln_angPsi = int(array_inp1[1])                              
            if array_inp[0] == "_rlnAutopickFigureOfMerit":
                array_inp1 = re.split(r'#', array_inp[1])
                col_no_rln_autopickFom = int(array_inp1[1])
        else:
            num_of_ptcl_lines_in_inp = num_of_ptcl_lines_in_inp + 1
            num_of_ptcls_in_curr_mic = num_of_ptcls_in_curr_mic + 1

            micName = inp_file        
            coordX = array_inp[col_no_rln_coordX]  
            coordY = array_inp[col_no_rln_coordY]  
            clsNum = array_inp[col_no_rln_clsNum]         
            angPsi = array_inp[col_no_rln_angPsi]  
            autopickFom = array_inp [col_no_rln_autopickFom]  
            path_micName = re.split(r'\/', inp_file)
            array_splitext_micName = re.split(r'_fesp.star', path_micName[-1])
            array_splitext_micName = re.split(input_star_ext, path_micName[-1])            
            path_output_file_star = output_star_dir+"/"+array_splitext_micName[0]+output_star_ext
            
            ptclListInCurrMic2d.append([]) # add a row
            ptclListInCurrMic2d[num_of_ptcls_in_curr_mic - 1].append(coordX) #
            ptclListInCurrMic2d[num_of_ptcls_in_curr_mic - 1].append(coordY) #
            ptclListInCurrMic2d[num_of_ptcls_in_curr_mic - 1].append(clsNum) #
            ptclListInCurrMic2d[num_of_ptcls_in_curr_mic - 1].append(angPsi) #
            ptclListInCurrMic2d[num_of_ptcls_in_curr_mic - 1].append(autopickFom) # 
            
      for centerIdx in range (num_of_ptcls_in_curr_mic):
         isInside = 0
         centerCoordX = float(ptclListInCurrMic2d[centerIdx - 1][0])
         centerCoordY = float(ptclListInCurrMic2d[centerIdx - 1][1])
         centerClsNum = int(ptclListInCurrMic2d[centerIdx - 1][2])
         centerAngPsi = float(ptclListInCurrMic2d[centerIdx - 1][3])
         centerAutopickFom = float(ptclListInCurrMic2d[centerIdx - 1][4])
                           
         for touchIdx in range (num_of_ptcls_in_curr_mic):            
            if touchIdx != centerIdx:
                touchCoordX = float(ptclListInCurrMic2d[touchIdx - 1][0])
                touchCoordY = float(ptclListInCurrMic2d[touchIdx - 1][1])
                touchClsNum = int(ptclListInCurrMic2d[touchIdx - 1][2])
                touchAngPsi = float(ptclListInCurrMic2d[touchIdx - 1][3])
                touchAutopickFom = float(ptclListInCurrMic2d[touchIdx - 1][4])
                                                            
                deltaX = touchCoordX-centerCoordX
                deltaY = touchCoordY-centerCoordY
                #psi = math.degrees( math.atan2( deltaY, deltaX ) )
                psi = -math.degrees( math.atan2( -deltaY, -deltaX ) )                
                dist = math.sqrt( deltaX*deltaX + deltaY*deltaY )
                
                if ( abs(psi - centerAngPsi ) < angle_range or abs(psi - centerAngPsi + 360) < angle_range or abs(psi - centerAngPsi - 360) < angle_range )    \
                    and ( abs(psi - touchAngPsi ) < angle_range or abs(psi - touchAngPsi + 360) < angle_range or abs(psi - touchAngPsi - 360) < angle_range  ) \
                    and dist < distance_range:
                    isInside = 1
                    num_of_detected_fil_insides_in_curr_mic = num_of_detected_fil_insides_in_curr_mic + 1
                    filehandle_out_log.write( "     %s  %d  %s%s,%s%s %f %f %f %f\n" % (micName, num_of_detected_fil_insides_in_curr_mic, " (", str(centerCoordX), str(centerCoordY), ") ", psi, centerAngPsi, touchAngPsi, dist) )
        
         if  not os.path.exists (path_output_file_star):
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
         if isInside == 0: 
                    filehandle_out_star = open(path_output_file_star, "a+")
                    filehandle_out_star.write( "%13.6f%13.6f%13d%13f%13.6f\n" % (float(centerCoordX)/binning_factor, float(centerCoordY)/binning_factor, int(centerClsNum), float(centerAngPsi), float(centerAutopickFom) ))
                    filehandle_out_star.close()
         #if isInside == 1:                                   
             #       filehandle_out_star = open(path_output_file_star, "a+")
             #       filehandle_out_star.write( "%13.6f%13.6f%13d%13f%13.6f\n" % (float(centerCoordX)/binning_factor, float(centerCoordY)/binning_factor, int(centerClsNum), float(centerAngPsi), 0.0 ))
             #       filehandle_out_star.close()                
      filehandle_out_log.write( "#### %s  %d\n" % (micName, num_of_detected_fil_insides_in_curr_mic ))
            
      filehandle_inp_ptcls_star.close()

filehandle_out_log.close()

print(("max_col_num_in_inp                                   = "+str(max_col_num_in_inp)+ " ("+input_star_dir+") "))      
print(("_rlnClassNumber              column ID               = "+str(col_no_rln_clsNum)))           
print(("_rlnCoordinateX              column ID               = "+str(col_no_rln_coordX))) 
print(("_rlnCoordinateY              column ID               = "+str(col_no_rln_coordY))) 
print(("_rlnAnglePsi                 column ID               = "+str(col_no_rln_angPsi)))  
print(("_rlnAutopickFigureOfMerit    column ID               = "+str(col_no_rln_autopickFom)))               
print("***********************************************************************************************")
print(("num_of_non_ptcl_lines_in_inp = "+str(num_of_non_ptcl_lines_in_inp)))
print(("num_of_ptcl_lines_in_inp     = "+str(num_of_ptcl_lines_in_inp)))
print("***********************************************************************************************")


########################################################################
# Closing more files

print("\n  DONE! Please check the output files! \n") 
print("***********************************************************************************************")

print('''
   The output .star files can be displayed in Fesp or Relion.
   
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
         
