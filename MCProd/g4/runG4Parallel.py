#!/usr/bin/env python3
import os
import subprocess

from concurrent.futures import ProcessPoolExecutor

def runEdepSim(iBatch):

    ## Sample config
    sampleDir = '/Users/yuntse/data/coherent/SNeNDSens'
    label = 'Cosmics'
    prefix = 'CosmicFlux'
    nFiles = 200
    nEventsPerFile = 100000

    ## General location
    gdml = '/Users/yuntse/work/coherent/SNeNDSens/MCProd/g4/gdml/COHAr250.gdml'
    
    # executable = '/Users/yuntse/opt/edep-sim/edep-gcc-17.0.0-arm64-apple-darwin24.5.0/bin/edep-sim'
    executable = '/Users/yuntse/opt/edep-sim-origin/edep-gcc-17.0.0-arm64-apple-darwin24.5.0/bin/edep-sim'

    inDir = f'{sampleDir}/gen/{label}/{(iBatch+1)*nFiles:04d}'
    if not os.path.isdir( inDir ):
        raise FileNotFoundError(f"Input directory '{inDir}' does not exist")

    outDir = f'{sampleDir}/g4/{label}/{(iBatch+1)*nFiles:04d}'
    if os.path.exists( outDir ):
        raise FileExistsError(f"Output directory '{outDir}' already exists.")
    else:
        os.makedirs( f'{outDir}/mac')

    for iFile in range( nFiles ):
        jFile = (iBatch+1)*nFiles + iFile
        macfile = f'{outDir}/mac/{prefix}_g4_{jFile:04d}.mac'
        infile = f'{inDir}/{prefix}_{jFile:04d}.hepevt'
        outfile = f'{outDir}/{prefix}_g4_{jFile:04d}.root'

        with open( macfile, 'w') as f:
            f.write(
f'''
/edep/phys/ionizationModel 0
/edep/gdml/read {gdml}

/edep/db/set/neutronThreshold 0 MeV
/edep/db/set/lengthThreshold 0 mm
/edep/db/set/gammaThreshold 0 MeV
/edep/db/open {outfile}
# /edep/db/set/storeROOT true

/edep/hitSagitta LArTPC 1.0 mm
/edep/hitLength LArTPC 1.0 mm

/edep/hitSeparation LArTPC -1 mm
/edep/hitSeparation CRTtop -1 mm
/edep/hitSeparation CRTbottom -1 mm
/edep/hitSeparation CRTfront -1 mm
/edep/hitSeparation CRTback -1 mm
/edep/hitSeparation CRTright -1 mm
/edep/hitSeparation CRTleft -1 mm

/edep/update

/generator/kinematics/set hepevt

/generator/kinematics/hepevt/input {infile}
/generator/kinematics/hepevt/flavor marley

## Distribute the events based on the vertex in the rooTracker file.
/generator/position/set free

## Distribute the event times based onn the time in the rooTracker file.
/generator/time/set free

## Make sure EDEPSIM updates the kinematics generator.
/generator/add

/run/beamOn {nEventsPerFile}
'''
            )
        
        # execute edep-sim
        arg = [ macfile ]
        outlog = f'Edep-sim-{iBatch}.out'
        errlog = f'Edep-sim-{iBatch}.err'
        with open( outlog, 'w') as out, open(errlog, 'w') as err:
            subprocess.run( [executable] + arg, stdout = out, stderr = err)

    return
# def runEdepSim()

if __name__ == "__main__":

    nBatches = [ 0, 1, 2, 3, 4 ]

    # Run in parallel
    with ProcessPoolExecutor() as executor:
        list(executor.map(runEdepSim, nBatches))

    
