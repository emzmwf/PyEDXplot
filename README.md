# PyEDXplot
Python script to replot EMSA format EDX file
imports matplotlib.pyplot and tkinter
Loads files in the format of EMSA/MAS Spectral Data File only 
tkinter used to select file to plot
Parameters such as plot size, keV range, y limits, etc adjustable in the code itself

# EDXSeries_joydivPlot
Takes either spectra data from csv file or a series of spectra in a folder
Extracts data as with PyEDXplot script
Produces a plot of the spectra in a ridgeline plot

# PyPlot_Checklist_EDX
Replots EMSA format EDS file
Parses identified elements in the EMSA file
Displays checklist to select which peaks are to be labelled
Dialog to select maximum x range (value) and y range (value or "max")
Produces a plot of the spectra 
