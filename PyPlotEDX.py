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
XPERStr = "XPERCHAN"
XPERCHAN = []
TitleStr = "TITLE"
TitleTxt = []

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
       if XPERStr in line:
           xper = line.split(":")
           XPERCHAN.append(float(xper[1]))
       if TitleStr in line:
           Ttline = line.split(":")
           TitleTxt.append(str(Ttline[1]))
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

#print (EDXVar)
#print(XPERCHAN[0])
#print(TitleTxt)
TT = TitleTxt[0]
TT = TT.strip()
#print(TT)

#
#
###############################################




print("Plotting data")
# Define plot size
fig = plt.figure()
fig.set_size_inches(5, 2.5)

#plt = plt.gcf()
#plt.plot(xdata, ydata, ".", label="Data")
#plt.plot(xdata, ydata, color='red')
#plt.plot(xdata, ydata)

#line plot
plt.plot(xdata, ydata, label="Data")

#filled under
plt.fill_between(xdata, ydata, 0)

axis = plt.gca()
axis.set_ylabel('counts')
axis.set_xlim(0,20) #range to plot in keV
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
        
#could round xlab to the nearest XPERCHAN, but just find the min instead
#NOT the quickest way to do this in program terms, but quick to write    
    xlabR = min(xdata, key=lambda x:abs(x-xlab))
    ylab = ydata[xdata.index(xlabR)]

#set minimum value or don't plot
    labmin = 1000
    if (ylab>=labmin):
        axis.text(xlab, ylab+offset, oxlabTxt[lv])
    lv = lv +1


#plt.title('Plot Demo - EDX data parsed from msa file')
plt.title(TT)

# Show the graph
plt.legend()
plt.show()
