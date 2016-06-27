#Dependencies Numpy and Matplotlib are necessairy to execute!
import numpy as np
import matplotlib.pyplot as plt
from array import array

#PYROOT
import ROOT as rt
from ROOT import * 
from os import path

XSECTION = np.genfromtxt('../GF_NLO_13TeV_LR_3TeV_kl_35.txt', skip_header=1 , skip_footer=0, dtype='str')

BRANCHING = np.genfromtxt('../Decay_short_kl_35_arxiv1110.6452.txt', skip_header=1 , skip_footer=0, dtype='str')

counter = -1

# BR at 125 from YR4 https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR

hbb = 5.824E-01
hgg = 2.270E-03
hww = 2.137E-01
htt = 6.272E-02

# LR is lambda Radion

LR = 1 

# brSF you want to apply to the Graviton cross section
# and the file name

#brSF = 2*hbb*hgg*3/LR*3/LR
#outfilename = "BulkRadion_yr4_NLO_LR_1TeV_hh2b2g.dat"

brSF = hbb*hbb*3/LR*3/LR
outfilename = "BulkRadion_yr4_NLO_LR_1TeV_hh4b.dat"

pbtofb = 1000

# Min and Max mass to add to your file

#minMass = 800
#maxMass = 3000

minMass = 260
maxMass = 800

# ============================================= 


mass = []
xsec = []
bf = []

result = []

for entry in XSECTION :
    
    counter = counter + 1
    entryb = BRANCHING[counter]

    mass.append(int(entry[0]))
    xsec.append(float(entry[1]))
    bf.append(float(entryb[7]))

    
    result.append(float(xsec[counter])*pbtofb*float(bf[counter])*brSF)

    print mass[counter], " ", xsec[counter], " ", bf[counter]
    print "Xsec = ", result[counter]



recounter = 0
extmass = []
extresult = []

for imass in mass:

    extmass.append(imass)
    extresult.append(result[recounter])

    print imass, " ", result[recounter]


    if recounter == counter:
        continue

    slope = (log(result[recounter+1]) - log(result[recounter])) / (mass[recounter+1] - imass)
    shiftmass = imass + 100
    n = 1
    while shiftmass < mass[recounter+1]:
        result_interp = exp( log(result[recounter]) + slope * n*100 )
        
        print "  ", shiftmass, " ", result_interp
        extmass.append(shiftmass)
        extresult.append(result_interp)
        shiftmass = shiftmass + 100
        n = n+1

    recounter = recounter +1
    
with open(outfilename, "write") as outfile:
    counter = -1
    for imass in extmass:
        counter = counter + 1
        line = str(imass) + "\t" + "%.2e" % extresult[counter] + "\n"
        if imass >= minMass and imass <= maxMass:
            outfile.write(line)
    
        
        
