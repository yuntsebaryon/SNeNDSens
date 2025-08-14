#!/usr/bin/env python3
### 
# This script is doing the same thing as GenCosmicFlux.ipynb, which generate the cosmic muons
# kinematics, and create .npy files storing them for the second step filling the muon 4-momentum
# in the input files of geant4.
# I'm including a multithread processing to handle more cosmic muons
###

import numpy as np
import scipy.integrate as integrate

from concurrent.futures import ProcessPoolExecutor

# Analytical cosmic ray flux from the paper
def dI_dpdcosth(costh, p):
    return 18/(p*costh+145)* (1./np.power(p+2.7/costh, 2.7))* (p+5)/(p+5/costh)
# def dI_dpdcosth()

def getNSamples(xmin, xmax, N):
    return np.random.uniform(xmin, xmax, N)
# def getNSamples()

def isAccepted(n, vPDF, maxPDF):
    return np.random.uniform(0., maxPDF, n) < vPDF
# def isAccepted()

def rejectSampling(pmin, pmax, costhmin, costhmax, nSamples):
    outSamples = np.array([ (p, costh) for p, costh in 
                           zip(getNSamples(pmin, pmax, nSamples), getNSamples(costhmin, costhmax, nSamples)) ])
    outPDF = dI_dpdcosth(outSamples[:,1], outSamples[:,0])
    maxPDF = dI_dpdcosth(costhmax, pmin)

    mask = isAccepted(len(outSamples), outPDF, maxPDF)
    reject, = np.where(~mask)

    while reject.size > 0:
        fill = np.array([ (p, costh) for p, costh in
                        zip(getNSamples(pmin, pmax, reject.size), getNSamples(costhmin, costhmax, reject.size)) ])
        
        fillPDF = dI_dpdcosth(fill[:,1], fill[:,0])
        mask = isAccepted(len(fill), fillPDF, maxPDF)
        outSamples[reject[mask]] = fill[mask]
        reject = reject[~mask]

    return outSamples
# def rejectSampling()

def writeCosmicNPY(iFile):

    outFile = f'CosmicFlux_{iFile:02d}.npy'

    nSamples = 50000000
    pmins = np.array([1., 1., 2., 2., 4., 10.])
    pmaxs = np.array([2., 2., 4., 4., 10., 10000.])
    costhmins = np.array([0., 0.5, 0., 0.5, 0., 0.])
    costhmaxs = np.array([0.5, 1., 0.5, 1., 1., 1.])

    voutSamples = np.array([ rejectSampling(pmin, pmax, costhmin, costhmax, nSamples)
                        for pmin, pmax, costhmin, costhmax in zip(pmins, pmaxs, costhmins, costhmaxs) ])
    
    with open(outFile, 'wb') as f:
        np.save(f, voutSamples)

    return
# def writeCosmicNPY()

if __name__ == "__main__":

    nFiles = [0, 1, 2, 3, 4]

    with ProcessPoolExecutor() as executor:
        list(executor.map(writeCosmicNPY, nFiles))

    
