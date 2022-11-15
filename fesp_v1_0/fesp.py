#!/usr/bin/python
#
# Contact: Steven Chou (stevenzchou@gmail.com)
#
#

from sys import argv

import os
import re
import struct
import wx
from PIL import Image
from numpy import *

#from PIL import Image

######## FespSetttings.txt ######## each variable ends with an S (Setting)
workingDirS = "."  # string
windowWidthS = 1200  # integer; start window width in pixels
windowHeightS = 800  # integer; start window height in pixels
pickPtclSizeS = 60  # integer
refPtclSizeS = 48  # integer
magS = 1.0  # float
sigmaChoiceS = 5  # integer; 1-9 correspond to [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]
invertContrastS = 1  # integer; 1: invert; others: don't invert
displayBoxS = 1  # integer; 1: display; others: hide
displayPsiS = 1  # integer; 1: display; others: hide
psiNeedleRatioS = 1.0  # float: psiNeedleRatio = distanceOfEndPointFromCenter/pickPtclSize; usually 1.0
defaultPsiS = 0  # float; range: [-180,180]; 0: 3 o'clock
defaultFomS = 0  # float;
fomGreenS = 5  # float; threshold for coloring particles in green
fomYellowS = 4  # float; threshold for coloring particles in yellow
fomOrangeS = 3  # float; threshold for coloring particles in orange
fomMagentaS = 2  # float; threshold for coloring particles in magenta
fomRedS = 1  # float; threshold for coloring particles in red
fomCyanS = 0  # float; threshold for coloring particles in cyan
fomWhiteS = -999  # float; threshold for coloring particles in white
eraserRadiusS = 50  # integer;
fespSettingsTxt = ""
if os.path.exists("~/FespSettings.txt"):
    fespSettingsTxt = "~/FespSettings.txt"
if os.path.exists("./FespSettings.txt"):  # in priority
    fespSettingsTxt = "./FespSettings.txt"
