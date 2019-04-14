#!/usr/bin/env python
#
#   File = rws-00-fullSubredditRefresh.py
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

from gimpfu import *
import os

def full_subreddit_refresh(inputImage, inputDrawable, tgtPath):
    # Cleanup old sidebar and banner files before starting
    oldSidebarFile = os.path.join(tgtPath, 'sidebar-img.jpg')
    oldBannerImage = os.path.join(tgtPath, 'banner.jpg')
    os.remove(oldSidebarFile)
    os.remove(oldBannerImage)

    pdb.python_fu_get_winners(inputImage, inputDrawable, tgtPath)

    pdb.python_fu_gen_sidebar_image(inputImage, inputDrawable, tgtPath)

    pdb.python_fu_gen_banner_images(inputImage, inputDrawable, tgtPath)

    pdb.python_fu_build_banner(inputImage, inputDrawable, tgtPath)

    pdb.python_fu_update_subreddit(inputImage, inputDrawable, tgtPath)

############################################################################

register (
    "python_fu_full_subreddit_refresh",   # Name registered in Procedure Browser
    "r/WetShaving weekly image refresh",  # Widget title
    "Run through all the steps necessary for weekly updates to r/WetShaving's sidebar and banner images", # Help
    "BourbonInExile@gmail.com",           # Author
    "BourbonInExile@gmail.com",           # Copyright Holder
    "Feb 2019",                           # Date
    "<Image>/Reddit/0 - Full Banner Run", # Menu Location
    "",                                   # Image Type - No image required
    [ ( PF_DIRNAME, "tgtPath", "Working Directory:", ""), ],  # Params
    [],  # Results
    full_subreddit_refresh,       # Matches to name of function being defined
    )   # End register

main()
