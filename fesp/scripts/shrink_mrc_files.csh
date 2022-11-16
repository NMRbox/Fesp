#!/bin/csh -f

if ($#argv != 3) then
        echo " "
        echo "  Shrink/bin the images in .mrc format."
        echo "  Make sure that you have set the environment variables for EMAN2,"
        echo "  i.e., 'e2proc2d.py' is in your search path ('which e2proc2d.py')."		
        echo " "		
	echo "  Usage: $0  input_file_dir  output_file_dir  binning_factor"
	echo "  Notes:  "
	echo "         input_file_dir     Input directory holding unshrinked micrographs in .mrc format." 
	echo "         output_file_dir    Output directory. Should be a directory inside CWD." 	
        echo "         binning_factor     Binning factor: 2 or 4                   " 			
        echo " " 
        echo "  The output micrographs will be shrinked by a factor of 2 or 4."
        echo "  Input Files:      input_file_dir/abc_001.mrc"
        echo "  Output Files:    output_file_dir/abc_001.mrc		      "
        echo " "		
	exit;
endif

set input_file_dir   = $1
set output_file_dir  = $2
set binning_factor   = $3

if (-d $output_file_dir) then
  echo "Output directory exists. Please delete it first! " $output_file_dir
  exit
endif

mkdir $output_file_dir

foreach f ( $input_file_dir/*.mrc )
   echo "#### Shrinking micrograph: " $f
   #proc2d $f `basename $f .mrc`_s${binning_factor}.mrc shrink=${binning_factor} norm
   #e2proc2d.py $f `basename $f .mrc`_s${binning_factor}.mrc --meanshrink=${binning_factor} --process=normalize.edgemean 
   e2proc2d.py  $f  ${output_file_dir}/`basename $f .mrc`.mrc --meanshrink=${binning_factor} --process=normalize.edgemean   
end

echo "///////////////////////////////////////////////////////////////////////////////////////"
echo "DONE!"
echo "  "	   		
echo "  ls  ${output_file_dir}/*.mrc "