if fespSettingsTxt != "":
    filehandle_inp_fesp_settings_file = open(fespSettingsTxt, "r")
    while True:
        line_setting = filehandle_inp_fesp_settings_file.readline()
        if len(line_setting) == 0:
            break  ## In fact, blank lines are "\n".
    line_setting = line_setting.rstrip('\n')  ## remove "\n"
    if line_setting.startswith("_") and "=" in line_setting:
        array_setting_splitEqual = re.split(r'=', line_setting)
        if array_setting_splitEqual[0].strip() == "_workingDir":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            workingDirS = str(array_setting_splitPound[0].strip())
            if not os.path.exists(workingDirS):
                print("Working directory doesn't exit")
                sys.exit(1)
        if array_setting_splitEqual[0].strip() == "_windowWidth":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            windowWidthS = int(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_windowHeight":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            windowHeightS = int(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_pickPtclSize":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            pickPtclSizeS = int(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_refPtclSize":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            refPtclSizeS = int(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_mag":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            magS = float(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_sigmaChoice":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            sigmaChoiceS = int(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_invertContrast":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            invertContrastS = float(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_displayBox":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            displayBoxS = int(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_displayPsi":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            displayPsiS = int(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_psiNeedleRatio":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            psiNeedleRatioS = float(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_defaultPsi":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            defaultPsiS = int(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_defaultFom":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            defaultFomS = int(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_fomGreen":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            fomGreenS = float(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_fomYellow":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            fomYellowS = float(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_fomOrange":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            formOrange = float(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_fomMagenta":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            fomMagentaS = float(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_fomRed":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            fomRedS = float(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_fomCyan":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            fomCyanS = float(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_fomWhite":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            fomWhiteS = float(array_setting_splitPound[0].strip())
        if array_setting_splitEqual[0].strip() == "_eraserRadius":
            array_setting_splitPound = re.split(r'#', array_setting_splitEqual[1])
            eraserRadiusS = int(array_setting_splitPound[0].strip())
    filehandle_inp_fesp_settings_file.close()
"""
print "================================================"
print "%s%s  "   %  ("_wrokingDir     = ", workingDirS    )
print "%s%s  "   %  ("_pickPtclSize   = ", pickPtclSizeS  )
print "%s%s  "   %  ("_refPtclSize    = ", refPtclSizeS   )
print "%s%s  "   %  ("_mag            = ", magS           )
print "%s%s  "   %  ("_sigmaChoice    = ", sigmaChoiceS   )
print "%s%s  "   %  ("_invertContrast = ", invertContrastS)
print "%s%s  "   %  ("_displayBox     = ", displayBoxS  )
print "%s%s  "   %  ("_displayPsi     = ", displayPsiS    )
print "%s%s  "   %  ("_psiNeedleRatio = ", psiNeedleRatioS)
print "%s%s  "   %  ("_defaultPsi     = ", defaultPsiS    )
print "%s%s  "   %  ("_defaultFom     = ", defaultFomS    )
print "%s%s  "   %  ("_fomGreen       = ", fomGreenS      )
print "%s%s  "   %  ("_fomYellow      = ", fomYellowS     )
print "%s%s  "   %  ("_fomOrange      = ", fomOrangeS     )
print "%s%s  "   %  ("_fomMagenta     = ", fomMagentaS    )
print "%s%s  "   %  ("_fomRed         = ", fomRedS        )
print "%s%s  "   %  ("_fomCyan        = ", fomCyanS        )
print "%s%s  "   %  ("_fomWhite       = ", fomWhiteS      )
print "%s%s  "   %  ("_eraserRadius   = ", eraserRadiusS  )
print "================================================"	
"""


class ImageFunctions:  ######## Class 1: ImageFunctions ########
    def Brightness(self, img, factor):  # factor [-1,1]: 0: original pix; 1: all 255; -1: all 0
        pass

    #	im_auto = Contrast(img,-1,-1)		# factor positive: increase brightness, and vice versa
    #	factor_abs = abs(factor)
    #	a = 1 - factor_abs
    #	if factor >= 0:
    #		b = 255 * factor_abs
    #		return im_auto.point(lambda i: i * a + b)
    #	else:
    #		return im_auto.point(lambda i: i * a)

    def Contrast(self, img, pix_min, pix_max, brightness):
        if pix_min == pix_max:
            return img

        a = 255 / (pix_max - pix_min)
        mini = pix_min * (-a) + brightness
        return img.point(lambda i: i * a + mini)

    def ContrastSigma(self, img, stat, sigma):
        if stat[3] > stat[4]:
            return img
        # Contrast by sigma multiplier (e.g. 3), no brightness adjustment
        setmin = stat[0] - stat[1] * sigma
        setmax = stat[0] + stat[1] * sigma
        return self.Contrast(img, setmin, setmax, 0)

    def CountFrame(self, img):  # Count how many images inside one stack file
        try:
            nimages = img.nimages
            return nimages
        except:
            goon = True
            i = 0
            try:
                while goon:
                    img.seek(i)
                    i += 1
            except EOFError:
                return i

    def CutPartNormal(self, img, xylist, boxSize):
        regionnormallist = []
        regionlist = self.CutPart(img, xylist, boxSize)
        for region in regionlist:
            stat = self.StatCal(region)
            regionnormallist.append(self.ContrastSigma(region, stat, 3))
        return regionnormallist

    def CutPart(self, img, xylist, boxSize):
        regionlist = []
        rad = int(boxSize / 2.0)
        for xy in xylist:
            box = (xy[0] - rad, xy[1] - rad, xy[0] + rad, xy[1] + rad)
            region = img.crop(box)
            regionlist.append(region)
        return regionlist

    def ImgToBmp(self, img):
        if wx.__version__.startswith("3"):
            image = wx.EmptyImage(img.size[0], img.size[1])  # wxPython 3.0
        elif wx.__version__.startswith("4"):
            image = wx.Image(img.size[0], img.size[1])  # wxPython 4.0
        image.SetData(img.convert('RGB').tostring())
        bmp = image.ConvertToBitmap()
        return bmp

    def InvertContrast(self, img, stat):
        if stat[3] > stat[4]:
            return img
        a = -1.0
        b = stat[0] * 2
        img_invert = img.point(lambda i: i * a + b)
        return img_invert

    def Resize(self, img, newsizex, newsizey):
        sizex, sizey = img.size
        if newsizex < sizex or newsizey < sizey:
            return img.resize((newsizex, newsizey), Image.ANTIALIAS)
        else:
            return img.resize((newsizex, newsizey), Image.BICUBIC)

    def ResizeToBmp(self, img, newsizex, newsizey):
        sizex, sizey = img.size
        if newsizex < sizex or newsizey < sizey:  # Downsampling using PIL
            newimg = img.resize((newsizex, newsizey), Image.ANTIALIAS)
        else:  # Upsampling
            newimg = img.resize((newsizex, newsizey), Image.BICUBIC)
        return self.ImgToBmp(newimg)

    def ShiftImg(self, img, shx, shy):  # Shift an image by x-y integer numbers
        imgsh = img.copy()
        xsize, ysize = imgsh.size
        nparray = array(imgsh.getdata()).reshape(ysize, xsize)
        if shx != 0:
            if shx < 0:
                shx = xsize + shx
            nparray = hstack((nparray[:, (xsize - shx):], nparray[:, :(xsize - shx)]))
        if shy != 0:
            if shy < 0:
                shy = ysize + shy
            nparray = vstack((nparray[(ysize - shy):, :], nparray[:(ysize - shy), :]))
        imgsh.putdata(nparray.ravel())
        return imgsh

    def Stat(self, filename):  # Get stat first by looking at the SPIDER header, if not found calculate them
        hlist = self.SpiHeader(filename)
        if len(hlist) > 0:
            hdlist = (99,) + hlist
            if hdlist[6] == 1:  # IMAMI = 1, if stat was there
                std = hdlist[10]  # somtimes std is -1
                if std > 0:
                    avg = hdlist[9]
                    sumlist = avg * hdlist[2] * hdlist[12]
                    imgmin = hdlist[8]
                    imgmax = hdlist[7]
                    stat = [avg, std, sumlist, imgmin, imgmax]
                    return stat
        img = Image.open(filename)
        return self.StatCal(img)

    def StatCal(self, img):  # Calculate the stat using numpy array
        try:  # If color image: pixel value is a tuple, not a number
            float(img.getpixel((0, 0)))
        except TypeError:
            return [1, 1, 1, 1, -1]  # Mock values. stat[3](min) > stat[4](max) means 'color'
        newsize = 512
        sizex, sizey = img.size
        if sizex > newsize and sizey > newsize:
            imgs = img.copy()
            imgs.thumbnail((newsize, newsize))
            npa = array(imgs.getdata())
        else:
            npa = array(img.getdata())
        imgmin, imgmax = img.getextrema()
        return [average(npa), npa.std(), 0, imgmin, imgmax]  # [avg, std, dummy value, imgmin, imgmax]

    def SpiHeader(self, spiderfile):  # Get spider header records 1-30
        hlist = []
        minsize = 30 * 4
        if os.path.getsize(spiderfile) < minsize:
            return hlist

        f = open(spiderfile, 'rb')  # Open in binary mode
        fh = f.read(minsize)
        f.close()
        endtype = 'BIG'
        hlist = struct.unpack('>30f', fh)  # Try big_endian first
        validheader = self.SpiTestIform(hlist)
        if not validheader:
            endtype = 'SMALL'
            hlist = struct.unpack('<30f', fh)  # Use small_endian first
            validheader = self.SpiTestIform(hlist)
        if not validheader:
            hlist = []
        return hlist

    def SpiTestIform(self, hlist):  # Test if the list looks like a SPIDER header
        try:
            for item in hlist:
                int(item)
        except ValueError:
            return False
        h = (99,) + hlist  # Add one item, so index start=1
        valid = True
        for item in [1, 2, 5, 12, 13, 22, 23]:  # All these should be intergers
            if h[item] != int(h[item]):
                valid = False
        if int(h[23]) != int(h[13]) * int(h[22]):  # LENBYT = LABREC * LABBYT
            valid = False
        return valid


imageFunctions = ImageFunctions()


class ImageFile:  ######## Class 2: ImageFile ########
    def __init__(self, path):
        self.path = path
        self.img = Image.new('F', (0, 0), None)  # initiate with a mock image
        self.preSize = [0, 0]  # [for record only] Image size before loading (if different, > sizex/y_ori)
        self.preExtrema = [0, 0]  # [for record only] Image min,max before loading

        self.img_invert = Image.new('F', (0, 0), None)  # inverted version
        self.thumbnail = Image.new('F', (0, 0), None)  # thumbnail version
        self.refCoordSource = ""  # reference coordinate source
        self.edtCoordSource = ""  # editable coordinate source

        self.sizex_ori, self.sizey_ori = self.img.size
        self.stat = []  # calculated when the image is loaded
        self.stat_invert = []  # stat for inverted image
        self.xysmcList = []  # particle coordinates (SVCO_*.dat)
        self.xysmcListRef = []  # ref. particle coordinates (not modifiable) # (ref/SVCO_*.dat)
        self.displayPsi = displayPsiS  # flag for displaying psi. 0: hide; 1: display
        self.displayBox = 1  # flag for displaying particle paint. 0: hide; 1: display

    def DispXysmcList(self, factor, boxSize):  # factor is (displayed image size / original image size)
        dispXysmcList = []
        for item in self.xysmcList:
            newx = int(item[0] * factor)
            newy = int(item[1] * factor)
            news = float(item[2])  # psi
            newm = float(item[3])  # fom
            rad = int(boxSize * factor / 2.0)
            newsize = rad * 2
            dispXysmcList.append([newx - rad, newy - rad, newsize, news, newm])
        return dispXysmcList

    def DispXysmcListRef(self, factor, boxSize):  # factor is (displayed image size / original image size)
        dispXysmcListRef = []
        for item in self.xysmcListRef:
            newx = int(item[0] * factor)
            newy = int(item[1] * factor)
            news = float(item[2])  # psi
            newm = float(item[3])  # fom

            rad = int(boxSize * factor / 2.0)
            newsize = rad * 2
            dispXysmcListRef.append([newx - rad, newy - rad, newsize, news, newm])
        return dispXysmcListRef

    def InvertContrast(self):
        self.img_invert = imageFunctions.InvertContrast(self.img, self.stat)
        self.stat_invert = imageFunctions.StatCal(self.img_invert)


class Fesp(wx.Frame):  ######## Class 3: Fesp ########
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(windowWidthS, windowHeightS))
        self.cwd = os.getcwd()

        #### Program Introduction
        self.introductionShow = True
        self.introductionText = [ \
            """
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
      1864.000000  1672.000000	   8 	107.123456     3.253871  """]
        self.introductionTextBackup = self.introductionText

        introductionLength = len(self.introductionText)
        self.introductionCoord = []
        for item in range(introductionLength):
            self.introductionCoord.append((40, item * 20 + 20))

        #### Status Bar
        self.statusBar = self.CreateStatusBar(3)
        self.statusBar.SetStatusWidths([-3, -1, -3])

        #### Menu Bar
        menuBar = wx.MenuBar()
        menuFile = wx.Menu()
        menuFile.Append(11, 'Open .mrc files', 'Open one or multiple .mrc files')
        menuFile.Append(12, 'Close .mrc files', 'Close all the .mrc files')
        menuFile.Append(13, 'Save .star files', 'Save a .star file for each loaded .mrc file')
        menuFile.AppendSeparator()
        menuFile.Append(14, '&Exit', 'Exit the program')
        menuBar.Append(menuFile, '&File')
        menuHelp = wx.Menu()
        menuHelp.Append(22, 'Prepare .mrc files', 'Using the script shrink_mrc_files.csh')
        menuHelp.Append(23, 'Prepare _pick.star files', 'Using the script convert_star_files.py')
        menuHelp.Append(24, 'Prepare _ref.star files', 'Using the script convert_star_files.py')
        menuHelp.Append(25, 'Use _fesp.star files', 'Using the script scale_star_files.py')
        menuHelp.AppendSeparator()
        menuHelp.Append(26, 'Introduction', 'First introduction')
        menuHelp.Append(27, 'Usages', 'Brief usage')
        menuHelp.AppendSeparator()
        menuHelp.Append(28, '&About')
        menuBar.Append(menuHelp, '&Help')
        self.SetMenuBar(menuBar)

        #### Main Panel
        self.mainPanel = wx.Panel(self, -1)  # Intialize Fesp MainPanel
        self.StartFesp()

    def StartFesp(self):
        self.mainPanel = FespMainPanel(self, -1)  # Load Fesp MainPanel

        self.Bind(wx.EVT_MENU, self.mainPanel.OnMenuFileOpen, id=11)
        self.Bind(wx.EVT_MENU, self.mainPanel.OnMenuFileCloseAll, id=12)
        self.Bind(wx.EVT_MENU, self.mainPanel.OnMenuFileSaveAllCoordinates, id=13)
        self.Bind(wx.EVT_MENU, self.OnMenuFileExit, id=14)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpPrepareMrc, id=22)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpPreparePickStar, id=23)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpPrepareRefStar, id=24)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpUseFespStar, id=25)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpIntroduction, id=26)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpUsages, id=27)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpAbout, id=28)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetTitle('Fesp: Filament End and Single Particle Picker, v1.0')
        self.Layout()

        # read .mrc/.star files from command line
        if (len(argv) >= 1):
            paths_checked = []
            for item in argv:
                if item.endswith(".mrc"):
                    paths_checked.append(os.path.abspath(item))
            self.mainPanel.OpenFiles(paths_checked)

    def OnMenuFileExit(self, event):
        self.Close()

    def OnMenuHelpPrepareMrc(self, event):
        self.introductionText = """
How to prepare .mrc files? The script "shrink_mrc_files.csh" might be helpful. 

Usage: shrink_mrc_files.csh  input_file_dir  output_file_dir  binning_factor
Notes:  
       input_file_dir	Input directory holding unshrinked micrographs in .mrc format.
       output_file_dir  Output directory. Should be a directory inside CWD.
       binning_factor	Binning factor: 2 or 4. """
        self.StartFesp()

    def OnMenuHelpPreparePickStar(self, event):
        self.introductionText = """
How to prepare _pick.star files? The script "convert_star_files.py" might be helpful. 

Usage: convert_star_files.py  input_star_file  output_star_dir  output_star_ext  binning_factor
Notes:
       input_star_file  Input .star file. _rlnAnglePsi will be read.
                        ALL the particles in all the images are in ONE .star file.
                e.g., particles.star (after Class2D or Class3D or Selection); 
       output_star_dir  Output directory for all the .star files. 
                        ONE .star for each image.
                e.g., pick_star_files
       output_star_ext  Output star file extension.
                        This only changes the extension of output star files, not the contents.
                e.g., _pick.star  or  _ref.star 		
       binning_factor	Binning factor for the coordinates. 
                        >1: shrinking; =1: no change; <1: expanding
                e.g., 2 """
        self.StartFesp()

    def OnMenuHelpPrepareRefStar(self, event):
        self.introductionText = """
How to prepare _ref.star files? The script "convert_star_files.py" might be helpful. 

The procedure is the same as that for preparing _pick.star files.
The contents of _pick.star files and _ref.star files can be the same.
The _ref.star files are absolutely optional."""
        self.StartFesp()

    def OnMenuHelpUseFespStar(self, event):
        self.introductionText = """
How to use _fest.star files? The script "scale_star_files.py" might be helpful.

Usage: scale_star_files.py  input_star_dir  output_star_dir  output_star_ext  binning_factor
Notes:
       input_star_dir	Input directory holding _fesp.star files.ONE .star for each image.
                e.g., fesp_star_dir
       output_star_dir  Output directory for all the .star files. ONE .star for each image.
                e.g., pick_star_dir
       output_star_ext  Output star file extension.
                e.g., _pick.star		
       binning_factor	Coordinate binning factor. >1: shrinking; =1: no change; <1: expanding
                e.g., 2

Import _pick.star files into Relion for particle extraction. """
        self.StartFesp()

    def OnMenuHelpIntroduction(self, event):
        self.introductionText = self.introductionTextBackup
        self.StartFesp()

    def OnMenuHelpUsages(self, event):
        self.introductionText = """
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
    Left click, then hold 'Alt' or 'Cmd' and right click around (not on) the particle.
[*] Estimate psi: 
    Use the text box on the right side of the 'Psi' button.
[*] Change the box color (FOM): 
    Use the right most text box.
    [>=5: green; >=4 yellow; >=3: orange; >=2: magenta >=1: red; >=0: cyan; others: white]
[*] Read initial settings: 
    Put 'FespSettings.txt' in your working directory (in priority) or home directory."""
        self.StartFesp()

    def OnMenuHelpAbout(self, event):
        dlgtext = """
Fesp: Filament End and Single Particle Picker, v1.0
(Contact: Steven Chou, stevenzchou@gmail.com)
"""
        dlg = wx.MessageDialog(self, dlgtext, 'About Fesp',
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def RefreshMainPanel(self, mode):  # almost the same as StarFesp()
        self.mainPanel.Destroy()  # if uncommented, after you close a mic and load a new one, you'll get a RuntimeError
        self.mainPanel = FespMainPanel(self, -1)  # Load Fesp MainPanel

        self.Bind(wx.EVT_MENU, self.mainPanel.OnMenuFileOpen, id=11)
        self.Bind(wx.EVT_MENU, self.mainPanel.OnMenuFileCloseAll, id=12)
        self.Bind(wx.EVT_MENU, self.mainPanel.OnMenuFileSaveAllCoordinates, id=13)
        self.Bind(wx.EVT_MENU, self.OnMenuFileExit, id=14)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpPrepareMrc, id=22)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpPreparePickStar, id=23)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpPrepareRefStar, id=24)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpUseFespStar, id=25)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpIntroduction, id=26)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpUsages, id=27)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpAbout, id=28)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def ClearStatusBar(self):
        for item in range(3):
            self.statusBar.SetStatusText('', item)


