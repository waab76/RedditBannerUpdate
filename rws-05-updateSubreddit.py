#!/usr/bin/env python
# coding: utf-8
#
#   File = rws-updateSubreddit.py
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
import praw
import reddit_config as cfg

def update_subreddit(inputImage, inputDrawable, tgtPath):
    theSub = praw.Reddit(client_id=cfg.client_id,
                             client_secret=cfg.client_secret,
                             user_agent=cfg.user_agent,
                             username=cfg.username,
                             password=cfg.password
                             ).subreddit('WetShaving')
    stylesheet = theSub.stylesheet

    # Update the sidebar image
    stylesheet.delete_image("sidebar-img")
    stylesheet.upload("sidebar-img", os.path.join(tgtPath, "sidebar-img.jpg"))

    # Update the banner image
    stylesheet.delete_image("banner")
    stylesheet.upload("banner", os.path.join(tgtPath, "banner.jpg"))

    # Trigger the update
    stylesheet.update(cfg.css_sheet, "Auto-updating sidebar/banner")

    # Update the sidebar widget (New Reddit)
    widgets = theSub.widgets
    image_widget = None

    for widget in widgets.sidebar:
        if isinstance(widget, praw.models.ImageWidget):
            image_widget = widget
            break

    imageData = [{'width': 1000, 'height': 1000, 'linkUrl': '',
             'url': widgets.mod.upload_image(os.path.join(tgtPath, 'sidebar-img.jpg'))}]
    image_widget.mod.update(data=imageData)

    # Update the banner (New Reddit)
    stylesheet.upload_banner(os.path.join(tgtPath, "banner.jpg"))

############################################################################

register (
    "python_fu_update_subreddit",             # Name registered in Procedure Browser
    "", # Widget title
    "", # Help
    "BourbonInExile@gmail.com",         # Author
    "BourbonInExile@gmail.com",         # Copyright Holder
    "Feb 2019",           # Date
    "<Image>/Reddit/5 - Update Subreddit",     # Menu Location
    "",                   # Image Type - No image required
    [ ( PF_DIRNAME, "tgtPath", "Working Directory:", ""), ],  # Params
    [],  # Results
    update_subreddit,       # Matches to name of function being defined
    )   # End register

main()
