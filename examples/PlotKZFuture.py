### This script calculates the sensitivity of an experiment searching
### for 0nubb-decay in Ge76 

import os.path
FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = FILE_PATH + '/../data/'
import sys
sys.path.append(FILE_PATH + '/..')
import matplotlib.pyplot as plt

import csv
from numpy import arange
from pybbsens import units
from pybbsens import isotope
from pybbsens import experiment
from pybbsens import conflimits
from pybbsens import nmeset


########################################
### EXPERIMENT DATA ####################

name = "KZEN"
isot = isotope.Xe136
eff  = 0.55
eres = isot.Qbb * 0.06
bkg  = 1.0E-4 / (units.keV*units.kg*units.year)
mass = 429. *units.kg
expo = 2200. *units.kg*units.year

nmes=["ISM","IBM2"]
cnmes=["blue","red"]


########################################
### Create a confidence-limit calculator. 
### We use in this case the Feldman-Cousins memoizer.
fcm = conflimits.FCMemoizer(0.9)
fcm.ReadTableAverageUpperLimits(DATA_PATH+'FC90.dat')

exp = experiment.Experiment(name, isotope.Xe136, eff, eres, bkg, mass)

i=0
for nme in nmes:
	
	isotope.SelectNMESet(nmeset.nmedb[nme])
	MBB=[]
	MT=arange(10,10010,10.)
	MBB =[exp.sensitivity(mt * units.kg * units.year, fcm) / units.meV for mt in MT]

	color = cnmes[i]
	i+=1
	linestyle = 'solid'

	plt.plot(MT, MBB, color, linewidth=2.5, ls=linestyle)
	ax = plt.subplot(111)
	plt.axis([1e+2,1e+4,2,200])
	plt.xlabel('Exposure (kg year)')
	plt.ylabel(r'$m_{\beta\beta}$ (meV)')
	ax.set_xscale('log')
	plt.grid(True)
	plt.show()

	print "**Experiment KZEN for NME= %s asymptotic mbb -->%5.2f"%(nme,MBB[-1])
	#ax.set_yscale('log')
    