class FespMainPanel(wx.Panel):  ######## Class 4: Fesp Main Panel ######## MenuBar not included
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        #### Initial Values
        self.imageFiles = []
        self.openFirstFile = True
        self.particleList = []
        self.sigmaLevel = 3
        self.boxSize_ref = refPtclSizeS  # initial box size for reference coordinates
        self.boxSize = pickPtclSizeS
        self.cursorDraw = False  # Draw a circle attached to cursor # when rad>1, ctrl is pressed, and mouse motion

        self.invertMarker = 1
        self.pickedRectID = -1  # Selected particles in the montage

        self.particleFreePos = False  # Free docking of montage in particle panel # ON when montage is moved (right move), OFF when mag is changed (wheeler)
        self.particleDraw_x = 0
        self.particleDraw_y = 0
        self.particleMag = 1  # Side panel (Particle) mag

        #### Layout Setup
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panelT = FespPanelT(self, -1)  # Toolbar panel
        sizer.Add(self.panelT, 0, wx.EXPAND | wx.BOTTOM, 5)
        self.splitter = wx.SplitterWindow(self, -1, style=wx.BORDER_SUNKEN)
        self.panelP = FespPanelP(self.splitter, -1)  # Particle panel
        self.panelP.SetBackgroundColour(wx.BLACK)
        self.panelM = FespPanelM(self.splitter, -1)  # Micrograph panel
        self.panelM.SetBackgroundColour(wx.BLACK)
        self.splitter.SetMinimumPaneSize(5)
        self.splitter.SplitVertically(self.panelP, self.panelM, 250)
        sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.panelM.Bind(wx.EVT_PAINT, self.OnPaintM)
        self.panelM.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDownM)
        self.panelM.Bind(wx.EVT_LEFT_UP, self.OnLeftUpM)
        self.panelM.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDownM)
        self.panelM.Bind(wx.EVT_RIGHT_UP, self.OnRightUpM)  # right up 1
        self.panelM.Bind(wx.EVT_RIGHT_UP, self.OnRightUpPsiM)  # right up 2
        self.panelM.Bind(wx.EVT_MOTION, self.OnMotionM)
        self.panelM.Bind(wx.EVT_MOUSEWHEEL, self.OnWheelM)
        self.panelM.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUpM)  # works
        self.panelM.Bind(wx.EVT_KEY_UP, self.OnKeyUpM, id=60)  # key release ; for inverting the contrast

        self.panelP.Bind(wx.EVT_PAINT, self.OnPaintP)
        self.panelP.Bind(wx.EVT_LEFT_UP, self.OnLeftUpP)
        self.panelP.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDownP)
        self.panelP.Bind(wx.EVT_RIGHT_UP, self.OnRightUpP)
        self.panelP.Bind(wx.EVT_MOTION, self.OnMotionP)
        self.panelP.Bind(wx.EVT_MOUSEWHEEL, self.OnWheelP)
        self.panelP.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDclickP)
        self.panelP.Bind(wx.EVT_KEY_UP, self.OnKeyUpP)  # key release ; for navigating the particles (page up and down)
