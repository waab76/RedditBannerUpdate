#!/usr/bin/env python
#
#   File = rws-03-genBannerImages.py
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
import re

def gen_banner_images(inputImage, inputDrawable, tgtPath):
    inputFileList = os.listdir(tgtPath)
    srcFileList = []

    jpgXform = re.compile('\.jpg', re.IGNORECASE)

    # Get the list of all .jpg files in the source directory
    for filename in inputFileList:
        filename = filename.lower()
        if filename.count('.jpg') > 0 and filename.count('sidebar-img') < 1 and filename.count('banner') < 1:
            srcFileList.append(filename)

    # Loop on jpegs, open each & save as xcf
    for srcFile in srcFileList:
        bannerFilename = jpgXform.sub('_bnr.xcf', srcFile)

        # Open the .jpg image
        srcFile = os.path.join(tgtPath, srcFile)
        theImage = pdb.file_jpeg_load(srcFile, srcFile)
        theLayer = theImage.active_layer

        aspectRatio = float(theLayer.height) / theLayer.width

        # Don't overwrite existing, might be work in Progress
        if bannerFilename not in inputFileList:
            bannerFile = os.path.join(tgtPath, bannerFilename)
            targetHeight = 394
            targetWidth = int(round(targetHeight/aspectRatio))
            theLayer.scale(targetWidth, targetHeight)
            theImage.resize(targetWidth, targetHeight, 0, 0)
            pdb.gimp_xcf_save(0, theImage, theLayer, bannerFile, bannerFile)

        pdb.gimp_image_delete(theImage)
    # End for loop

############################################################################

register (
    "python_fu_gen_banner_images",                     # Name registered in Procedure Browser
    "Convert winner JPG to banner XCF",                # Widget title
    "Convert selected directory of .jpg images into banner-sized .xcf images", # Help
    "BourbonInExile@gmail.com",                        # Author
    "BourbonInExile@gmail.com",                        # Copyright Holder
    "Feb 2019",                                        # Date
    "<Image>/Reddit/3 - Generate Banner-sized Images", # Menu Location
    "",                   # Image Type - No image required
    [ ( PF_DIRNAME, "tgtPath", "Working Directory:", "" ), ],  # Params
    [],  # Results
    gen_banner_images,       # Matches to name of function being defined
    )   # End register

main()
