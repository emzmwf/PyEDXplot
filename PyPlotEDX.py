import sys;
import matplotlib.pyplot as plt;
import tkinter as tk
from tkinter import filedialog
import numpy as np

### Version updated March 2026

###########################################
#User Set Variables
###########################################

xplotmax = 10 #end of plot range in keV
yplotmax = 3000 # maximum height of intensity plotted
LabelOverlapRange = 0.01# in keV, width at which to check if there's more counts from another peak
labmin = 25# minimum intensity to label a peak



def get_text_positions(x_data, y_data, txt_width, txt_height):
    # Need to sort the data, and identify any with close x gap where there isn't a y gap
    a = zip(y_data, x_data)
    text_positions = y_data.copy()
    orig_text_positions = y_data.copy()
    print(text_positions)
    txt_height = txt_height

    for index, (y, x) in enumerate(a):
        local_text_positions = [i for i in a]
        sorted_ltp = sorted(local_text_positions)
        differ = np.diff(sorted_ltp, axis=0)
        print(sorted_ltp)
        print(differ)
        #Now check differ for overlaps
        for k, (j, m) in enumerate(differ):
            if (abs(m)<txt_width) and (j < txt_height):
                print('side collision at'+str(index)+'k no'+str(k))
                #Well, now we've found it, what do we do with it?
                #get the value from sorted_ltp, and find that same value
                #in text_positions
                #Then change that value by value+txt_height
                
                #if the j value of the error is positive, move the second index up
                #otherwise move the first index up
                if m>=0:
                    kindex = k+1
                if m<0:
                    kindex = k
                errorval = sorted_ltp[kindex]
                print('label to change is ')
                print(errorval)
                #find errorval[0] in text_positions
                print(text_positions)
                cval = orig_text_positions.index(errorval[0])
                text_positions[cval] = errorval[0]+txt_height*1.5
                
    print(text_positions)
    return text_positions


def text_plotter(x_data, y_data, labels, text_positions, axis,txt_width,txt_height):
    for x,y,lab, t in zip(x_data, y_data, labels, text_positions):
        #axis.text(x - .03, 1.02*t, '%d'%int(y),rotation=0, color='blue', fontsize=13)
        axis.text(x - .13, 1.02*t, str(lab),rotation=0, color='blue', fontsize=13)
        if y != t:
            axis.arrow(x, t+20,0,y-t, color='blue',alpha=0.2, width=txt_width*0.0,
                       head_width=.02, head_length=txt_height*0.5,
                       zorder=0,length_includes_head=True)


def Main(xplotmax, yplotmax, LabelOverlapRange, labmin):



    ##############################################
    #Select a style for the plot
    #if you have a defined local style
    #
    #Example style file used:
    #font.family  : sans-serif
    #axes.titlesize : 18
    #axes.labelsize : 15
    #lines.linewidth : 3
    #lines.markersize : 10
    #xtick.labelsize : 12
    #ytick.labelsize : 12
    #xtick.major.size:    3.5     # major tick size in points
    #xtick.major.width:   0.8     # major tick width in points
    #ytick.major.size:    3.5     # major tick size in points
    #ytick.major.width:   0.8     # major tick width in points
    #figure.dpi:         100       # figure dots per inch
    #figure.facecolor: white
    #figure.edgecolor: white
    #figure.facecolor:   FDFBF9     # figure face color, off white
    #figure.edgecolor:   F3F4F5     # figure edge color, 
    #axes.prop_cycle: cycler('color', ['2ca02c','9467bd','1f77b4', 'ff7f0e',  'd62728',  '8c564b', 'e377c2', '7f7f7f', 'bcbd22', '17becf'])	#Green, purple as first choices - aid Deuteranopia?
    ###############################################
    stylefile = 'Style1.mplstyle'
    #plt.style.use(stylefile)

    ###########################################
    # #import data
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

    TT = TitleTxt[0]
    TT = TT.strip()




    ###############################################
    # Plot
    #
    ###############################################

    print("Plotting data")
    # Define plot size
    fig = plt.figure()
    fig.set_size_inches(10, 5)

    #line plot
    plt.plot(xdata, ydata, label="Data")

    #filled under
    plt.fill_between(xdata, ydata, 0)

    axis = plt.gca()
    axis.set_xlabel('keV')
    axis.set_ylabel('counts')
    axis.set_xlim(0,xplotmax) #range to plot in keV
    axis.set_ylim(0,yplotmax)

    #Hide the legend
    #axis.get_legend().remove()

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
    # keV per channel is in variable XPERCHAN[0]
    # to get number of indexes to move forward or back in array
    xrange = int(LabelOverlapRange/XPERCHAN[0])

    #Test - set up as lists, then create plot separately
    xtlab = []
    ytlab = []
    tlabtxt = []

    # len(oxlabVal)
    lv = 0
    while lv < len(oxlabVal):
        xlab = round(oxlabVal[lv],2)
        labelyes = 1
            
    #could round xlab to the nearest XPERCHAN, but just find the min instead
    #NOT the quickest way to do this in program terms, but quick to write    
        xlabR = min(xdata, key=lambda x:abs(x-xlab))
        ylab = ydata[xdata.index(xlabR)]
    # Selecting which to plot
    # checking local range and seeing which of overlapping points would be highest
    # e.g. to avoid multiple labels caused by k-edges
    # this version - not great, look for local maxima and match instead?
        ylabLocalMax = max(ydata[xdata.index(xlab)-xrange:xdata.index(xlab)+xrange])
        if ylab < ylabLocalMax*0.999:
                           labelyes = 1#deactivated this
        if lv == 0:
            labelyes = 1
    #set minimum value or don't plot
        if (ylab<labmin):
            labelyes = 0
        if (labelyes == 1):
            #axis.text(xlab, ylab+offset, oxlabTxt[lv])
            xtlab.append(xlab)
            ytlab.append(ylab+offset)
            tlabtxt.append(oxlabTxt[lv])
        lv = lv +1

    txt_height = 0.04*(plt.ylim()[1] - plt.ylim()[0])
    txt_width = 0.02*(plt.xlim()[1] - plt.xlim()[0])
    textpositions = get_text_positions(xtlab, ytlab, txt_width, txt_height)
    text_plotter(xtlab, ytlab, tlabtxt, textpositions, axis,txt_width,txt_height)

    plt.title(TT)

    # Show the graph
    plt.show()
    

Main(xplotmax, yplotmax, LabelOverlapRange, labmin)
