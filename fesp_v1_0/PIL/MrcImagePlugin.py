#
# The Python Imaging Library.
#
# MRC image file handling
#
# History:
# 2010-06-08    Created by Maofu Liao
#
# ----------------------------------------------------------------------
#
# Author: Maofu Liao (maofuliao@gmail.com)
#
# This program is free open-source software, licensed under the terms of 
# the GNU Public License version 3 (GPLv3). If you redistribute it and/or 
# modify it, please make sure the contribution of Maofu Liao 
# is acknowledged appropriately.
#
#
#

import Image, ImageFile
import struct

def isInt(f):
    try:
        i = int(f)
	if i == f:
		return True
	else:
		return False
    except:
        return False

def checkMrcHeader(t):
	# several criteria to check header

	# valid mode number
	mode = int(t[3])
	if not (mode in [0,1,2,3,4,6]):
		#print '%d not valid mode' % mode
		return False
	
	# axis must be 1,2,3
	for ct in [16,17,18]:
		axis = int(t[ct])
		if not (axis in [1,2,3]):
			#print 'bad axis'
			return False

	# min <= mean <= max
	#dmin = int(t[19])
	#dmax = int(t[20])
	#dmean = int(t[21])
	#if dmin > dmean or dmean > dmax:
	#	print 'bad maxmin'
	#	return False

	return True


class MrcImageFile(ImageFile.ImageFile):

	format = "MRC"
	format_description = "MRC image file"

	def _open(self):

		# ----- check header ----- #

		f = self.fp.read(24*4)	# up to "next": number of bytes in extended header
		f19 = f[:76]		# part to 19, before Min-Max-Mean
		try:
			self.bigendian = True
			t = struct.unpack('>19I', f19)
			valid = checkMrcHeader(t)
			if not valid:
				self.bigendian = False
				t = struct.unpack('<19I', f19)
				valid = checkMrcHeader(t)
			if not valid:
				raise SyntaxError, "not a valid MRC file"
		except struct.error:
			raise SyntaxError, "not a valid MRC file"

		if self.bigendian:	# "next": number of bytes in extended header
			self.extlen = int(struct.unpack('>1I', f[-4:])[0])
		else:
			self.extlen = int(struct.unpack('<1I', f[-4:])[0])

		# size in pixels (width, height)
		self.size = int(t[0]), int(t[1])
		# total image number
		self.nimages = int(t[2])


		# ----- mode selection ----- (1 byte = 8 bits) #

		mode = int(t[3])		# LW4_mode:	0        image : signed 8-bit bytes range -128 to 127
						#		1        image : 16-bit halfwords
						#		2        image : 32-bit reals
						#		3        transform : complex 16-bit integers
						#		4        transform : complex 32-bit reals
						#		6        image : unsigned 16-bit range 0 to 65535
		if mode == 0:
			self.rawmode = "I;8S"
			self.mode = "I"
			self.imgbytes = self.size[0] * self.size[1] * 1
		elif mode == 1:
			if self.bigendian:
				self.rawmode = "I;16BS"
			else:
				self.rawmode = "I;16S"
			self.mode = "I"
			self.imgbytes = self.size[0] * self.size[1] * 2
		elif mode == 2:
			if self.bigendian:
				self.rawmode = "F;32BF"
			else:
				self.rawmode = "F;32F"
			self.mode = "F"
			self.imgbytes = self.size[0] * self.size[1] * 4
		elif mode == 6:
			if self.bigendian:
				self.rawmode = "I;16B"
			else:
				self.rawmode = "I;16"
			self.mode = "I"
			self.imgbytes = self.size[0] * self.size[1] * 2
		else:
			raise SyntaxError, "MRC mode not supported"
		#print 'MRC mode=', self.rawmode, self.mode		# NOTE: "mode" and "rawmode" have different meaning!


		self.curFrame = 0
		self.__fp = self.fp	# NOTE: save the type of file_pointer, the actual pointing position seems not important
					# Looks like: "self.fp" will disappear if going to a funciton whose name is not started with "_" ...

		offset = 1024 + self.extlen
		self._load(offset)	# NOTE: "_" in the function name is essential!!!


	def _load(self, offset):
		# data descriptor
		self.tile = [("raw", (0,0)+self.size, offset, (self.rawmode, 0, -1))]
	
	def tell(self):
		if self.curFrame < 0:
			return 0
		else:
			return self.curFrame

	def seek(self, frame):
		if frame < 0:
			return
		if frame > (self.nimages - 1):
			raise EOFError, "attempt to seek past end of file"
		self.curFrame = frame
		self._seek(frame)

	def _seek(self, frame):
		# data descriptor
		self.fp = self.__fp
		offset = 1024 + self.extlen + frame * self.imgbytes	# first image: curFrame = 0
		self._load(offset)

Image.register_open("MRC", MrcImageFile)
Image.register_extension("MRC", ".mrc")

