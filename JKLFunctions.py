import os
from PIL import Image

texDir = os.fsencode(str("PATH TO TEXTURES"))

def worldmaterials(line, infile, TextureList, mtlFile, TextureBank):
    # If the line doesn't start with 0:, skip the line
    while not line.startswith('0:'):
        line = infile.__next__()
    else:
        pass
     # If the line starts with "End" then skip
    while not line.startswith("end"):
        if line.startswith("end"):
            pass
        else:
            # Loop through the lines and add it to the texture list. This saves the name of all the materials.
            TextureList.append(line.split(":")[-1].rstrip().split()[0].split(".", 1)[0])
            # Save this data to the Texture Bank. [0,0] is the default values. We will fill these in later.
            TextureBank.update({str(line.split(":")[-1].rstrip().split()[0].split(".", 1)[0]): [0, 0]})

            # Write material info to the mtl file.
            mtlFile.write("newmtl " + line.split(":")[-1].rstrip().split()[0].split(".", 1)[0] +"\n"+"\td 1.000000\n"+"\tmap_Kd map/" + line.split(":")[-1].rstrip().split()[0].split(".", 1)[0] + ".bmp\n\n")
            # Skip to the next line in the file
            line = infile.__next__()
    else:
        pass


def worldvertices(line, infile, WorldVerticies):
    # Extract the vert number from the header
    numberverts = int(line.split()[2])
    # Skip to next line. Might have to do a check in the future (like the one in World Materials)
    line = infile.__next__()
    for i in range(0, numberverts):
        line = infile.__next__()
        # Writing the number verts to the output file.
        # outfile.write("v" + line.split(":")[-1].rstrip() + "\n")
        # Format the text
        FormatText = (line.split(":")[-1].rstrip() + "\n").split()
        # Write the [0][1][2] values (xyz) to the WorldVerticies list (Might have to reverse values here as map is
        # flipped incorrectly. If I replace 0 and 1, the map is flipped right but is inverted.
        WorldVerticies.append("v " + FormatText[0] + " " + FormatText[1] + " " + FormatText[2] + "\n")


def worldtextureverts(line, infile, TextureVertList):
    # Extract the vert number from the header
    numberVerts = int(line.split()[3])
    line = infile.__next__()
    Counter = 0
    for i in range(0, numberVerts):
        line = infile.__next__()
        # Get the float value from text
        floatNum = line.split(":")[-1].rstrip()
        # Clear off other stuff (Can probably be moved into floatnum by adding split to the end)
        floatVal = floatNum.split()

        # Get the first float from floatVal
        floatValMath = float(floatVal[0])
        # Get the second float from floatVal
        floatValMath2 = float(floatVal[1])
        # Output the float vals to the output file. The image sizes are stored in the texture bank and will be reffed
        # later in World Surfaces.
        TextureVertList.update( {Counter : [floatValMath, 1, floatValMath2, 1]} )
        # Increment counter
        Counter += 1

def worldsurfaces(line, infile, shouldnewline, texturelist, WorldSurfaces, TextureVertList, TextureBank, TextureVertListUpdated):
    # Extract the vert number from the header
    numberVerts = int(line.split()[2])
    # This is the vert that we use to create brand new texture vertices
    vertInc = 0

    line = infile.__next__()
    for i in range(0, numberVerts):
        line = infile.__next__()
        # Get the Nverts value
        NvertsTxt = line.split()[9].rstrip()
        # Clean Nverts value. Can be consolidated with Nverts
        Nverts = int(NvertsTxt.split()[0])
        # Get geo value
        GeoInt = int(line.split()[4])
        # Get the texture index
        TextureIndex = int(line.split()[1])

        # If GeoInt doesn't equal 0 then continue
        if GeoInt != 0:
            # Write the texture name on the line
            WorldSurfaces.append("usemtl " + texturelist[TextureIndex] + "\nf")
            pass

        # If Geo is 0 then don't build faces for it.
        else:
            pass

        for i in range(Nverts):
            # Only do this if Geo is not 0. 0 indicates a hidden face. Might have to clean later?
            if GeoInt != 0:
                # Text is the value for the face vert
                text = line.split()[10 + i].rstrip()
                textFixed = int(text.split(",")[0])

                # vertFixed is the value for the texture vert.
                vertFixed = int(text.split(",")[1])
                # Output the face text to the WorldSurfaces list. We increment by 1 because OBJ doesn't support 0
                WorldSurfaces.append(" " + str(textFixed + 1) + "/" + str(vertInc + 1))
                # Add value to the updated Vert list. Since we're building new values.
                TextureVertListUpdated.update({vertInc: [1,1]})

                # Get the name of the texture
                TextureName = texturelist[TextureIndex]

                # Get the current value of the updated list. The first value is the original value from the vert list
                # and we divide that by the value in Texture bank (image size). [0] is X and [1] is Y
                TextureVertListUpdated[vertInc][0] = (TextureVertList[vertFixed][0] / TextureBank[TextureName][0])
                TextureVertListUpdated[vertInc][1] = (TextureVertList[vertFixed][2] / TextureBank[TextureName][1])

                # Increment vertInc
                vertInc += 1
                # Set shouldNewLine to True since we have more data to loop through
                shouldnewline = True
            else:
                # If we hit this else, that means the loop is done and we should NOT newline.
                shouldnewline = False
                pass
        # If we should newLine then append a new line to the WorldSurfaces list
        if shouldnewline:
            WorldSurfaces.append("\n")
        else:
            pass


def TextureBankCalc(TextureBank):
    # We already generated the Texture Bank in the WorldMaterials function, but the values are 0,0. We are going to
    # look through each file and look for it in the textures folder. It'll find a match and get the image size
    # for us so we can put that into the texture bank for texture calculations later.
    for key in TextureBank:
        for file in os.listdir(texDir):
            filename = os.fsdecode(file)
            # Find filename match with Texture Bank. Lowercase it just in case.
            if filename.startswith(str(key).lower()):
                # Open the image
                im = Image.open(texDir + filename)

                # Set the texture bank 0 and 1 keys to the image X and Y values
                TextureBank[key][0] = im.size[0]
                TextureBank[key][1] = im.size[1]
                # Close the image when done
                im.close()
            else:
                pass