# JKConvert
Converts Jedi Knight JKL maps to OBJ

<img title="Caesars Palace" src="img\Caesars2.png" width="600">

This was my first "real" Python project outside of following tutorials. It's quite a mess but it does the job. For materials, you will have to extract and convert them to BMP before running this script. It relies on being pointed to a directory with all of the BMP files. 

The file paths are hardcoded in this script, but should be easy enough to figure out. 

All of the conversion tools I had previously used had issues converting the Caesar's Palace custom map, so my goal was to have it work here. Good news is, it does! Along with all of the other maps I threw at it!

I had no intention on sharing this since the code is sloppy and it was a personal learning project, but I might as well. I'd like to revisit it one day and have it read in GOB files/convert textures on its own instead of relying on extracting BMPs, but that's for another day.

I am not sure if this is the most up to date version of the code. The geometry may be flipped 90 degrees on the Y axis, but that should be easy enough to fix.