#gcw        self.GetParent().statusBar.SetStatusText('Happy Particle Picking, %s!' % os.getlogin(), 2)

        ######## PanelT Events ######## Toolbar Panel

    def OnMenuFileOpen(self, event):
        if len(self.imageFiles) == 0:
            self.openFirstFile = True
        paths = []
        dlg = wx.FileDialog(self, 'Open one or more micrographs in .mrc format', workingDirS, '', '*',
                            wx.FD_OPEN | wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        dlg.Destroy()
        if len(paths) == 0:
            return
        self.GetParent().cwd = os.path.dirname(paths[0])

        # check for duplication
        paths_checked = []
        for path in paths:
            i = 0
            goon = True
            while goon and i < len(self.imageFiles):
                if path == self.imageFiles[i].path:
                    goon = False
                i += 1
            if goon:
                paths_checked.append(path)
        self.OpenFiles(paths_checked)

    def OpenFiles(self, paths_checked):
        for path in paths_checked:  # Read image files and coordinate files
            try:
                img = Image.open(
                    path)  # Module Image imported from PIL can determine the image type based on file extension (.mrc)
                imagefile = ImageFile(path)  # Class constructed
                imagefile.img = img
                self.imageFiles.append(imagefile)

                basename = os.path.splitext(os.path.basename(path))
                refcoorf = os.path.dirname(path) + '/' + basename[
                    0] + '_ref.star'  # Load ref coordinate file, if present
                if os.path.exists(refcoorf):
                    imagefile.refCoordSource = "ref"
                    imagefile.xysmcListRef = self.LoadCoord(refcoorf)

                fespcoorf = os.path.dirname(path) + '/' + basename[
                    0] + '_fesp.star'  # Load fesp coordinate file, if present
                pickcoorf = os.path.dirname(path) + '/' + basename[
                    0] + '_pick.star'  # Load pick coordinate file, if present
                if os.path.exists(fespcoorf):
                    imagefile.edtCoordSource = "fesp"
                    imagefile.xysmcList = self.LoadCoord(fespcoorf)
                elif os.path.exists(pickcoorf):
                    imagefile.edtCoordSource = "pick"
                    imagefile.xysmcList = self.LoadCoord(pickcoorf)
                item = '[%d] %s [%d %s](%d %s)' % (
                len(self.imageFiles), os.path.basename(path), len(imagefile.xysmcListRef), imagefile.refCoordSource,
                len(imagefile.xysmcList), imagefile.edtCoordSource)
                self.comboFiles.Append(item)
            except IOError:
                print('Can NOT open ', path)

        if self.openFirstFile:  # if first time open, auto load the 1st image
            if len(self.imageFiles) > 0:
                self.currFile = 0
                self.comboFiles.SetSelection(0)
                self.currImageFile = self.imageFiles[0]  # set the first image (self.imageFiles[0]) to the currImageFile
                self.LoadImage()

    def LoadCoord(self, coorf):  # This funciton is also used in other places
        self.currImageFile = self.imageFiles[
            0]  # assuming all the images have the same dimension Y. we use the first image (self.imageFiles[0]) to get dimension.
        self.img_ori = self.currImageFile.img
        self.sizex_ori, self.sizey_ori = self.img_ori.size
        xysmcList = []  #
        col_no_rln_coordX = 0
        col_no_rln_coordY = 0
        col_no_rln_clsNum = 0
        col_no_rln_angPsi = 0
        col_no_rln_autopickFom = 0
        f = open(coorf)
        for line in f:
            if len(line) == 0:  ## In fact, blank lines are "\n".
                break
            line = line.rstrip('\n')  ## remove "\n"
            array_inp = re.split(r'\s+', line)
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
                # Difference between Spider (Fesp) and Relion in coordinate system
            # coordY is flipped    ; CoordY (Fesp) = SizeY - CoordY (Relion)
            # Psi is also flipped  ; Psi    (Fesp) = - Psi          (Relion)
            if len(array_inp) > 5:
                content = line.split()
                x = int(float(array_inp[col_no_rln_coordX])) - 1  # usu. col 1
                y = int(self.sizey_ori - (
                            float(array_inp[col_no_rln_coordY]) - 1))  # usu. col 2 # the axis needs to be flipped
                s = float(0.0 - float(array_inp[col_no_rln_angPsi]))  # usu. col 4 # The sign needs to be flipped
                m = float(float(array_inp[col_no_rln_autopickFom]))  # usu. col 5 # #figure of Merit
                c = int(array_inp[col_no_rln_clsNum])  # usu. col 3 # #class number
                xysmcList.append([x, y, s, m, c])  #
        f.close()
        return xysmcList

    def LoadImage(self):
        self.invertMarker = 1  # Autoset the image contrast as original (non-inverted)
        if len(self.currImageFile.stat) == 0:  # process the first time opened file
            self.currImageFile.stat = imageFunctions.Stat(self.currImageFile.path)
        self.img_ori = self.currImageFile.img
        self.img_ori_invert = self.currImageFile.img_invert
        self.sizex_ori, self.sizey_ori = self.img_ori.size

        if self.invertMarker == 1:
            self.imgstat = self.currImageFile.stat
        else:
            self.imgstat = self.currImageFile.stat_invert

        statusinfo = 'Min:%.1f, Max:%.1f, Mean:%.1f, Std:%.1f, Dim:%s' % (
        self.imgstat[3], self.imgstat[4], self.imgstat[0], self.imgstat[1], self.img_ori.size)
        self.GetParent().statusBar.SetStatusText(statusinfo, 0)
        self.img_contrast = imageFunctions.ContrastSigma(self.img_ori, self.imgstat, self.sigmaLevel)

        if self.openFirstFile:
            self.FitWin()  # Set all initial settings(map, size, pos, mag)
            self.openFirstFile = False
        else:  # Using previous settings
            self.bitmap_sizex = int(float(self.sizex_ori) * self.mag)
            self.bitmap_sizey = int(float(self.sizey_ori) * self.mag)
            self.bitmap = imageFunctions.ResizeToBmp(self.img_contrast, self.bitmap_sizex, self.bitmap_sizey)

        fmin, fmax = self.AutoContrastValue(self.imgstat, self.sigmaLevel)  # Set the values of contrast min/max fields
        # self.spinContrastMin.SetValue(fmin)
        # self.spinContrastMax.SetValue(fmax)

        self.panelM.Refresh()  # Draw image
        if len(self.currImageFile.xysmcList) > 0:  # Draw box if xylist is not empty
            self.particleList = imageFunctions.CutPartNormal(self.img_ori, self.currImageFile.xysmcList,
                                                             self.boxSize)  # ZC; particleList in the particle panel
        else:
            self.particleList = []
        self.pickedRectID = -1  # Clear the Selected particle ID in the montage from last file
        self.panelP.Refresh()

        if invertContrastS == 1:
            self.invertMarker = self.invertMarker * (-1)
            if self.invertMarker == -1:
                if self.currImageFile.img_invert.size[0] == 0:  # Inverted image not calculated yet
                    self.currImageFile.InvertContrast()
                self.imgstat = self.currImageFile.stat_invert
                self.img_contrast = imageFunctions.ContrastSigma(self.currImageFile.img_invert, self.imgstat,
                                                                 self.sigmaLevel)
            else:
                self.imgstat = self.currImageFile.stat
                self.img_contrast = imageFunctions.ContrastSigma(self.currImageFile.img, self.imgstat, self.sigmaLevel)
            self.bitmap = imageFunctions.ResizeToBmp(self.img_contrast, self.bitmap_sizex, self.bitmap_sizey)
            self.panelM.Refresh()
            fmin, fmax = self.AutoContrastValue(self.imgstat,
                                                self.sigmaLevel)  # Set the values of contrast min/max fields
            # self.spinContrastMin.SetValue(fmin)
            # self.spinContrastMax.SetValue(fmax)
        self.GetParent().statusBar.SetStatusText(
            'One micrograph loaded: %s' % (os.path.basename(self.currImageFile.path)), 2)

    def OnComboFilesT(self, event):  # Select and Load an image file
        self.currFile = self.comboFiles.GetSelection()
        self.currImageFile = self.imageFiles[self.currFile]
        self.SaveAllCoordinates()  # Autosave all particles before loading a new image
        self.LoadImage()  # "self.currImageFile" is loaded
        self.currFile = self.comboFiles.GetSelection()

    """
    def OnButtonCloseT(self, event):
        self.currFile = self.comboFiles.GetSelection()
        if self.currFile > -1:
            self.imageFiles.pop(self.currFile)
            self.comboFiles.Delete(self.currFile)
        if len(self.imageFiles) == 0: # when you close the last microghraph, refreshMainPanel in mode 2
            a =1
            self.GetParent().RefreshMainPanel(2)			
        else:
            if len(self.imageFiles) <= self.currFile:
                self.currFile = len(self.imageFiles) - 1
            count = 1			# refresh file list display
            self.comboFiles.Clear()
            for imagefile in self.imageFiles:
                item = '[%d] %s [%d %s](%d %s)' % (count, os.path.basename(imagefile.path), len(imagefile.xysmcListRef), imagefile.refCoordSource, len(imagefile.xysmcList), imagefile.edtCoordSource) # 
                self.comboFiles.Append(item)
                count += 1
            self.comboFiles.SetSelection(self.currFile)	
            self.currImageFile = self.imageFiles[self.currFile]
            self.LoadImage()
    """

    def OnButtonNextT(self, event):
        self.currFile = self.comboFiles.GetSelection()
        # if self.currFile > -1:
        #	self.imageFiles.pop(self.currFile)
        #	#self.comboFiles.Delete(self.currFile)
        if len(self.imageFiles) == 0:  # when you close the last microghraph, refreshMainPanel in mode 2
            a = 1
            self.GetParent().RefreshMainPanel(2)
        else:
            if self.currFile < len(self.imageFiles) - 1:
                self.currFile = self.currFile + 1
            else:
                self.currFile = self.currFile

            self.comboFiles.SetSelection(self.currFile)
            self.currImageFile = self.imageFiles[self.currFile]
            self.LoadImage()

    def OnMenuFileCloseAll(self, event):
        if len(self.imageFiles) == 0:
            return
        dlg = wx.MessageDialog(self, 'Do you want to close all the micrographs?', 'Please confirm!',
                               wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_YES:
            self.comboFiles.Clear()
            self.imageFiles = []
        self.panelM.Refresh()
        self.particleList = []
        self.panelP.Refresh()
        self.GetParent().ClearStatusBar()
        dlg.Destroy()

    def OnButtonFitWindowsT(self, event):
        if len(self.imageFiles) == 0:
            return
        self.FitWin()
        self.panelM.Refresh()

    def FitWin(self):  # Image fit into the window size
        winsizex, winsizey = self.panelM.GetSize()
        if float(winsizey) / self.sizey_ori <= float(winsizex) / self.sizex_ori:
            self.bitmap_sizey = winsizey
            self.bitmap_sizex = int(self.bitmap_sizey * (float(self.sizex_ori) / self.sizey_ori))
        else:
            self.bitmap_sizex = winsizex
            self.bitmap_sizey = int(self.bitmap_sizex * (float(self.sizey_ori) / self.sizex_ori))
        self.bitmap_x = int((winsizex - self.bitmap_sizex) / 2.0)
        self.bitmap_y = int((winsizey - self.bitmap_sizey) / 2.0)
        self.bitmap = imageFunctions.ResizeToBmp(self.img_contrast, self.bitmap_sizex, self.bitmap_sizey)
        self.mag = self.bitmap_sizex / float(self.sizex_ori)
        self.GetParent().statusBar.SetStatusText('Mag:%.3f' % self.mag, 1)

    def OnButtonMagT(self, event):
        if len(self.imageFiles) == 0:
            return
        mag = float(self.textMag.GetValue())
        if mag <= 0 or mag > 2:
            self.textMag.SetValue('1.0')
            return
        self.mag = mag
        sizex, sizey = wx.Bitmap.GetSize(self.bitmap)  # Save old size for centering
        self.bitmap_sizex = int(self.mag * self.sizex_ori)
        self.bitmap_sizey = int(self.mag * self.sizey_ori)
        self.bitmap = imageFunctions.ResizeToBmp(self.img_contrast, self.bitmap_sizex, self.bitmap_sizey)
        winsizex, winsizey = self.panelM.GetSize()
        centerx = winsizex / 2
        centery = winsizey / 2
        # Keep the image region at the CENTER at original position
        self.bitmap_x = centerx - (centerx - self.bitmap_x) * self.bitmap_sizex / sizex
        self.bitmap_y = centery - (centery - self.bitmap_y) * self.bitmap_sizey / sizey

        self.panelM.Refresh()
        self.GetParent().statusBar.SetStatusText('Mag: %.3f' % self.mag, 1)

    def OnComboSigmaT(self, event):
        if len(self.imageFiles) == 0:
            return
        item = event.GetSelection()
        self.sigmaLevel = self.sigmaValues[item]
        fmin, fmax = self.AutoContrastValue(self.imgstat, self.sigmaLevel)
        # self.spinContrastMin.SetValue(fmin)
        # self.spinContrastMax.SetValue(fmax)
        if self.invertMarker == -1:
            self.img_contrast = imageFunctions.ContrastSigma(self.currImageFile.img_invert, self.imgstat,
                                                             self.sigmaLevel)
        else:
            self.img_contrast = imageFunctions.ContrastSigma(self.currImageFile.img, self.imgstat, self.sigmaLevel)
        self.bitmap = imageFunctions.ResizeToBmp(self.img_contrast, self.bitmap_sizex, self.bitmap_sizey)
        self.panelM.Refresh()

    def AutoContrastValue(self, stat, sigmaLevel):  # Set the values of contrast min & max TextCtrls
        truemin = stat[0] - stat[1] * sigmaLevel
        truemax = stat[0] + stat[1] * sigmaLevel
        imgmin = stat[3]
        imgmax = stat[4]
        imgrange = imgmax - imgmin
        fmin = int(1000 * (truemin - imgmin) / imgrange)
        fmax = int(1000 * (truemax - imgmin) / imgrange)
        return fmin, fmax

    """
    def OnButtonContrastT(self, event):
        if len(self.imageFiles) == 0:
            return
        imgmin = self.imgstat[3]
        imgmax = self.imgstat[4]
        imgrange = imgmax - imgmin
        truemin = imgmin + imgrange * 0.001 * self.spinContrastMin.GetValue()
        truemax = imgmin + imgrange * 0.001 * self.spinContrastMax.GetValue()
        brightness = self.spinBright.GetValue()
        if self.invertMarker == -1:
            self.img_contrast = imageFunctions.Contrast(self.currImageFile.img_invert, truemin, truemax, brightness)
        else:
            self.img_contrast = imageFunctions.Contrast(self.currImageFile.img, truemin, truemax, brightness)
        self.bitmap = imageFunctions.ResizeToBmp(self.img_contrast, self.bitmap_sizex, self.bitmap_sizey)
        self.panelM.Refresh()
    """

    def OnButtonInvertT(self, event):
        if len(self.imageFiles) == 0:
            return
        self.invertMarker = self.invertMarker * (-1)
        if self.invertMarker == -1:
            if self.currImageFile.img_invert.size[0] == 0:  # Inverted image not calculated yet
                self.currImageFile.InvertContrast()
            self.imgstat = self.currImageFile.stat_invert
            self.img_contrast = imageFunctions.ContrastSigma(self.currImageFile.img_invert, self.imgstat,
                                                             self.sigmaLevel)
        else:
            self.imgstat = self.currImageFile.stat
            self.img_contrast = imageFunctions.ContrastSigma(self.currImageFile.img, self.imgstat, self.sigmaLevel)
        self.bitmap = imageFunctions.ResizeToBmp(self.img_contrast, self.bitmap_sizex, self.bitmap_sizey)
        self.panelM.Refresh()
        fmin, fmax = self.AutoContrastValue(self.imgstat, self.sigmaLevel)  # Set the values of contrast min/max fields
        # self.spinContrastMin.SetValue(fmin)
        # self.spinContrastMax.SetValue(fmax)

    def OnButtonResizeT(self, event):
        self.boxSize = int(float(self.textBoxSize.GetValue()))
        self.boxSize_ref = int(float(self.textBoxSizeRef.GetValue()))
        if len(self.imageFiles) == 0:
            return
        self.panelM.Refresh()
        self.particleList = imageFunctions.CutPartNormal(self.img_ori, self.currImageFile.xysmcList,
                                                         self.boxSize)  # also update the particle window
        self.panelP.Refresh()

    def OnMenuFileSaveAllCoordinates(self, event):
        self.SaveAllCoordinates()  # this save function is also used in other places

    def SaveAllCoordinates(self):
        if len(self.imageFiles) == 0:
            return
        self.img_ori = self.currImageFile.img
        self.sizex_ori, self.sizey_ori = self.img_ori.size
        total = 0
        imgcount = 0
        for imagefile in self.imageFiles:
            if len(imagefile.xysmcList) > 0:  #
                basename = os.path.splitext(os.path.basename(imagefile.path))
                coorf = os.path.dirname(imagefile.path) + '/' + basename[0] + '_fesp.star'
                if os.path.exists(coorf):
                    os.remove(coorf)
                filehandle_out_star = open(coorf, "w")
                filehandle_out_star.write("%s\n" % (""))
                filehandle_out_star.write("%s\n" % ("data_"))
                filehandle_out_star.write("%s\n" % (""))
                filehandle_out_star.write("%s\n" % ("loop_ "))
                filehandle_out_star.write("%s\n" % ("_rlnCoordinateX #1 "))
                filehandle_out_star.write("%s\n" % ("_rlnCoordinateY #2 "))
                filehandle_out_star.write("%s\n" % ("_rlnClassNumber #3 "))
                filehandle_out_star.write("%s\n" % ("_rlnAnglePsi #4 "))
                filehandle_out_star.write("%s\n" % ("_rlnAutopickFigureOfMerit #5 "))
                i = 1
                for xysmc in imagefile.xysmcList:  # see LoadCoor() for the difference between Spider (Fesp) and Relion in coordinate system
                    filehandle_out_star.write("%13.6f%13.6f%13d%13f%13.6f\n" % (
                    float(xysmc[0] + 1), float(self.sizey_ori - xysmc[1] + 1), int(xysmc[4]), float(0.0 - xysmc[2]),
                    float(xysmc[3])))
                    i += 1
                    total += 1
                    filehandle_out_star.close()
                imgcount += 1
        self.GetParent().statusBar.SetStatusText('%d particles from %d images saved!' % (total, imgcount), 2)

    def OnButtonSaveCurrentCoordinatesT(self, event):
        self.SaveCurrentCoordinates()  # this save function is also used in other places

    def SaveCurrentCoordinates(self):
        if len(self.imageFiles) == 0:
            return
        self.img_ori = self.currImageFile.img
        self.sizex_ori, self.sizey_ori = self.img_ori.size
        total = 0
        if len(self.currImageFile.xysmcList) > 0:  #
            basename = os.path.splitext(os.path.basename(self.currImageFile.path))
            coorf = os.path.dirname(self.currImageFile.path) + '/' + basename[0] + '_fesp.star'
            if os.path.exists(coorf):
                os.remove(coorf)
            filehandle_out_star = open(coorf, "w")
            filehandle_out_star.write("%s\n" % (""))
            filehandle_out_star.write("%s\n" % ("data_"))
            filehandle_out_star.write("%s\n" % (""))
            filehandle_out_star.write("%s\n" % ("loop_ "))
            filehandle_out_star.write("%s\n" % ("_rlnCoordinateX #1 "))
            filehandle_out_star.write("%s\n" % ("_rlnCoordinateY #2 "))
            filehandle_out_star.write("%s\n" % ("_rlnClassNumber #3 "))
            filehandle_out_star.write("%s\n" % ("_rlnAnglePsi #4 "))
            filehandle_out_star.write("%s\n" % ("_rlnAutopickFigureOfMerit #5 "))
            i = 1
            for xysmc in self.currImageFile.xysmcList:  # see LoadCoor() for the difference between Spider (Fesp) and Relion in coordinate system
                filehandle_out_star.write("%13.6f%13.6f%13d%13f%13.6f\n" % (
                float(xysmc[0] + 1), float(self.sizey_ori - xysmc[1] + 1), int(xysmc[4]), float(0.0 - xysmc[2]),
                float(xysmc[3])))
                i += 1
                total += 1
                filehandle_out_star.close()
        self.GetParent().statusBar.SetStatusText('%d particles from the current image saved!' % (total), 2)

    def CalcPsiUsingTwoPoints4TheSelectedParticle(self, centerX, centerY, touchX, touchY):
        deltaX = float(touchX - centerX)
        deltaY = float(touchY - centerY)
        psi = math.degrees(math.atan2(deltaY, deltaX))
        return psi

    def OnButtonDisplayBoxT(self, event):
        if len(self.imageFiles) == 0:
            return
        if self.currImageFile.displayBox == 0:
            self.currImageFile.displayBox = 1
            self.GetParent().statusBar.SetStatusText('Box displayed: %d' % (self.currImageFile.displayBox), 2)
        elif self.currImageFile.displayBox == 1:
            self.currImageFile.displayBox = 0
            self.GetParent().statusBar.SetStatusText('Box hidden: %d' % (self.currImageFile.displayBox), 2)
        self.panelM.Refresh()

    def OnButtonDisplayPsiT(self, event):
        if len(self.imageFiles) == 0:
            return
        if self.currImageFile.displayPsi == 0:
            self.currImageFile.displayPsi = 1
            self.GetParent().statusBar.SetStatusText('Psi displayed: %d' % (self.currImageFile.displayPsi), 2)
        elif self.currImageFile.displayPsi == 1:
            self.currImageFile.displayPsi = 0
            self.GetParent().statusBar.SetStatusText('Psi hidden: %d' % (self.currImageFile.displayPsi), 2)
        self.panelM.Refresh()

    def OnTextSetPsi4CurrPtclT(self, event):
        self.psi = float(self.textSetPsi.GetValue())
        self.currImageFile.xysmcList[self.pickedRectID][2] = self.psi
        self.dispXysmcList = self.currImageFile.DispXysmcList(self.mag, self.boxSize)  # constructs self.dispXysmcList
        self.panelM.Refresh()

    def OnTextSetFom4CurrPtclT(self, event):
        self.fom = float(self.textSetFom.GetValue())
        self.currImageFile.xysmcList[self.pickedRectID][3] = self.fom
        self.dispXysmcList = self.currImageFile.DispXysmcList(self.mag, self.boxSize)  # constructs self.dispXysmcList
        self.panelM.Refresh()

    def RefreshPanelT(self):  # not used yet
        self.panelT.Destroy()
        self.panelT = FespPanelT(self, -1)
        frameSizer = wx.BoxSizer(wx.VERTICAL)
        frameSizer.Add(self.panelT, 0, wx.EXPAND | wx.BOTTOM, 5)
        frameSizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(frameSizer)
        self.Layout()

    ######## PanelM Events ######### PanelM: Micrograph Panel
    def OnPaintM(self, event):  # paint the micrograph
        dc = wx.PaintDC(self.panelM)  # PaintDC: paint device; paint particles (memoryDC) on the micrograph (bitmap)
        dc.SetBrush(wx.Brush(wx.BLACK, wx.SOLID))  # set the background of micrograph panel black
        dc.SetBackground(wx.Brush(wx.BLACK))
        dc.Clear()
        if len(self.imageFiles) == 0 or self.comboFiles.GetSelection() == -1:  # display intro upon starting the program
            if self.GetParent().introductionShow:
                dc.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                dc.DrawTextList(self.GetParent().introductionText, self.GetParent().introductionCoord,
                                wx.WHITE)  # introduction screen
            return
        memDC = wx.MemoryDC()  # MemoryDC: memory device; for drawing graphics onto a bitmap

        # Draw micrograph
        if wx.__version__.startswith("3"):
            drawbmp = wx.EmptyBitmap(self.bitmap_sizex, self.bitmap_sizey)  # wxPython 3.0
        elif wx.__version__.startswith("4"):
            drawbmp = wx.Bitmap(self.bitmap_sizex, self.bitmap_sizey)  # wxPython 4.0
        memDC.SelectObject(drawbmp)
        memDC.Clear()
        memDC.DrawBitmap(self.bitmap, 0, 0)

        # Draw Boxes [not editable] according to the xysmcListRef
        self.dispXysmcListRef = self.currImageFile.DispXysmcListRef(self.mag, self.boxSize_ref)
        if len(self.dispXysmcListRef) > 0:
            memDC.SetPen(wx.Pen(wx.BLUE, 2))
            memDC.SetBrush(wx.Brush(wx.WHITE, wx.TRANSPARENT))
            dispRectangleListRef = []
            dispPenListRef = []
            for item in self.dispXysmcListRef:
                rectangleX = int(item[0])  # ???
                rectangleY = int(item[1])
                rectangleW = int(item[2])
                rectangleH = int(item[2])
                penRef = wx.Pen(wx.Colour(255, 255, 255), 1, wx.PENSTYLE_SOLID)
                dispRectangleListRef.append([rectangleX, rectangleY, rectangleW, rectangleH])
                dispPenListRef.append(penRef)
            if self.currImageFile.displayBox == 1:
                memDC.DrawRectangleList(dispRectangleListRef, dispPenListRef)  # works

        # Draw Circles and lines according to the xysmcList
        self.dispXysmcList = self.currImageFile.DispXysmcList(self.mag, self.boxSize)  # constructs self.dispXysmcList
        if len(self.dispXysmcList) > 0:
            memDC.SetPen(wx.Pen(wx.GREEN, 1))  #
            memDC.SetBrush(wx.Brush(wx.WHITE, wx.TRANSPARENT))
            # DrawEllipse (self, x, y, width, height)
            # Pen(colour, width=1, style=PENSTYLE_SOLID)
            dispEllippseList = []
            dispPenList = []
            for item in self.dispXysmcList:
                ellipseX = int(item[0])  # ???
                ellipseY = int(item[1])
                ellipseW = int(item[2])
                ellipseH = int(item[2])
                # based on class averages
                if item[4] >= fomGreenS:  # 5 GREEN:   crispy classes
                    pen = wx.Pen(wx.Colour(0, 255, 0), 1, wx.PENSTYLE_SOLID)
                elif item[4] >= fomYellowS:  # 4 YELLOW:  decent classes (some with one smear subunit)
                    pen = wx.Pen(wx.Colour(255, 255, 0), 1, wx.PENSTYLE_SOLID)
                elif item[4] >= fomOrangeS:  # 3 ORANGE:  reasonally good classes
                    pen = wx.Pen(wx.Colour(255, 165, 0), 1, wx.PENSTYLE_SOLID)
                elif item[4] >= fomMagentaS:  # 2 MAGENTA: classes contain middle parts
                    pen = wx.Pen(wx.Colour(255, 0, 255), 1, wx.PENSTYLE_SOLID)
                elif item[4] >= fomRedS:  # 1  RED:    not so clear classes
                    pen = wx.Pen(wx.Colour(255, 0, 0), 1, wx.PENSTYLE_SOLID)
                elif item[4] >= fomCyanS:  # 1  CYAN:    not so clear classes
                    pen = wx.Pen(wx.Colour(0, 255, 255), 1, wx.PENSTYLE_SOLID)
                else:  # 0  WHITE:  bad classes; empty classes
                    pen = wx.Pen(wx.Colour(255, 255, 255), 1, wx.PENSTYLE_SOLID)
                dispEllippseList.append([ellipseX, ellipseY, ellipseW, ellipseH])
                dispPenList.append(pen)
            if self.currImageFile.displayBox == 1:
                memDC.DrawEllipseList(dispEllippseList, dispPenList)  # works
            memDC.SetPen(wx.Pen(wx.BLUE, 4))  # this determines the width of the psi indicator
            memDC.SetBrush(wx.Brush(wx.WHITE, wx.TRANSPARENT))
            disp2PointList = []
            for item in self.dispXysmcList:
                centerX = int(item[0]) + int(item[2]) / 2  # ???
                centerY = int(item[1]) + int(item[2]) / 2  # ???
                dist_from_center_to_point1 = float(item[2]) / 2
                dist_from_center_to_point2 = float(item[2]) * float(
                    psiNeedleRatioS)  # this determines the length of the psi indicator
                angPsi = item[3]
                point1X = float(centerX) + (float(dist_from_center_to_point1)) * math.cos(
                    (float(angPsi) / 180.0) * math.pi)
                point1Y = float(centerY) - (float(dist_from_center_to_point1)) * math.sin(
                    (float(angPsi) / 180.0) * math.pi)
                point2X = float(centerX) + (float(dist_from_center_to_point2)) * math.cos(
                    (float(angPsi) / 180.0) * math.pi)
                point2Y = float(centerY) - (float(dist_from_center_to_point2)) * math.sin(
                    (float(angPsi) / 180.0) * math.pi)
                disp2PointList.append([int(point1X), int(point1Y), int(point2X), int(point2Y)])
                if self.currImageFile.displayPsi == 1 and psiNeedleRatioS != 0.0:
                    memDC.DrawLineList(disp2PointList)  # works

        # Draw picked_BOX (in RED)
        if self.pickedRectID > -1:  # when you click on a ptcl in panelP, you highlight the corresponding ptcl on the micrograph panel.
            rect = self.dispXysmcList[self.pickedRectID]  #
            memDC.SetPen(wx.Pen(wx.RED, 2))
            memDC.SetBrush(wx.Brush(wx.WHITE, wx.TRANSPARENT))
            memDC.DrawRectangle(rect[0], rect[1], rect[2], rect[2])  #

        # Draw eraser cursor circle, when ctrl+motion and rad>1
        if self.cursorDraw:
            ptx = self.cursorPt[0] - self.bitmap_x
            pty = self.cursorPt[1] - self.bitmap_y
            memDC.SetPen(wx.Pen(wx.RED, 5))
            memDC.SetBrush(wx.Brush(wx.WHITE, wx.TRANSPARENT))
            memDC.DrawCircle(ptx - 1, pty - 1, self.cursorRadius)  # with mag already applied (in function "OnMotion")
            # pt-1 to get better positioning
        # Real drawing
        dc.Blit(self.bitmap_x, self.bitmap_y, self.bitmap_sizex, self.bitmap_sizey, memDC, 0, 0, wx.COPY, True)
        memDC.SelectObject(wx.NullBitmap)

    def HitTest(self,
                pt):  # micrograph panel # HitTest (mouse left down or up): Finds the row and column of the character at the specified point.
        if len(self.currImageFile.xysmcList) == 0:
            return []
        pt = (pt[0] - self.bitmap_x, pt[1] - self.bitmap_y)  # True coordinate on micrograph
        hitpoints = []
        for i in range(len(self.dispXysmcList)):
            disp = self.dispXysmcList[i]

            if pt[0] >= disp[0] and pt[0] <= (disp[0] + disp[2]):
                # if pt[1] >= disp[1] and pt[1] <= (disp[1] + disp[3]):
                if pt[1] >= disp[1] and pt[1] <= (disp[1] + disp[2]):  # dispXysmcList x-rad, y-rad, boxSize, phi, fom
                    hitpoints.append(i)
                    self.pickedRectID = i  # for highlighting the left mouse SELECTED ptcl in Micrograph panel
                    # when you click on an existing ptcl in the panelM, its psi and fom are displayed in the top right corner.
                    self.textSetPsi.SetValue(str(self.currImageFile.xysmcList[self.pickedRectID][2]))  #
                    self.textSetFom.SetValue(str(self.currImageFile.xysmcList[self.pickedRectID][3]))  #
        return hitpoints  # ; the displayed ptcl id in self.dispXysmcList, starting from 0; taking the manually picked ptcls into account

    def OnLeftDownM(self, event):
        if len(self.imageFiles) == 0:
            return
        pt = event.GetPosition()
        pt_img = (pt[0] - self.bitmap_x, pt[1] - self.bitmap_y)
        pt = (self.bitmap_x + pt_img[0], self.bitmap_y + pt_img[1])
        hitpoints = self.HitTest(pt)
        if len(hitpoints) > 0:  # if one particle is hit, save ID and the coordinate
            self.hit_leftdown = hitpoints[0]
            self.xysmcList_hit = []  #
            self.xysmcList_hit.extend(self.currImageFile.xysmcList[self.hit_leftdown])  #
            self.hitPt = pt  # Saved for others, e.g. 'OnMotion' to move box
        else:
            self.hit_leftdown = -1  # -1: no hit; otherwise, hit a particle

    def OnLeftUpM(self, event):
        if len(self.imageFiles) == 0:
            return
        pt = event.GetPosition()
        pt_img = (pt[0] - self.bitmap_x, pt[1] - self.bitmap_y)
        pt = (self.bitmap_x + pt_img[0], self.bitmap_y + pt_img[1])
        hitpoints = self.HitTest(pt)  # HitTest for mouse_up
        if event.ShiftDown():  # Delete one particle
            if len(hitpoints) == 1:
                self.currImageFile.xysmcList.pop(hitpoints[0])
                self.particleList.pop(hitpoints[0])
                self.pickedRectID = -1  # Clear the highlighted particle
                self.GetParent().statusBar.SetStatusText(
                    'One particle deleted. Current total %d' % len(self.particleList), 2)
                self.panelP.Refresh()
                self.panelM.Refresh()
                # Refresh combo_box to show particle number
                self.comboFiles.Delete(self.currFile)
                newitem = '[%d] %s [%d %s](%d %s)' % (
                self.currFile + 1, os.path.basename(self.currImageFile.path), len(self.currImageFile.xysmcListRef),
                self.currImageFile.refCoordSource, len(self.currImageFile.xysmcList), self.currImageFile.edtCoordSource)
                self.comboFiles.Insert(newitem, self.currFile)
                self.comboFiles.SetSelection(self.currFile)
            return
        if len(hitpoints) == 0:
            self.hit_leftup = -1
        elif len(hitpoints) == 1:
            self.hit_leftup = hitpoints[0]
        else:
            self.hit_leftup = -2  # This only happen when a box moved on top of another
        if self.hit_leftdown == -1:  # New particle picked
            if self.hit_leftup == -1:
                newx = int((pt[0] - self.bitmap_x) / self.mag)
                newy = int((pt[1] - self.bitmap_y) / self.mag)

                news = float(float(self.textSetPsi.GetValue()))  #
                newm = float(float(self.textSetFom.GetValue()))  #
                newc = int("0")  # the manually picked partcle is assigned to class 0
                if newx > 0 and newx < self.sizex_ori and newy > 0 and newy < self.sizey_ori:
                    self.currImageFile.xysmcList.append([newx, newy, news, newm, newc])  #
                    newregion = imageFunctions.CutPartNormal(self.img_ori, [[newx, newy]], self.boxSize)[0]
                    self.particleList.append(newregion)
                    self.GetParent().statusBar.SetStatusText(
                        'One particle added. Current total %d' % len(self.particleList), 2)
                    # Refresh combo_box to show particle number
                    self.comboFiles.Delete(self.currFile)
                    newitem = '[%d] %s [%d %s](%d %s)' % (
                    self.currFile + 1, os.path.basename(self.currImageFile.path), len(self.currImageFile.xysmcListRef),
                    self.currImageFile.refCoordSource, len(self.currImageFile.xysmcList),
                    self.currImageFile.edtCoordSource)
                    self.comboFiles.Insert(newitem, self.currFile)
                    self.comboFiles.SetSelection(self.currFile)
                    self.pickedRectID = int(
                        len(self.currImageFile.xysmcList) - 1)  # for hightlighting the last picked particle
        else:  # Modify previous particles
            i = self.hit_leftdown
            if self.hit_leftup == -2:  # No change, restore old coordinate
                self.currImageFile.xysmcList[i][0] = self.xysmcList_hit[0]  #
                self.currImageFile.xysmcList[i][1] = self.xysmcList_hit[1]
            else:  # Change one particle coordinate
                self.currImageFile.xysmcList[i][0] = self.xysmcList_hit[0] + int((pt[0] - self.hitPt[0]) / self.mag)
                self.currImageFile.xysmcList[i][1] = self.xysmcList_hit[1] + int((pt[1] - self.hitPt[1]) / self.mag)
                newregion = imageFunctions.CutPartNormal(self.img_ori, [
                    [self.currImageFile.xysmcList[i][0], self.currImageFile.xysmcList[i][1]]], self.boxSize)[0]
                self.particleList[i] = newregion
        self.panelM.Refresh()
        self.panelP.Refresh()

    def OnRightDownM(self, event):
        if len(self.imageFiles) == 0:
            return
        self.dragStartPos = event.GetPosition()
        if wx.__version__.startswith("3"):
            self.panelP.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))  # wxPython 3.0
        elif wx.__version__.startswith("4"):
            self.panelP.SetCursor(wx.Cursor(wx.CURSOR_ARROW))  # wxPython 4.0
        self.panelM.Refresh()

    def OnRightUpM(self, event):
        if len(self.imageFiles) == 0:
            return
        if wx.__version__.startswith("3"):
            self.panelP.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))  # wxPython 3.0
        elif wx.__version__.startswith("4"):
            self.panelP.SetCursor(wx.Cursor(wx.CURSOR_ARROW))  # wxPython 4.0

    def OnMotionM(self, event):  # Mouse Left Hold and move
        if len(self.imageFiles) == 0:
            return
        if event.ShiftDown():  # No response for "Shift" (to delete particle)
            return
        pt = event.GetPosition()
        if event.ControlDown():  # "Ctrol" to draw a circle attached to cursor
            self.cursorRadiusTrue = float(self.textEraserRadius.GetValue())
            self.cursorRadius = int(self.cursorRadiusTrue * self.mag)
            if self.cursorRadius > 1:
                self.cursorDraw = True
                self.cursorPt = pt
                if event.RightIsDown():  # Eraser = Ctrl + Hold down Right + Move
                    xtrue = int((pt[0] - self.bitmap_x) / self.mag)
                    ytrue = int((pt[1] - self.bitmap_y) / self.mag)
                    xysmcList_new = []  # The remaining particle coordinates and cut-particles
                    particleList_new = []
                    i = -1
                    for item in self.currImageFile.xysmcList:  #
                        i += 1
                        if abs(item[0] - xtrue) > self.cursorRadiusTrue or abs(item[1] - ytrue) > self.cursorRadiusTrue:
                            xysmcList_new.append(item)
                            particleList_new.append(self.particleList[i])
                    self.currImageFile.xysmcList = []
                    self.currImageFile.xysmcList.extend(xysmcList_new)
                    self.particleList = []
                    self.particleList.extend(particleList_new)
                    self.pickedRectID = -1  # Clear the highlighted particle
                    self.GetParent().statusBar.SetStatusText('Erasing particles', 2)
                    self.panelP.Refresh()
                    # Refresh combo_box to show particle number
                    self.comboFiles.Delete(self.currFile)
                    newitem = '[%d] %s [%d %s](%d %s)' % (
                    self.currFile + 1, os.path.basename(self.currImageFile.path), len(self.currImageFile.xysmcListRef),
                    self.currImageFile.refCoordSource, len(self.currImageFile.xysmcList),
                    self.currImageFile.edtCoordSource)
                    self.comboFiles.Insert(newitem, self.currFile)
                    self.comboFiles.SetSelection(self.currFile)
        else:
            self.cursorDraw = False
            if event.RightIsDown():  # Moving the micrograph
                diff = pt - self.dragStartPos
                if abs(diff[0]) > 1 or abs(diff[1]) > 1:
                    self.bitmap_x += diff[0]
                    self.bitmap_y += diff[1]
                    self.dragStartPos[0] += diff[0]
                    self.dragStartPos[1] += diff[1]
            elif event.LeftIsDown() and self.hit_leftdown != -1:  # Moving the marker (box)
                i = self.hit_leftdown
                # Box movement is not determined by the clicking point, but rather the moving of mouse/box
                self.currImageFile.xysmcList[i][0] = self.xysmcList_hit[0] + int((pt[0] - self.hitPt[0]) / self.mag)
                self.currImageFile.xysmcList[i][1] = self.xysmcList_hit[1] + int((pt[1] - self.hitPt[1]) / self.mag)
                newregion = imageFunctions.CutPartNormal(self.img_ori, [
                    [self.currImageFile.xysmcList[i][0], self.currImageFile.xysmcList[i][1]]], self.boxSize)[0]
                self.particleList[i] = newregion
                self.panelP.Refresh()
            else:
                return
        self.panelM.Refresh()

    def OnWheelM(self, event):
        if len(self.imageFiles) == 0:
            return
            rotation = event.GetWheelRotation()  # -120: rotate down, shrink image; +120: up, enlarge
        sizex, sizey = wx.Bitmap.GetSize(self.bitmap)
        if sizex < 20 or sizey < 20:
            if rotation < 0:
                return  # Can not make any smaller
        if rotation > 0:
            label = 1
        else:
            label = -1
        if event.ControlDown():
            step = 0.01
        else:
            step = 0.05
        self.mag += label * step
        self.bitmap_sizex = int(self.mag * self.sizex_ori)
        self.bitmap_sizey = int(self.mag * self.sizey_ori)
        self.bitmap = imageFunctions.ResizeToBmp(self.img_contrast, self.bitmap_sizex, self.bitmap_sizey)
        # Position of the resized bitmap (Center with mouse or display center)
        if event.ControlDown():
            centerx, centery = event.GetPosition()
        else:
            winsizex, winsizey = self.panelM.GetSize()
            centerx = winsizex / 2
            centery = winsizey / 2
        # Keep the image region at the CENTER at original position
        self.bitmap_x = centerx - (centerx - self.bitmap_x) * self.bitmap_sizex / sizex
        self.bitmap_y = centery - (centery - self.bitmap_y) * self.bitmap_sizey / sizey

        self.panelM.Refresh()
        self.GetParent().statusBar.SetStatusText('Mag:%.3f' % self.mag, 1)

    def OnRightUpPsiM(self, event):
        if event.AltDown():  # Use the combination Alt+RightUp to calc and set the phi angle of the selected particle
            if len(self.imageFiles) == 0:
                return
        if event.ShiftDown():  # Avoid confusion with fast click of "Shift + Left" (to remove particles)
            return
        if event.ControlDown():  # Avoid confusion with fast click of "Shift + Left" (to remove particles)
            return
        if event.CmdDown():  # Avoid confusion with fast click of "Shift + Left" (to remove particles)
            return
        pt = event.GetPosition()
        pt_img = (pt[0] - self.bitmap_x, pt[1] - self.bitmap_y)
        pt = (self.bitmap_x + pt_img[0], self.bitmap_y + pt_img[1])
        if self.pickedRectID >= 0:  # center is selected
            centerX = self.currImageFile.xysmcList[self.pickedRectID][0]
            centerY = self.currImageFile.xysmcList[self.pickedRectID][1]
            touchX = int((pt[0] - self.bitmap_x) / self.mag)  # No need to check the range of pt[],
            touchY = int((pt[1] - self.bitmap_y) / self.mag)  # even though it's in the black area, it's ok
            psi = - self.CalcPsiUsingTwoPoints4TheSelectedParticle(centerX, centerY, touchX,
                                                                   touchY)  # Y is flipped, so the sign is "-"
            self.textSetPsi.SetValue(str(psi))  #
        self.panelM.Refresh()

    def OnMiddleUpM(self, event):
        if len(self.imageFiles) == 0:
            return
            if self.currImageFile.displayBox == 0:
                self.currImageFile.displayBox = 1
                self.GetParent().statusBar.SetStatusText('Box displayed: %d' % (self.currImageFile.displayBox), 2)
            elif self.currImageFile.displayBox == 1:
                self.currImageFile.displayBox = 0
                self.GetParent().statusBar.SetStatusText('Box hidden: %d' % (self.currImageFile.displayBox), 2)
        if self.currImageFile.displayPsi == 0:
            self.currImageFile.displayPsi = 1
            self.GetParent().statusBar.SetStatusText('Psi displayed: %d' % (self.currImageFile.displayPsi), 2)
        elif self.currImageFile.displayPsi == 1:
            self.currImageFile.displayPsi = 0
            self.GetParent().statusBar.SetStatusText('Psi hidden: %d' % (self.currImageFile.displayPsi), 2)
        self.panelM.Refresh()

    def OnKeyUpM(self, event):
        #		print("M1 keycode =", keycode)
        if len(self.imageFiles) == 0:
            return

        pt = event.GetPosition()
        keycode = event.GetKeyCode()
        print("M2 keycode =", keycode)
        if (keycode == wx.WXK_CONTROL_I or keycode == wx.WXK_PAGEUP):
            self.invertMarker = self.invertMarker * (-1)
            if self.invertMarker == -1:
                if self.currImageFile.img_invert.size[0] == 0:  # Inverted image not calculated yet
                    self.currImageFile.InvertContrast()
                self.imgstat = self.currImageFile.stat_invert
                self.img_contrast = imageFunctions.ContrastSigma(self.currImageFile.img_invert, self.imgstat,
                                                                 self.sigmaLevel)
            else:
                self.imgstat = self.currImageFile.stat
                self.img_contrast = imageFunctions.ContrastSigma(self.currImageFile.img, self.imgstat, self.sigmaLevel)
                self.bitmap = imageFunctions.ResizeToBmp(self.img_contrast, self.bitmap_sizex, self.bitmap_sizey)
                self.panelM.Refresh()
            fmin, fmax = self.AutoContrastValue(self.imgstat,
                                                self.sigmaLevel)  # Set the values of contrast min/max fields

    ######## PanelP ######## PanelP: Particle Panel
    def OnPaintP(self, event):
        self.panelP.SetBackgroundColour(wx.BLACK)
        if len(self.particleList) == 0:
            return
        partwinsize = self.panelP.GetSize()
        mboxSize = int(self.boxSize * self.particleMag)
        if partwinsize[0] < mboxSize + 4:
            numperrow = 1
        else:
            numperrow = int(partwinsize[0] / float((mboxSize) + 1))
        row = int(len(self.particleList) / numperrow) + 1
        dc = wx.PaintDC(self.panelP)
        draw_sizex = numperrow * (mboxSize + 1)
        draw_sizey = row * (mboxSize + 1)
        if wx.__version__.startswith("3"):
            drawbmp = wx.EmptyBitmap(draw_sizex, draw_sizey)  # wxPython 3.0
        if wx.__version__.startswith("4"):
            drawbmp = wx.Bitmap(draw_sizex, draw_sizey)  # wxPython 4.0
        memDC = wx.MemoryDC()
        memDC.SelectObject(drawbmp)
        memDC.SetBrush(wx.Brush(wx.BLACK, wx.SOLID))
        memDC.SetBackground(wx.Brush(wx.BLACK))
        memDC.Clear()  # Clears the device context using the current background brush.
        memDC.SetPen(wx.Pen(wx.GREEN, 1))
        memDC.SetBrush(wx.Brush(wx.BLACK, wx.TRANSPARENT))

        # Draw montage
        self.particleRectList = []
        count = 0
        for y in range(row):
            for x in range(numperrow):
                if count < len(self.particleList):
                    if self.particleMag == 1:
                        bitmap = imageFunctions.ImgToBmp(self.particleList[count])
                    else:
                        bitmap = imageFunctions.ResizeToBmp(self.particleList[count], mboxSize, mboxSize)
                    memDC.DrawBitmap(bitmap, x * (mboxSize + 1), y * (mboxSize + 1))
                    self.particleRectList.append(
                        wx.Rect(x * (mboxSize + 1), y * (mboxSize + 1), mboxSize, mboxSize))  # Reclist for Hittest
                count += 1

        if self.pickedRectID > -1:
            rect = self.particleRectList[self.pickedRectID]
            memDC.SetPen(wx.Pen(wx.RED, 1))
            memDC.DrawRectangle(rect[0], rect[1], rect[2], rect[2])

        # Reset montage up left corner
        if not self.particleFreePos:
            self.particleDraw_x = 0
            if draw_sizey < partwinsize[1]:
                self.particleDraw_y = 0
            else:
                self.particleDraw_y = partwinsize[1] - draw_sizey

        dc.Blit(self.particleDraw_x, self.particleDraw_y, draw_sizex, draw_sizey, memDC, 0, 0, wx.COPY, True)
        memDC.SelectObject(wx.NullBitmap)

    def OnLeftUpP(self, event):  # move a particle to the top in the particle panel
        if len(self.particleList) == 0:
            return
        pt = event.GetPosition()
        pt_montage = pt - (self.particleDraw_x, self.particleDraw_y)
        i = 0  # Hit_test
        goon = True
        contains = False
        while i < len(self.particleRectList) and goon:
            if wx.__version__.startswith("3"):
                contains = self.particleRectList[i].InsideXY(pt_montage[0], pt_montage[1])  # wxPython 3.0
            elif wx.__version__.startswith("4"):
                contains = self.particleRectList[i].Contains(pt_montage[0], pt_montage[1])  # wxPython 4.0
            if contains == True:
                if event.ShiftDown():  # Delete one particle
                    self.particleList.pop(i)
                    self.currImageFile.xysmcList.pop(i)
                    self.pickedRectID = -1
                    self.GetParent().statusBar.SetStatusText(
                        'One particle deleted. Current total %d' % len(self.particleList), 2)
                    self.comboFiles.Delete(self.currFile)  # Refresh combo_box to show particle number
                    newitem = '[%d] %s [%d %s](%d %s)' % (
                    self.currFile + 1, os.path.basename(self.currImageFile.path), len(self.currImageFile.xysmcListRef),
                    self.currImageFile.refCoordSource, len(self.currImageFile.xysmcList),
                    self.currImageFile.edtCoordSource)
                    self.comboFiles.Insert(newitem, self.currFile)
                    self.comboFiles.SetSelection(self.currFile)
                elif event.ControlDown():  # Move this particle to the top of the particle list
                    movepart = self.particleList.pop(i)
                    self.particleList.insert(0, movepart)
                    movexy = self.currImageFile.xysmcList.pop(i)  #
                    self.currImageFile.xysmcList.insert(0, movexy)  #
                    self.pickedRectID = -1
                    self.GetParent().statusBar.SetStatusText(
                        'One particle moved to the top. Current total %d' % len(self.particleList), 2)
                else:  # Highlight one particle
                    self.pickedRectID = i
                    self.GetParent().statusBar.SetStatusText('ID of the selected particle: %d' % (i + 1), 2)
                    winsizex, winsizey = self.panelM.GetSize()
                    self.bitmap_x = int(winsizex / 2.0 - self.mag * self.currImageFile.xysmcList[i][0])
                    self.bitmap_y = int(winsizey / 2.0 - self.mag * self.currImageFile.xysmcList[i][1])
                    self.textSetPsi.SetValue(str(self.currImageFile.xysmcList[self.pickedRectID][2]))  #
                    self.textSetFom.SetValue(str(self.currImageFile.xysmcList[self.pickedRectID][3]))  #
                self.panelP.Refresh()
                self.panelM.Refresh()  # when you release the left mouse on a particle int he particle panel, it highlights that particle with a square
                goon = False
            i += 1

    def OnKeyUpP(self, event):
        if len(self.imageFiles) == 0:
            return
        pt = event.GetPosition()
        keycode = event.GetKeyCode()
        # print 	"P keycode =", keycode
        if (keycode == wx.WXK_LEFT or keycode == wx.WXK_PAGEUP):
            self.pickedRectID = self.pickedRectID - 1
            if self.pickedRectID < 0:
                self.pickedRectID = 0
            self.GetParent().statusBar.SetStatusText('Selected particle ID -1: %d' % (self.pickedRectID + 1), 2)
            winsizex, winsizey = self.panelM.GetSize()
            self.bitmap_x = int(winsizex / 2.0 - self.mag * self.currImageFile.xysmcList[self.pickedRectID][0])
            self.bitmap_y = int(winsizey / 2.0 - self.mag * self.currImageFile.xysmcList[self.pickedRectID][1])

            # when you navigate to a particle in the particle panel, its psi and fom are displayed on the top right corner.
            self.textSetPsi.SetValue(str(self.currImageFile.xysmcList[self.pickedRectID][2]))  #
            self.textSetFom.SetValue(str(self.currImageFile.xysmcList[self.pickedRectID][3]))  #
        if (keycode == wx.WXK_RIGHT or keycode == wx.WXK_PAGEDOWN):
            self.pickedRectID = self.pickedRectID + 1
            if self.pickedRectID > len(self.particleRectList) - 1:
                self.pickedRectID = len(self.particleRectList) - 1
            self.GetParent().statusBar.SetStatusText('Selected particle ID +1: %d' % (self.pickedRectID + 1), 2)
            winsizex, winsizey = self.panelM.GetSize()
            self.bitmap_x = int(winsizex / 2.0 - self.mag * self.currImageFile.xysmcList[self.pickedRectID][0])
            self.bitmap_y = int(winsizey / 2.0 - self.mag * self.currImageFile.xysmcList[self.pickedRectID][1])
            # when you navigate to a particle in the particle panel, its psi and fom are displayed on the top right corner.
            self.textSetPsi.SetValue(str(self.currImageFile.xysmcList[self.pickedRectID][2]))  #
            self.textSetFom.SetValue(str(self.currImageFile.xysmcList[self.pickedRectID][3]))  #
        if (keycode == 68) or (keycode == wx.WXK_DELETE) or (keycode == wx.WXK_NUMPAD_DELETE):  # The d key
            length_self_particleRectList = 0
            length_self_particleRectList = len(self.particleRectList)
            if self.pickedRectID < 0:
                self.pickedRectID = 0
            elif self.pickedRectID > length_self_particleRectList - 1:
                self.pickedRectID = length_self_particleRectList - 1
            else:
                self.pickedRectID = self.pickedRectID
            self.particleList.pop(self.pickedRectID)
            self.currImageFile.xysmcList.pop(self.pickedRectID)
            self.GetParent().statusBar.SetStatusText('One particle deleted. Current total %d' % len(self.particleList),
                                                     2)
            # Refresh combo_box to show particle number
            self.comboFiles.Delete(self.currFile)
            newitem = '[%d] %s [%d %s](%d %s)' % (
            self.currFile + 1, os.path.basename(self.currImageFile.path), len(self.currImageFile.xysmcListRef),
            self.currImageFile.refCoordSource, len(self.currImageFile.xysmcList), self.currImageFile.edtCoordSource)
            self.comboFiles.Insert(newitem, self.currFile)
            self.comboFiles.SetSelection(self.currFile)
            if self.pickedRectID > length_self_particleRectList - 2:  # if you deleted the last particle (=length_self_particleRectList - 1)
                self.pickedRectID = length_self_particleRectList - 2
            elif self.pickedRectID < 0:
                self.pickedRectID = 0
            else:
                self.pickedRectID = self.pickedRectID
            winsizex, winsizey = self.panelM.GetSize()
            self.bitmap_x = int(winsizex / 2.0 - self.mag * self.currImageFile.xysmcList[self.pickedRectID][0])
            self.bitmap_y = int(winsizey / 2.0 - self.mag * self.currImageFile.xysmcList[self.pickedRectID][1])
            length_self_particleRectList = 0
        self.panelP.Refresh()
        self.panelM.Refresh()

    def OnRightDownP(self, event):
        if len(self.particleList) == 0:
            return
        self.side_dragStartPos = event.GetPosition()
        if wx.__version__.startswith("3"):
            self.panelP.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))  # wxPython 3.0
        elif wx.__version__.startswith("4"):
            self.panelP.SetCursor(wx.Cursor(wx.CURSOR_ARROW))  # wxPython 4.0

    def OnRightUpP(self, event):
        if len(self.particleList) == 0:
            return
        if wx.__version__.startswith("3"):
            self.panelP.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))  # wxPython 3.0
        elif wx.__version__.startswith("4"):
            self.panelP.SetCursor(wx.Cursor(wx.CURSOR_ARROW))  # wxPython 4.0
        pt = event.GetPosition()
        pt_montage = pt - (self.particleDraw_x, self.particleDraw_y)
        i = 0  # Hit_test
        goon = True
        contains = False
        while i < len(self.particleRectList) and goon:
            if wx.__version__.startswith("3"):
                contains = self.particleRectList[i].InsideXY(pt_montage[0], pt_montage[1])  # wxPython 3.0
            elif wx.__version__.startswith("4"):
                contains = self.particleRectList[i].Contains(pt_montage[0], pt_montage[1])  # wxPython 4.0
            if contains == True:
                if event.ShiftDown():  # Delete this and ALL following particles!
                    rmtotal = len(self.particleList) - i
                    self.particleList = self.particleList[:i]
                    self.currImageFile.xysmcList = self.currImageFile.xysmcList[:i]
                    self.pickedRectID = -1
                    self.GetParent().statusBar.SetStatusText('%d particles deleted. Current total %d' % (rmtotal, i), 2)
                    self.comboFiles.Delete(self.currFile)  # Refresh combo_box to show particle number
                    newitem = '[%d] %s [%d %s](%d %s)' % (
                    self.currFile + 1, os.path.basename(self.currImageFile.path), len(self.currImageFile.xysmcListRef),
                    self.currImageFile.refCoordSource, len(self.currImageFile.xysmcList),
                    self.currImageFile.edtCoordSource)
                    self.comboFiles.Insert(newitem, self.currFile)
                    self.comboFiles.SetSelection(self.currFile)
                self.panelP.Refresh()
                self.panelM.Refresh()
                goon = False
            i += 1

    def OnMotionP(self, event):
        if len(self.particleList) == 0:
            return
        pt = event.GetPosition()
        if event.RightIsDown():  # Moving the micrograph
            diff = pt - self.side_dragStartPos
            if abs(diff[0]) > 2 or abs(diff[1]) > 2:
                self.particleDraw_x += diff[0]
                self.particleDraw_y += diff[1]
                self.side_dragStartPos[0] += diff[0]
                self.side_dragStartPos[1] += diff[1]
            self.particleFreePos = True  # Free positioning of the montage
        self.panelP.Refresh()

    def OnWheelP(self, event):
        if len(self.particleList) == 0:
            return
            rotation = event.GetWheelRotation()  # -120: rotate down, shrink image; +120: up, enlarge
        mboxSize = int(self.boxSize * self.particleMag)
        if mboxSize < 20:
            if rotation < 0:
                return  # Can not make any smaller
        if rotation < 0:
            self.particleMag += -0.1
        else:
            self.particleMag += 0.1
        self.particleFreePos = False  # Reset the montage position
        self.panelP.Refresh()

    def OnLeftDclickP(self, event):
        # Open the next or previous image file in the list
        if len(self.imageFiles) == 0:
            return
        if event.ShiftDown():  # Avoid confusion with fast click of "Shift + Left" (to remove particles)
            return
        self.SaveAllCoordinates()  # Autosave all particles
        doloadimg = False
        if event.ControlDown():
            if self.currFile > 0:
                self.currFile = self.currFile - 1
                doloadimg = True
        else:
            if self.currFile < (len(self.imageFiles) - 1):
                self.currFile += 1
                doloadimg = True
        if doloadimg:
            self.comboFiles.SetSelection(self.currFile)
            self.currImageFile = self.imageFiles[self.currFile]
            self.LoadImage()


