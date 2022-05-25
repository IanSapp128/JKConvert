import os
from JKLFunctions import *

# Currently we are not generating face normals as they seem to be fine (with Official maps at least)
# We may have to change this later but at the moment I am avoiding this step.

# Known issues:
# Map is rotated 90 on the X axis. If I swap the numbers in the array the map is flipped horizontally.

ShouldNewLine = False
TextureList = []
TextureVertList = {}
TextureVertListUpdated = {}

WorldMaterials = []
WorldVerticies = []
WorldTextureVertices = []
WorldSurfaces = []
TextureBank = {}

ImageSizeY = 0
ImageSizeX = 0

# Texture Directory
TextDir = os.fsencode(str("PATH TO TEXTURES"))

# Input File
infile = open("PATH TO .JKL FILE", "r")
# Output File
outfile = open("PATH TO OUTPUT FILE (MUST END IN .OBJ)", "w")
# Material File
mtlFile = open("SAME AS OUTFILE BUT NEEDS TO END IN .MTL", "w")
matFileName = os.path.basename(mtlFile)


# Write the MTL Header
outfile.write(f"mtllib {matFileName}\n")
# Begin going through the JKL file
for line in infile:
    # Loop through the World Materials function
    if line.startswith("World materials"):
        worldmaterials(line, infile, TextureList, mtlFile, TextureBank)
        # Build the Texture Bank
        TextureBankCalc(TextureBank)
        pass

    # Loop through the World Vertices function
    elif line.startswith("World vertices"):
        worldvertices(line, infile, WorldVerticies)
        pass
    # Loop through the World texture vertices function
    elif line.startswith("World texture vertices"):
        worldtextureverts(line, infile, TextureVertList)
        pass
    # Loop through the World surfaces function
    elif line.startswith("World surfaces"):
        worldsurfaces(line, infile, ShouldNewLine, TextureList, WorldSurfaces, TextureVertList, TextureBank, TextureVertListUpdated)
        pass
# Close the files when we're done

for i in WorldVerticies:
    outfile.write(i)

# Loop through the TextureVertListUPDATED and output it to the outfile.
for key in TextureVertListUpdated:
    outfile.write("vt " + str(TextureVertListUpdated[key][0]) + " " + str(TextureVertListUpdated[key][1]) + "\n")

# Write the World Surfaces to the outfile
for i in WorldSurfaces:
    outfile.write(i)

# Debug junk
# print(TextureVertListUpdated)
# print(TextureBank)
# print(TextureVertListUpdated[1][0])
#print(TextureVertList)

# Close the files
outfile.close()
mtlFile.close()