"""
Script to generate nice scalebars on images with LaTeX and TikZ.
Ported from https://github.com/habi/latex/blob/master/scalebar.m to Python

The script needs an image and a pixel size as input, then either uses the full
width of the image or a user-defined length (also as input) and calculates all
the necessary values to generate a LaTeX-file as output.
Said LaTeX-file is then compiled with "latexmk" so that - after running the
script - you get an image_scalebar.tex for further editing and and
image_scalebar.pdf for use in a talk or so.
"""

from optparse import OptionParser
from pylab import *
import os
import subprocess

# Use Pythons Optionparser to define and read the options, and also
# give some help to the user
parser = OptionParser()
usage = "usage: %prog [options] arg"
parser.add_option("-i", "--image", dest="Image",
                  help="Location of the file you want to draw a scalebar on",
                  metavar="path")
parser.add_option("-p", "--pixelsize", dest="Pixelsize",
                  type="float",
                  help="Pixel/voxel size of the image (in micrometers)",
                  metavar="1.48")
parser.add_option("-l", "--length", dest="Scalebarlength",
                  type="int",
                  help="Length of the scale bar you will draw. Generally you "
                  "know that two features are x pixels afar from each other, "
                  "then you can use this length, e.g. the tips of your sample "
                  " are 646 pixels apart...",
                  metavar="648")
parser.add_option("-f", "--fullscale", dest="fullscale",
                  default=1,
                  action="store_true",
                  help="Use the full image for scaling, do not define a scale "
                  " bar manually. Makes the '-l' entry obsolete")
(options, args) = parser.parse_args()

# Show help if no parameters are given
if options.Image is None:
    parser.print_help()
    print "Example:"
    print "The command below makes a 500 um long scalebar on a 2D image",\
        "'rec.png', which is 1024 x 1014 pixels big (with 2.8 um pixel ",\
        "size):"
    print ""
    print sys.argv[0], "-i /sls/X02DA/data/e13960/test.jpg -p 2.8 -f"
    print ""
    print "The command below makes a 500 um long scalebar on a test-image",\
        "'3d.jpg' from which you know that two features are 2170 px apart ",\
        "(650 nm px size). The script asks you to click the two points."
    print ""
    print sys.argv[0], "-i /sls/X02DA/data/e13960/test.jpg -p 0.65 -l 2170"
    print ""
    sys.exit(1)

# Warn user if options are missing or something else is wrong
if not os.path.exists(options.Image):
    print "I cannot find", options.Image, ", please try again."
    sys.exit(1)

if options.Pixelsize is None:
    print "You need to enter a pixel size! Please enter your command as this"
    print " ".join(sys.argv), "-p some_micrometers"
    sys.exit(1)

if options.Scalebarlength:
    # Set fullscale to Flase if user wants to define a length himself
    options.fullscale = False

# Hey ho, let's go
print 80 * "-"

# Display image to user
Image = plt.imread(options.Image)
plt.imshow(Image)
plt.axis([0, Image.shape[1], 0, Image.shape[0]])

# Either let user choose a set length or use the full scale of the image
if options.fullscale:
    print "Using full size of image (" +\
        str(Image.shape[1]), "x",\
        str(Image.shape[0]), "px @" + \
        str(options.Pixelsize), "um) to calculate scalebar"
    StartPoint = [(0, Image.shape[0] / 2)]
    EndPoint = [(Image.shape[1], Image.shape[0] / 2)]
else:
    print
    print "Please click on two points", options.Scalebarlength, "px (@",\
        options.Pixelsize, "um) apart, i.e. the length you chose will",\
        "be", str(options.Scalebarlength * options.Pixelsize / 1000), "mm"
    print
    plt.title(options.Image + "\nClick on start point of " +
              str(options.Scalebarlength) + " px long (" +
              str(options.Scalebarlength * options.Pixelsize / 1000) +
              " mm) line")
    StartPoint = ginput(1)
    plt.plot(StartPoint[0][0], StartPoint[0][1], marker="o", color="g")
    plt.axis([0, Image.shape[1], 0, Image.shape[0]])
    plt.draw()
    plt.title(options.Image + "\nClick on end point of " +
              str(options.Scalebarlength) + " px long (" +
              str(options.Scalebarlength * options.Pixelsize / 1000) +
              " mm) line")
    plt.draw()
    EndPoint = ginput(1)

# Plot the length we"re using to calculate
StartPoint = StartPoint[0]
EndPoint = EndPoint[0]
line = [StartPoint, EndPoint]
plt.plot(StartPoint[0], StartPoint[1], marker="o", color="g")
plt.plot(EndPoint[0], EndPoint[1], marker="o", color="r")
plt.plot([StartPoint[0], EndPoint[0]], [StartPoint[1], EndPoint[1]])
plt.axis([0, Image.shape[1], 0, Image.shape[0]])

# Calculate the stuff we need to draw a nice scalebar and update figure
if options.fullscale:
    options.Scalebarlength = Image.shape[1]
plt.title(options.Image + "\nThis line is " + str(options.Scalebarlength) +
          " px long (" +
          str(options.Scalebarlength * options.Pixelsize / 1000) + " mm)")
plt.draw()

ItemLength = 100  # px
SetScaleBarTo = 500  # um

Scale = options.Scalebarlength * options.Pixelsize / 1000
ChosenLength = np.hypot(StartPoint[0] - EndPoint[0],
                        StartPoint[1] - EndPoint[1])
UnitLength = Scale / ChosenLength * ItemLength * 1000
ScaleBarLength = ItemLength / UnitLength * SetScaleBarTo

# Inform the user
print "The chosen length of", int(round(ChosenLength)), "px corresponds to",\
    Scale, "mm."
