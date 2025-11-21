#!/usr/bin/env python
#
# Copyright (c) 2025 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.shortcuts import render
from django.http import Http404

from omeroweb.decorators import login_required


# login_required: if not logged-in, will redirect to webclient
# login page. Then back to here, passing in the 'conn' connection
# and other arguments **kwargs.
@login_required()
def index(request, conn=None, **kwargs):
    # We can load data from OMERO via Blitz Gateway connection.
    # See https://docs.openmicroscopy.org/latest/omero/developers/Python.html
    experimenter = conn.getUser()

    # A dictionary of data to pass to the html template
    context = {
        "firstName": experimenter.firstName,
        "lastName": experimenter.lastName,
        "experimenterId": experimenter.id,
    }
    # print can be useful for debugging, but remove in production
    # print('context', context)

    # Render the html template and return the http response
    return render(request, "omero_demo2025/index.html", context)


@login_required()
def tracker(request, conn=None, **kwargs):
    """Track panning of images from iviewer.

    Expect ?image=123 as GET parameter
    """
    image_id = request.GET.get("image", None)
    if image_id is None:
        raise Http404("Use ?image=123 to specify image id")
    image = conn.getObject("Image", image_id)
    if image is None:
        raise Http404(f"Image with id={image_id} not found")

    context = {
        "imageId": image_id,
        "name": image.getName(),
        "width": image.getSizeX(),
        "height": image.getSizeY(),
    }

    return render(request, "omero_demo2025/tracker.html", context)
