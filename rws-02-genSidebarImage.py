#!/usr/bin/env python
#
#   File = rws-genSidebarImage.py
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the MIT license.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
############################################################################
#
from gimpfu import *
import os

def gen_sidebar_image(inputImage, inputDrawable, tgtPath):
    inputFileList = os.listdir(tgtPath)
    srcFileList = []

    # Get the list of all .jpg files in the source directory
    for filename in inputFileList:
        filename = filename.lower()
        if filename.count('.jpg') > 0:
            srcFileList.append(filename)

    srcFileList = reversed(sorted(srcFileList))
    for srcFile in srcFileList:
        sidebarFilename = "sidebar-img.jpg"

        # Open the .jpg image
        srcFile = os.path.join(tgtPath, srcFile)
        theImage = pdb.file_jpeg_load(srcFile, srcFile)
        theLayer = theImage.active_layer

        aspectRatio = float(theLayer.height) / theLayer.width

        sidebarFile = os.path.join(tgtPath, sidebarFilename)
        targetHeight = 500
        targetWidth = int(round(targetHeight/aspectRatio))
        theLayer.scale(targetWidth, targetHeight)
        theImage.resize(targetWidth, targetHeight, 0, 0)
        pdb.file_jpeg_save(theImage, theLayer, sidebarFile, sidebarFile, 0.9, 0, 0, 0, "", 0, 0, 0, 0)

        pdb.gimp_image_delete(theImage)
        break

############################################################################

register (
    "python_fu_gen_sidebar_image",               # Name registered in Procedure Browser
    "Create sidebar image",                      # Widget title
    "Create sidebar image",                      # Help
    "BourbonInExile@gmail.com",                  # Author
    "BourbonInExile@gmail.com",                  # Copyright Holder
    "Feb 2019",                                  # Date
    "<Image>/Reddit/2 - Generate Sidebar Image", # Menu Location
    "",                   # Image Type - No image required
    [ ( PF_DIRNAME, "tgtPath", "Working Directory:", "" ), ],  # Params
    [],  # Results
    gen_sidebar_image,       # Matches to name of function being defined
    )   # End register

main()
