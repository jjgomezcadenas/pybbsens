"""docstring for experiment"""

import isotope
import units
import constants
import conflimits

import math



class Experiment(object):
    """docstring for Experiment"""

    def __init__(self, name, isotope, eff, res, bkg, mass):
        self.name = name ### Experiment's name
        self.isotope = isotope ### bb isotope used by the experiment
        self.eff = eff ### Detection efficiency for 0nubb
        self.res = res ### Energy resolution (FWHM) at Qbb
        self.bkg = bkg ### Background rate in ROI
        self.mass = mass ### Isotope mass

    def N2nubb(self, time):
        """Return the number of 2nubb expected after a certain 
        observation time assuming perfect detection efficiency."""
        return math.log(2.) * self.mass * constants.N_A * time \
               / (self.isotope.W * self.isotope.T2nu)

    def Nbkg(self, exposure):
        """Return the number of background events expected 
        for a given exposure."""
        return (self.bkg * exposure * self.res)

    def sensitivity_halflife(self, exposure, clc):
        """Return the experimental sensitivity to the half-life of the
        0nubb process."""
        aul = clc.AverageUpperLimit(self.Nbkg(exposure))
        return math.log(2.)*constants.N_A*self.eff*exposure/(self.isotope.W*aul)

    def sensitivity_mbb(self, exposure, clc):
        half_life = self.sensitivity_halflife(exposure, clc)
        return self.isotope.mbb(half_life)


##############################

name = "NEXT100"

eff  = 0.30
res  = 0.75*2458.*units.keV 
bkg  = 5.E-4 /(units.keV*units.kg*units.year)
mass = 100.*0.91*units.kg

next100 = Experiment(name, isotope.Xe136, eff, res, bkg, mass)

##############################


##############################


if __name__ == '__main__':

    FC = conflimits.FeldmanCousins(0.9)
    print next100.sensitivity(100.*units.kg*units.year, FC) / units.meV