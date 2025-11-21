
[![Actions Status](https://github.com/ome/omero-demo2025/workflows/OMERO/badge.svg)](https://github.com/ome/omero-demo2025/actions)


OMERO.omero_demo2025
==================================

demo app.

Installation
============

This section assumes that an OMERO.web is already installed. See [OMERO.web installation instructions]<https://github.com/ome/omero-web/blob/master/README.rst> for more details.

Installing from Pypi
--------------------

Install the app using [pip](<https://pip.pypa.io/en/stable/>) .

Ensure that you are running ``pip`` from the Python environment
where ``omero-web`` is installed. Depending on your install, you may need to
call ``pip`` with, for example: ``/path/to_web_venv/venv/bin/pip install ...``

    $ pip install -U omero-demo2025


Development mode
----------------

Install `omero-demo2025` in development mode as follows:

    # within your python venv:
    $ cd omero-demo2025
    $ pip install -e .

After installation either from [Pypi](https://pypi.org/) or in development mode, you need to configure the application.
To add the application to the `omero.web.apps` settings, run the following command:

Note the usage of single quotes around double quotes:

    $ omero config append omero.web.apps '"omero_demo2025"'

Optionally, add a link "OMERO Demo 2025" at the top of the webclient to
open the index page of this app:

    $ omero config append omero.web.ui.top_links '["OMERO Demo 2025", "omero_demo2025_index", {"title": "Open OMERO Demo 2025 in new tab", "target": "_blank"}]'


Now restart your `omero-web` server and go to
<http://localhost:4080/omero_demo2025/> in your browser.


OMERO.iviewer tracker page
==========================

This app includes a basic viewer to track the panning of the ivewer around an image.
For an image that is being viewed in iviewer, go to `/omero_demo2025/tracker?image=3111`.
When the user zooms in to 100%, red shading will be applied to the corresponding area
at 0.5 opacity and less if they zoom out.

NB: needs a custom build of iviewer containing this code:

```
+++ b/src/viewers/viewer/Viewer.js
@@ -602,6 +602,24 @@ class Viewer extends OlObject {
             view: view
         });
 
+        // listen for pan events... and broadcast them
+        const bc = new BroadcastChannel('viewer.pan');
+
+        this.viewer_.on('moveend', function(evt) {
+            console.log("Map moved END", evt);
+            // top-left is 0,0 - y is negative downwards
+            // console.log("center x,y", evt.frameState.viewState.center)
+            // console.log("size", evt.frameState.size)
+            let extent = evt.frameState.extent;
+            let [minX, minY, maxX, maxY] = extent;
+            console.log("extent", {minX, minY, maxX, maxY})
+            bc.postMessage({
+                imageId: this.id_,
+                extent: {minX, minY: -minY, maxX, maxY: -maxY},
+                size: evt.frameState.size,
+            });
+        }.bind(this));
+
         // enable bird's eye view
```


Further Info
============

1. This app was derived from [cookiecutter-omero-webapp](https://github.com/ome/cookiecutter-omero-webapp).
2. For further info on deployment, see [Deployment](https://docs.openmicroscopy.org/latest/omero/developers/Web/Deployment.html)


License
=======

This project, similar to many Open Microscopy Environment (OME) projects, is
licensed under the terms of the AGPL v3.


Copyright
=========

2025 University of Dundee

