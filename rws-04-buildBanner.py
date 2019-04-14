#!/usr/bin/env python
#
#   File = rws-04-buildBanner.py
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

def build_banner(inputImage, inputDrawable, tgtPath):
    # create banner image
    bannerImage = gimp.Image(1920, 384, RGB)

    inputFileList = os.listdir(tgtPath)
    srcFileList = []

    # Get the list of all banner files in the working directory
    for filename in inputFileList:
        filename = filename.lower()
        if filename.count('_bnr.xcf') > 0:
            srcFileList.append(filename)

    srcFileList = reversed(sorted(srcFileList))
    nextStartPixel = 0
    layerNumber = 1
    skippedLatest = 0

    # Loop on winner images
    for srcFilename in srcFileList:
        # Skip the first winner because it's sidebar
        if skippedLatest < 1:
            skippedLatest = 1
            continue

        srcFile = os.path.join(tgtPath, srcFilename)
        winnerLayer = pdb.gimp_file_load_layer(bannerImage, srcFile)
        winnerLayer.name = srcFilename[0:10]
        bannerImage.add_layer(winnerLayer, 0)
        winnerLayer.set_offsets(nextStartPixel,0)

        layerNumber = layerNumber + 1
        nextStartPixel = nextStartPixel + winnerLayer.width

        if nextStartPixel > 1920:
            break
    # End for loop

    bannerImage.flatten()
    bannerFile = os.path.join(tgtPath, 'banner.jpg')
    pdb.file_jpeg_save(bannerImage, bannerImage.active_layer, bannerFile, bannerFile, 0.9, 0, 0, 0, "", 0, 0, 0, 0)

############################################################################

register (
    "python_fu_build_banner",              # Name registered in Procedure Browser
    "Build the banner",                    # Widget title
    "Build the banner",                    # Help
    "BourbonInExile@gmail.com",            # Author
    "BourbonInExile@gmail.com",            # Copyright Holder
    "Feb 2019",                            # Date
    "<Image>/Reddit/4 - Build the Banner", # Menu Location
    "",                   # Image Type - No image required
    [ ( PF_DIRNAME, "tgtPath", "Working Directory:", "" ), ],  # Params
    [],  # Results
    build_banner,       # Matches to name of function being defined
    )   # End register

main()
