import sys;
import matplotlib.pyplot as plt;
import tkinter as tk
from tkinter import filedialog

###########################################
#import data
# use tkinter to open a file

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

#gives file_path

#now open the file
print("opening EDX format file")
f = open(file_path, 'r')

# r	Open for reading plain text
# w 	Open for writing plain text
# a	Open an existing file for appending plain text
# rb	Open for reading binary data
# wb	Open for writing binary data

# f is a file defining the type of file

# If the file is small, can open all at once:
print("Parsing EDX file")
text = f.read()
# gives a text content of the file

# read one line - the first
line = f.readline()

# read in one line at a time, through whole file 
# parse and append valid info to an array or library

"""
with open(file_path) as fp:
   for cnt, line in enumerate(fp):
       print("Line {}: {}".format(cnt, line))
"""

"""
#Identify if there is a hash in a line
HashStr = "#"
with open(file_path) as fp:
   for cnt, line in enumerate(fp):
       print("Line {}: {}".format(cnt, line))
       if HashStr in line:
           print("Hash in line")
"""

# Check this looks like a spectra file
#FORMAT      : EMSA/MAS Spectral Data File

#Extract labels for use
##OXINSTLABEL: 26, 6.404, Fe
# Second number is keV

EDXVar = False
HashStr = "#"
OXStr = "OXINSTLABEL"
xdata = []
ydata = []
oxlabVal = []
oxlabTxt = []

EDX_str = "EMSA/MAS"
with open(file_path) as fp:
   for cnt, line in enumerate(fp):
       #print("Line {}: {}".format(cnt, line))
       if EDX_str in line:
           EDXVar = True
       if OXStr in line:
           oxlb = line.split(",")
           oxlabVal.append(float(oxlb[1]))
           oxlabTxt.append(oxlb[2])
       if not HashStr in line:
           #print("will append this line")
           values = line.split(",")
           xv = values[0]
           xdata.append(float(xv))
           yv = values[1]
           ydata.append(float(yv))

#End if this isn't an EDX file
if not EDXVar:
    print ("This does not appear to be an EDX format file")
    sys.exit

print (EDXVar)    

#
#
###############################################




print("Plotting data")
# Define plot size
fig = plt.figure()

#plt = plt.gcf()
#plt.plot(xdata, ydata, ".", label="Data")
#plt.plot(xdata, ydata, color='red')
#plt.plot(xdata, ydata)
plt.plot(xdata, ydata, label="Data")
axis = plt.gca()
#plt.set_size_inches(5,3)
axis.set_ylabel('counts')
axis.set_xlim(0,10)
#axis.set_ylim(0,2000)

###Annotations###

#Add an offset so the plot doesn't appear on top of the line
offset = 0.5

"""
#Test values
##OXINSTLABEL: 29, 8.048, Cu
xlab = 8.04
ylab = ydata[xdata.index(xlab)]
axis.text(xlab, ylab+offset, 'Cu')
"""

# len(oxlabVal)
lv = 0
while lv < len(oxlabVal):
    xlab = round(oxlabVal[lv],2)
    ylab = ydata[xdata.index(xlab)]
    axis.text(xlab, ylab+offset, oxlabTxt[lv])
    lv = lv +1


plt.title('Plot Demo - EDX data parsed from msa file')

# Show the graph
plt.legend()
plt.show()
