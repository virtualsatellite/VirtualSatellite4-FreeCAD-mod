# Virtual Satellite 4 - FreeCAD Module - Alpha

Virtual Satellite 4 - FreeCAD Module is an extension for [FreeCAD](https://freecadweb.org/), an Open Source 3D Parametric Modeler.
This extension allows to create a round-trip engineering workflow with Virtual Satellite.

**Note:** This extension is still under development. It is not ready for productive use and is subject to constant change.

## Project Status

| Master | Development | 
|:------:|:-----------:| 
|[![Master][master-status]][master-builds]|[![Development][development-status]][development-builds]| 

[master-status]: https://travis-ci.com/virtualsatellite/VirtualSatellite4-FreeCAD-mod.svg?branch=master 

[master-builds]: https://travis-ci.com/virtualsatellite/VirtualSatellite4-FreeCAD-mod 

[development-status]: https://travis-ci.com/virtualsatellite/VirtualSatellite4-FreeCAD-mod.svg?branch=development 

[development-builds]: https://travis-ci.com/virtualsatellite/VirtualSatellite4-FreeCAD-mod

## Purpose

Virtual Satellite 4 FreeCAD Module is an extension to FreeCAD. FreeCAD is an open source mechanical engineering CAD tool. The extension can be easily installed to FreeCAD. It allows to import structural configuration information into FreeCAD and keep it consistently synchronized with Virtual Satellite 

## Requirements 

This program is based on FreeCAD and Python. The following infrastructure is required:
 - FreeCAD 0.18 and higher (64bit)
 - A2plus Workbench 0.4.26 and higher
 - Virtual Satellite 4
 
## Quickstart for Users

If you just want to use Virtual Satellite feel free to download it from the [Releases](https://github.com/virtualsatellite/VirtualSatellite4-FreeCAD-mod/releases) section here on GitHub.

## Quickstart for Developers

To set up your Eclipse IDE, run the Apache ANT *build.xml*. It works for Windows and Linux systems.  
The Ant script is performing the following steps:
1. Install FreeCAD.
2. Install the A2plus Workbench.
3. Apply need patches (To fix some interim bugs in FreeCAD)

If you have FreeCAD already installed and you only want to install this extension, please follow these steps:
1. Find the default configuration path to FreeCAD (e.g. `~/.FreeCAD/` on Linux)   
2. Type `cd path/to/your/.FreeCAD/Mod` to change directory  to your default configuration _Mod_ subdirectory.   
3. Download the extension zip file (from [Releases](https://github.com/virtualsatellite/VirtualSatellite4-FreeCAD-mod/releases)) into this directory and unzip it.   
4. Start or Restart FreeCAD.

**Note:** You can get the configuration directory by using the FreeCAD's python console: `FreeCAD.ConfigGet("UserAppData")` 

**Note:** A `git clone` method compared to copying and unzipping is preferred. Updates are conveniently done with a simple `git fetch` instead of needing to re-download the zip file and unzipping it.  


The Virtual Satellite Workbench is now available in FreeCAD

## Travis CI and Releases

Travis CI is set-up to start a build job for every branch and every new commit to the repository. It executes all relevant tests. Making a successful pull-request into development requires all tests to pass.

Starting a Travis CI job on development deploys all relevant artifacts.

For creating a new release, create a tag starting with *Release_* on the *master* branch. All artifacts are automatically deployed.

## Provided Features

- A new Virtual Satellite Workbench
- Functionality to upload a design to Virtual Satellite.
- Functionality to download a design from Virtual Satellite.

## Contributing

We are happy to receive your contributions. Nevertheless in such a big project there is a lot to respect and to obey. 
One thing to respect are legal requirements such as authorship rights and privacy protection. 
Therefore, before we can accept your contributions we need you to sign our *Contributor License Agreement (CLA)*.

Please follow the process described in *[Virtual Satellite 4 - Core](https://github.com/virtualsatellite/VirtualSatellite4-Core)* to become an authorized contributor. 

Once you are an authorized committer feel free to contribute. We will not activate your account within our organization. Therefore use Pull-Requests to contribute:

1. Create your own fork of the project.
2. Apply your changes.
3. Create a pull-request of your change to our development branch.

To increase chance that we accept your pull-request, make sure all tests are working. The best indicator is the Travis CI job. Next we will review your pull-request, give comments and maybe accept it.

## Third party dependencies

The Apache Ant script for the build process has following third party dependencies:
- Apache Compress Ant Library: [Apache License 2.0](http://www.apache.org/licenses/)
- Apache Commons Compress: [Apache License 2.0](http://www.apache.org/licenses/)
- XZ for Java: public domain

The final FreeCAD Module (see [Releases](https://github.com/virtualsatellite/VirtualSatellite4-FreeCAD-mod/releases)) does NOT have those third party dependencies.

## License

Copyright (C) 2019 by

   DLR (German Aerospace Center),
   Software for Space Systems and interactive Visualization
   Braunschweig, Germany

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