print ItemLength, "px are thus", int(round(UnitLength)), "um"
print int(round(ScaleBarLength)), "px are thus", SetScaleBarTo, "um and"
print int(round(ScaleBarLength / (SetScaleBarTo / 100))), "px are thus 100 um"

# Write LaTeX-file
print 80 * "-"
OutputFile = os.path.join(os.getcwd(),
                          os.path.splitext(os.path.basename(options.Image))
                          [0] + "_scalebar.tex")
print "writing LaTeX-code to", OutputFile
outputfile = open(OutputFile, "w")
outputfile.write("\documentclass{article}\n")
outputfile.write("\usepackage{graphicx}\n")
outputfile.write("\usepackage{tikz}\n")
outputfile.write("\usepackage{siunitx}\n")
outputfile.write("\usepackage[graphics,tightpage,active]{preview}\n")
outputfile.write("    \PreviewEnvironment{tikzpicture}\n")
outputfile.write("\\newcommand{\imsize}{\linewidth}\n")
outputfile.write("\\newlength\imagewidth % needed for scalebars\n")
outputfile.write("\\newlength\imagescale % ditto\n")
outputfile.write("\\begin{document}%\n")
outputfile.write("%-------------\n")
outputfile.write("\pgfmathsetlength{\imagewidth}{\imsize}%\n")
outputfile.write("\pgfmathsetlength{\imagescale}{\imagewidth/" +
                 str(Image.shape[1]) + "}%\n")
outputfile.write("\def\\x{" + str(int(round(Image.shape[1] * 0.618))) +
                 "}% scalebar-x starting at golden ratio of image width of " +
                 str(Image.shape[1]) + "px = " +
                 str(int(round(Image.shape[1] * 0.618))) + "\n")
outputfile.write("\def\y{" + str(int(round(Image.shape[0] * 0.9))) +
                 "}% scalebar-y at 90% of image height of " +
                 str(Image.shape[0]) + "px = " +
                 str(int(round(Image.shape[0] * 0.9))) + "\n")
outputfile.write("\def\shadow{4}% shadow parameter for scalebar\n")
outputfile.write("\\begin{tikzpicture}[x=\imagescale,y=-\imagescale]\n")
outputfile.write("    \clip (0,0) rectangle (" + str(Image.shape[1]) + "," +
                 str(Image.shape[0]) + ");\n")
outputfile.write("    %\\node[anchor=north west, inner sep=0pt, outer " +
                 "sep=0pt] at (0,0) {\includegraphics[width=\imagewidth]{" +
                 str(os.path.abspath(options.Image)) + "}};\n")
outputfile.write("    \\node[anchor=north west, inner sep=0pt, outer " +
                 "sep=0pt] at (0,0) {\includegraphics[width=\imagewidth]{" +
                 str(os.path.splitext(options.Image)[0]) + "}};\n")
outputfile.write("    % " + str(int(round(ChosenLength))) + "px = " +
                 str(Scale) + "mm > " + str(ItemLength) + "px = " +
                 str(int(round(UnitLength))) + "um > " +
                 str(int(round(ScaleBarLength))) + "px = " +
                 str(SetScaleBarTo) + "um, " +
                 str(int(round(ScaleBarLength / (SetScaleBarTo / 100)))) +
                 "px = 100um\n")
outputfile.write("    %\draw[|-|,blue,thick] (" +
                 str(int(round(StartPoint[0]))) + "," +
                 str(int(round(StartPoint[1]))) + ") -- (" +
                 str(int(round(EndPoint[0]))) + "," +
                 str(int(round(EndPoint[1]))) + ") node [sloped,midway," +
                 "above,fill=white,semitransparent,text opacity=1] {\SI{" +
                 str(Scale) + "}{\milli\meter} (" +
                 str(int(round(ChosenLength))) + "px) TEMPORARY!};\n")
outputfile.write("    \draw[|-|,thick] (\\x+\shadow,\y+\shadow) -- (\\x+" +
                 str(int(round(ScaleBarLength))) + "+\shadow,\y+\shadow) " +
                 "node [midway, above] {\SI{" + str(SetScaleBarTo) +
                 "}{\micro\meter}};\n")
outputfile.write("    \draw[|-|,white,thick] (\\x,\y) -- (\\x+" +
                 str(int(round(ScaleBarLength))) + ",\y) node [midway,above]" +
                 " {\SI{" + str(SetScaleBarTo) + "}{\micro\meter}};\n")
outputfile.write("    %\draw[color=red, anchor=south west] (0," +
                 str(int(round(Image.shape[0]))) + ") node [fill=white, " +
                 "semitransparent] {Legend} node {Legend};\n")
outputfile.write("\end{tikzpicture}%\n")
outputfile.write("%-------------\n")
outputfile.write("\end{document}%\n")
outputfile.close()

# Compile LaTeX-file and cleanup afterwards
nirvana = open("NUL", "w")
print "compiling", OutputFile
# compile even with errors
subprocess.call("latexmk -pdf -silent " + OutputFile, stdout=nirvana,
                stderr=nirvana, shell=True)
# cleanup after compilation
print "cleaning up"
subprocess.call("latexmk -c " + OutputFile, stdout=nirvana, stderr=nirvana,
                shell=True)
nirvana.close()

# Inform the user what has been going on and make sure we show image
print 80 * "-"
print "You now have two files (" + OutputFile + " and .../" +\
    os.path.basename(OutputFile)[:-3] + "pdf)."
print "The .tex-file is for further editing and the .pdf file can be used as "\
    "is in a PowerPoint or Keynote slide..."
plt.show()

exit()
