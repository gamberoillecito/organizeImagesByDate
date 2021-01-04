import subprocess
import os
import sys
import argparse
import re
import shutil
from findExtensions import getAllExtensions
# the following lists contain the extensions for videos and images
videoExt = [
	"3g2",
	"3gp",
	"aaf",
	"asf",
	"avchd",
	"avi",
	"drc",
	"flv",
	"m2v",
	"m4p",
	"m4v",
	"mkv",
	"mng",
	"mov",
	"mp2",
	"mp4",
	"mpe",
	"mpeg",
	"mpg",
	"mpv",
	"mxf",
	"nsv",
	"ogg",
	"ogv",
	"qt",
	"rm",
	"rmvb",
	"roq",
	"svi",
	"vob",
	"webm",
	"wmv",
	"yuv",
	"mts"
]
imageExt = [
 "ase",
 "art",
 "bmp",
 "blp",
 "cd5",
 "cit",
 "cpt",
 "cr2",
 "cut",
 "dds",
 "dib",
 "djvu",
 "egt",
 "exif",
 "gif",
 "gpl",
 "grf",
 "icns",
 "ico",
 "iff",
 "jng",
 "jpeg",
 "jpg",
 "jfif",
 "jp2",
 "jps",
 "lbm",
 "max",
 "miff",
 "mng",
 "msp",
 "nitf",
 "ota",
 "pbm",
 "pc1",
 "pc2",
 "pc3",
 "pcf",
 "pcx",
 "pdn",
 "pgm",
 "PI1",
 "PI2",
 "PI3",
 "pict",
 "pct",
 "pnm",
 "pns",
 "ppm",
 "psb",
 "psd",
 "pdd",
 "psp",
 "px",
 "pxm",
 "pxr",
 "qfx",
 "raw",
 "rle",
 "sct",
 "sgi",
 "rgb",
 "int",
 "bw",
 "tga",
 "tiff",
 "tif",
 "vtf",
 "xbm",
 "xcf",
 "xpm",
 "3dv",
 "amf",
 "ai",
 "awg",
 "cgm",
 "cdr",
 "cmx",
 "dxf",
 "e2d",
 "egt",
 "eps",
 "fs",
 "gbr",
 "odg",
 "svg",
 "stl",
 "vrml",
 "x3d",
 "sxd",
 "v2d",
 "vnd",
 "wmf",
 "emf",
 "art",
 "xar",
 "png",
 "webp",
 "jxr",
 "hdp",
 "wdp",
 "cur",
 "ecw",
 "iff",
 "lbm",
 "liff",
 "nrrd",
 "pam",
 "pcx",
 "pgf",
 "sgi",
 "rgb",
 "rgba",
 "bw",
 "int",
 "inta",
 "sid",
 "ras",
 "sun",
 "tga",
 "nef",
 # following extensions are RAW
 "3fr",
 "ari",
 "arw",
 "bay",
 "braw",
 "crw",
 "cr2",
 "cr3",
 "cap",
 "data",
 "dcs",
 "dcr",
 "dng",
 "drf",
 "eip",
 "erf",
 "fff",
 "gpr",
 "iiq",
 "k25",
 "kdc",
 "mdc",
 "mef",
 "mos",
 "mrw",
 "nef",
 "nrw",
 "obm",
 "orf",
 "pef",
 "ptx",
 "pxn",
 "r3d",
 "raf",
 "raw",
 "rwl",
 "rw2",
 "rwz",
 "sr2",
 "srf",
 "srw",
 "tif",
 "x3f"
]


# creates the part of the exiftool command to only consider the extensions in extensionList
def getOnlyExt(extensionList):
	s = ' '
	if extensionList != None:
		for i in extensionList:
			s += '-ext ' + i + ' '
	return(s)

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("-s", "--source",
				help="The absolute PATH of the folder that contains the images.")
	parser.add_argument("-d", "--destination",
				help="The absolute PATH of the folder where to put the YEARs folders.")
	parser.add_argument("-f", "--fileTypeToUse", choices=['photos', 'videos'],
				help="Set this to 'videos' to move videos only or to 'photos' to move photos only")
	args = parser.parse_args()

	if not os.path.isdir(args.source):
		print("The source folder is not valid")
		sys.exit(1)

	if not os.path.isdir(args.destination):
		print("The destination folder is not valid")
		sys.exit(1)

	# set the variable desiredExt so that it contains the desired variables
	if args.fileTypeToUse == 'videos':
		desiredExt = videoExt
	elif args.fileTypeToUse == 'photos':
		desiredExt = imageExt
	else:
		desiredExt = None


	restrictExt = getOnlyExt(desiredExt) # contains the part of the command to restrict extensions

	# compares all the extensions in the source folder to the desired extensions
	# and tells the user which will be ignored
	if args.fileTypeToUse != None:
		print("I found these extensions in the source folder:")
		extensionsInSource = getAllExtensions(args.source)
		print(*extensionsInSource, sep=", ")
		print()
		extThatWillBeExcluded = []
		for e in extensionsInSource:
			if not e.lower() in [k.lower() for k in desiredExt]:
				extThatWillBeExcluded.append(e)

		print("The following extensions are in the source folder but will be ignored:")
		print(*extThatWillBeExcluded, sep=", ")

	# creates the exiftool command
	command = r'exiftool -m ' + restrictExt + ' -r -d ' + args.destination + '\%Y/%m/%d/%Y-%m-%d_%H%M%S%%c.%%e "-filename<filemodifydate" "' + args.source + '" -o fakedir'
	print ("\nThe command that will be executed is:\n")
	print(command + '\n')

	a = input("Press ENTER to continue... ")
	try:
		subprocess.run(command)
		pass
	except subprocess.CalledProcessError:
		sys.exit(1)

	print()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(1)
