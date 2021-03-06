
from myClasses import fft 
from myClasses import fftfilter
import h5py
import pylab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams.update( {'font.size':22})
#############################################
#USER CODE BELOW

#VARIABLES
ft = fft()
ft2 = fftfilter()
f = h5py.File('/dls/science/groups/das/ExampleData/OpusData/Nexus/BSA low conc T 10x10 line.0.nxs',"r") # load you nexus file here

s = f["entry1/instrument/interferometer/sample_interferogram_scan"][...] #signal on which to perform FFT

com = f["entry1/instrument/interferometer/sample_scan"][...]# this is the FT of the same file, as performed by opus

highfold = f['/entry1/instrument/interferometer/opus_parameters/instrument/high_folding_limit'][...]

zerofill = f['/entry1/instrument/interferometer/opus_parameters/ft/zero_filling_factor'][...]
zerofill =np.asarray(zerofill, int)

refer = f['/entry1/instrument/interferometer/reference_scan'][...] #reference scan
absorb = f['/entry1/instrument/interferometer/ratio_absorbance_scan'][...] #reference scan
#renergy =  f["entry1/instrument/interferometer/reference_energy"][...] # energy axis of reference scan 
#absenergy = f["entry1/instrument/interferometer/ratio_absorbance_energy"][...] # energy axis of reference scan 
ymax = f['/entry1/instrument/interferometer/opus_parameters/sample_data_interferogram/y_maximum'][...] #max amplitude of interferogram processed by Opus
yscaling = f['/entry1/instrument/interferometer/opus_parameters/sample_data_interferogram/y_scaling_factor'][...] #scaling factor that Opus applies to each intererigram before processing it.
ymaxspect = f['/entry1/instrument/interferometer/opus_parameters/sample_data/y_maximum'][...]#scaling factor that Opus applies to the final spectrum before plotting it.

axis  = f["entry1/instrument/interferometer/reference_energy"][...] #energy axis from Opus
s = s[7,:]
fw = 420 #defines the filter width. The filter is composed of a pair of symmetric, inverse Blackman Harris 3 (-67bD side lobe) filters, used to eliminate secondary fringes
#The filters are zero filled in the middle to sweep out a variable region of the spectrum. Select number of points you want to eliminate with the 'fw' parameter
fmin = 0.1 #the value of this parameter determines the minimum value of the filter, eg if fmin =0.0, some of the points will be completely eliminated. if fmin>0, points will be dampened only.
dv = 65 # dv = half of period of oscillatory fringes in absorbance spectrum/intensity spectrum, along the energy axis. 
#            NB.  Needs to be in units of cm-1!
#When you input dv, the program will use that information to position the inverse Blackman Harris filter to eliminate
#the oscillations in your spectrum. 
ymaxinterf = s.max() #compute the max height of interferogram (we ll need to pass it as a parameter)

#######################################
#COMMANDS

#Non oscillatory, single sided data

# single channel function that outputs 2 arrays, 1st array is the  single channel spectrum and the second array is the wavenumber axis [cm-1]

#schannel = ft.singleChannel(s,highfold,zerofill,ymax,ymaxinterf,yscaling,ymaxspect) #use this function if you have a single, raw interferogram
#absorb = ft.absorbance(schannel, refer, highfold,zerofill,ymax,ymaxinterf,yscaling,ymaxspect)

#Non oscillatory, DOUBLE sided data

schannel2 = ft.singleChannel2(s,highfold,zerofill,ymax,ymaxinterf,yscaling,ymaxspect) #use this function if you have a double sided interferogram 
#NB. the high folding limit must be in cm-1
#absorb2 = ft2.absorbance2(schannel2, refer, highfold,zerofill,ymax,ymaxinterf,yscaling,ymaxspect) # absorbance function for a double sided sample and reference interferogram
#########################################
#Oscillatory data

#Oscillatory, single sided data.


#schanneloscil = ft2.singleChannel(s, fw, fmin,highfold,dv,zerofill,ymax,ymaxinterf,yscaling,ymaxspect) #use this function if you have a single-sided, oscillatory, raw interferogram
#absorboscil = ft.absorbance(schanneloscil, refer, highfold,zerofill,ymax,ymaxinterf,yscaling,ymaxspect)

#Oscillatory, double sided data


#schannel2oscil = ft2.singleChannel2(s, fw, fmin,highfold,dv,zerofill,ymax,ymaxinterf,yscaling,ymaxspect) #use this function if you have a double sided, oscillatory, interferogram 
#NB. the high folding limit must be in cm-1
#absorboscil = ft2.absorbance2(schannel2oscil, refer, highfold,zerofill,ymax,ymaxinterf,yscaling,ymaxspect)



# example plotting tool below
x = schannel2 # select which spectrum to plot
#Tool for selecting which region of spectrum to display (default is 500 to 4000cm-1)
a = np.add(x[1],-axis[0])
a = np.abs(a)
a = a.argmin()
b = np.add(x[1],-axis[axis.size-1])
b = np.abs(b)
b = b.argmin()
final = x[0][a-1:b+1]
energy = x[1][a-1:b+1]


#pylab.plot(schannel2oscil[1],schannel2oscil[0])

plt.plot(energy,-np.log10(final*(refer.max()/final.max())/refer), label = 'Absorption Spectrum 2 After Fringe Elim.', linewidth = 2.0)
#plt.plot(energy[3:-3],absorb, label = 'Absorption Spectrum 2 Before Fringe Elim.', linewidth = 2.0)
#plt.plot(energy[3:-3], -np.log10(com/refer[3:-3]))
plt.xlabel("wavenumber [cm-1] ", fontsize = 21 )
plt.ylabel("Absorption Spectrum [dimensionless]", fontsize = 21)
#plt.legend(loc = 'upper right')

plt.show()