class FespPanelT(wx.Panel):  ######## Class 5: Fesp Toolbar ########
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.ID_comboFiles = 231
        # self.ID_buttonClose = 229
        self.ID_buttonNext = 229
        self.ID_buttonFitWindows = 233
        self.ID_buttonMag = 235
        self.ID_comboSigma = 237
        self.ID_buttonContrast = 241
        self.ID_buttonInvert = 242
        self.ID_buttonResize = 245
        self.ID_buttonSaveCurrentCoordinates = 247
        self.ID_buttonDisplayBox = 261
        self.ID_buttonDisplayPsi = 262
        self.ID_textSetPsi = 263
        self.ID_textSetFom = 264

        self.GetParent().comboFiles = wx.ComboBox(self, self.ID_comboFiles, size=(30, -1), choices=[],
                                                  style=wx.CB_READONLY)
        # self.GetParent().buttonClose = wx.Button(self, self.ID_buttonClose, 'Close Curr',size=(20, -1))
        self.GetParent().buttonNext = wx.Button(self, self.ID_buttonNext, 'Next Mic', size=(20, -1))
        self.GetParent().buttonFitWindows = wx.Button(self, self.ID_buttonFitWindows, 'Fit', size=(20, -1))
        self.GetParent().textMag = wx.TextCtrl(self, -1, str(magS), size=(20, -1))  # used in OnButtonMagT()
        self.GetParent().buttonMag = wx.Button(self, self.ID_buttonMag, 'Mag', size=(20, -1))
        sigmaChoices = ['Sigma 0.5', 'Sigma 1', 'Sigma 1.5', 'Sigma 2', 'Sigma 2.5', 'Sigma 3', 'Sigma 3.5', 'Sigma 4',
                        'Sigma 5']
        self.GetParent().sigmaValues = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # used in OnSigma()
        self.GetParent().comboSigma = wx.ComboBox(self, self.ID_comboSigma, size=(20, -1), choices=sigmaChoices,
                                                  style=wx.CB_READONLY)
        self.GetParent().comboSigma.SetSelection(sigmaChoiceS)
        # self.GetParent().spinContrastMin = wx.SpinCtrl(self, -1, '100', size=(20, -1), min=0, max=1000) # used in multiple functions
        # self.GetParent().spinContrastMax = wx.SpinCtrl(self, -1, '600', size=(20, -1), min=0, max=1000) # used in multiple functions
        # self.GetParent().buttonContrast = wx.Button(self, self.ID_buttonContrast, '>Contrast<', size=(40, -1))
        # self.GetParent().spinBright = wx.SpinCtrl(self, -1, '0', size=(20, -1), min=-255, max=255)      # used in multiple functions
        self.GetParent().buttonInvert = wx.Button(self, self.ID_buttonInvert, 'Inv', size=(10, -1))
        self.GetParent().textBoxSizeRef = wx.TextCtrl(self, -1, str(refPtclSizeS), size=(20, -1))
        self.GetParent().textBoxSize = wx.TextCtrl(self, -1, str(pickPtclSizeS), size=(20, -1))
        self.GetParent().buttonResize = wx.Button(self, self.ID_buttonResize, 'Resize', size=(20, -1))
        self.GetParent().textEraserRadius = wx.TextCtrl(self, -1, str(eraserRadiusS), size=(10, -1))
        self.GetParent().buttonSaveCoordinates = wx.Button(self, self.ID_buttonSaveCurrentCoordinates, 'Save Curr',
                                                           size=(40, -1))
        self.GetParent().buttonDisplayBox = wx.Button(self, self.ID_buttonDisplayBox, 'Box', size=(5, -1))
        self.GetParent().buttonDisplayPsi = wx.Button(self, self.ID_buttonDisplayPsi, 'Psi', size=(5, -1))
        self.GetParent().textSetPsi = wx.TextCtrl(self, self.ID_textSetPsi, str(defaultPsiS), size=(20, -1))
        self.GetParent().textSetFom = wx.TextCtrl(self, self.ID_textSetFom, str(defaultFomS), size=(20, -1))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)

        sizer1.Add(self.GetParent().comboFiles, 10, wx.EXPAND)
        # sizer1.Add(self.GetParent().buttonClose, 2, wx.EXPAND)
        sizer1.Add(self.GetParent().buttonNext, 2, wx.EXPAND)

        sizer2.Add(self.GetParent().buttonFitWindows, 1, wx.EXPAND)
        sizer2.Add(self.GetParent().textMag, 1, wx.EXPAND)
        sizer2.Add(self.GetParent().buttonMag, 1, wx.EXPAND)

        sizer3.Add(self.GetParent().comboSigma, 2, wx.EXPAND)
        # sizer3.Add(self.GetParent().spinContrastMin, 1, wx.EXPAND)
        # sizer3.Add(self.GetParent().spinContrastMax, 1, wx.EXPAND)
        # sizer3.Add(self.GetParent().buttonContrast, 2, wx.EXPAND)
        # sizer3.Add(self.GetParent().spinBright, 1, wx.EXPAND)
        sizer3.Add(self.GetParent().buttonInvert, 1, wx.EXPAND)

        sizer4.Add(self.GetParent().textBoxSizeRef, 1, wx.EXPAND)
        sizer4.Add(self.GetParent().textBoxSize, 1, wx.EXPAND)
        sizer4.Add(self.GetParent().buttonResize, 1, wx.EXPAND)
        sizer4.Add(self.GetParent().textEraserRadius, 1, wx.EXPAND)
        sizer4.Add(self.GetParent().buttonSaveCoordinates, 2, wx.EXPAND)
        sizer4.Add(self.GetParent().buttonDisplayBox, 1, wx.EXPAND)  #
        sizer4.Add(self.GetParent().buttonDisplayPsi, 1, wx.EXPAND)  #
        sizer4.Add(self.GetParent().textSetPsi, 1, wx.EXPAND)  #
        sizer4.Add(self.GetParent().textSetFom, 1, wx.EXPAND)  #

        sizer.Add(sizer1, 6, wx.EXPAND)
        sizer.Add(sizer2, 2, wx.EXPAND | wx.LEFT, 10)
        sizer.Add(sizer3, 2, wx.EXPAND | wx.LEFT, 10)
        sizer.Add(sizer4, 5, wx.EXPAND | wx.LEFT, 10)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_COMBOBOX, self.GetParent().OnComboFilesT, id=self.ID_comboFiles)
        # self.Bind(wx.EVT_BUTTON,   self.GetParent().OnButtonCloseT, id = self.ID_buttonClose)
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnButtonNextT, id=self.ID_buttonNext)
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnButtonFitWindowsT, id=self.ID_buttonFitWindows)
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnButtonMagT, id=self.ID_buttonMag)
        self.Bind(wx.EVT_COMBOBOX, self.GetParent().OnComboSigmaT, id=self.ID_comboSigma)
        # self.Bind(wx.EVT_BUTTON,   self.GetParent().OnButtonContrastT, id = self.ID_buttonContrast)
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnButtonInvertT, id=self.ID_buttonInvert)
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnButtonResizeT, id=self.ID_buttonResize)
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnButtonSaveCurrentCoordinatesT,
                  id=self.ID_buttonSaveCurrentCoordinates)
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnButtonDisplayBoxT, id=self.ID_buttonDisplayBox)  #
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnButtonDisplayPsiT, id=self.ID_buttonDisplayPsi)  #
        self.Bind(wx.EVT_TEXT, self.GetParent().OnTextSetPsi4CurrPtclT, id=self.ID_textSetPsi)  #
        self.Bind(wx.EVT_TEXT, self.GetParent().OnTextSetFom4CurrPtclT, id=self.ID_textSetFom)  #


class FespPanelP(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)


class FespPanelM(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)


class MyApp(wx.App):
    def OnInit(self):
        frame = Fesp(None, -1, '')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


app = MyApp(0)
app.MainLoop()
