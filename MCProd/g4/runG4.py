import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser( description = 'Process GEANT4 simulation using edep-sim.' )

    parser.add_argument('--sample', type = str, required = True, 
                        choices = ['signal', 'cosmic', 'BRN', 'dirt', 'HOG'],
                        help = 'Sample types: signal, dirt, cosmic, BRN, HOG')
    parser.add_argument('--dir', type = str, required = True, help = 'directory of input and output files')

    args = parser.parse_args()

    sample = args.sample
    sampleConfig = { 'signal': {'label': 'NueArCC', 'prefix': 'nueArCC_sns_yDir', 'nFiles': 10, 'nEventsPerFile': 10000 },
                     'cosmic': {'label': 'Cosmics', 'prefix': 'CosmicFlux', 'nFiles': 4000, 'nEventsPerFile': 5000  },
                     'BRN': { 'label': 'BRN', 'prefix': 'BRN', 'nFiles': 1, 'nEventsPerFile': 1 },
                     'dirt': { 'label': 'NueArCCdirt', 'prefix': 'nueArCC_sns_yDir', 'nFiles': 40, 'nEventsPerFile': 10000 },
                     'HOG': { 'label': 'HOG', 'prefix': 'HOG', 'nFiles': 1, 'nEventsPerFile': 1 } }
    
    gdml = '/Users/yuntse/work/coherent/SNeNDSens/MCProd/g4/gdml/COHAr250.gdml'
    
    executable = '/Users/yuntse/opt/edep-sim/edep-gcc-17.0.0-arm64-apple-darwin24.5.0/bin/edep-sim'

    inDir = f'{args.dir}/gen/{sampleConfig[sample]['label']}'
    if not os.path.isdir( inDir ):
        raise FileNotFoundError(f"Input directory '{inDir}' does not exist")

    outDir = f'{args.dir}/g4/{sampleConfig[sample]['label']}'
    if os.path.exists( outDir ):
        raise FileExistsError(f"Output directory '{outDir}' already exists.")
    else:
        os.makedirs( f'{outDir}/mac')

    for iFile in range( sampleConfig[sample]['nFiles'] ):
        macfile = f'{outDir}/mac/{sampleConfig[sample]['prefix']}_g4_{iFile:04d}.mac'
        infile = f'{inDir}/{sampleConfig[sample]['prefix']}_{iFile:04d}.hepevt'
        if sample in ['signal', 'dirt']:
            infile = f'{inDir}/{sampleConfig[sample]['prefix']}_{iFile:02d}.hepevt'
        outfile = f'{outDir}/{sampleConfig[sample]['prefix']}_g4_{iFile:04d}.root'

        with open( macfile, 'w') as f:
            f.write(
f'''
/generator/kinematics/set hepevt

/generator/kinematics/hepevt/input {infile}
/generator/kinematics/hepevt/flavor marley

## Distribute the events based on the vertex in the rooTracker file.
/generator/position/set free

## Distribute the event times based onn the time in the rooTracker file.
/generator/time/set free

## Make sure EDEPSIM updates the kinematics generator.
/generator/add
'''
            )
        
        cmd = f'{executable} -u -e {sampleConfig[sample]['nEventsPerFile']} -o {outfile} -g {gdml} {macfile}'
        print( cmd )
        os.system( cmd )
