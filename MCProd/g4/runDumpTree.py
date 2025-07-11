#!/usr/bin/env python
import argparse
import dumpTree

if __name__ == "__main__":

    parser = argparse.ArgumentParser( description = 'Process GEANT4 simulation using edep-sim.' )

    parser.add_argument('--sample', type = str, required = True,
                        choices = ['signal', 'cosmic', 'BRN', 'dirt', 'HOG'],
                        help = 'Sample types: signal, dirt, cosmic, BRN, HOG')
    parser.add_argument('--dir', type = str, required = True, help = 'directory of input and output files')

    args = parser.parse_args()

    sample = args.sample
    sampleConfig = { 'signal': {'label': 'NueArCC', 'prefix': 'nueArCC_sns_yDir', 'nFiles': 10, 'nEventsPerFile': 10000 },
                     'cosmic': {'label': 'Cosmics', 'prefix': 'CosmicFlux', 'nFiles': 200, 'nEventsPerFile': 100000  },
                     'BRN': { 'label': 'BRN', 'prefix': 'BRN', 'nFiles': 50, 'nEventsPerFile': 10000 },
                     'dirt': { 'label': 'NueArCCdirt', 'prefix': 'nueArCC_sns_yDir', 'nFiles': 40, 'nEventsPerFile': 10000 },
                     'HOG': { 'label': 'HOG', 'prefix': 'HOG', 'nFiles': 1, 'nEventsPerFile': 1 } }
    
    for iFile in range( sampleConfig[sample]['nFiles'] ):
        rootFile = f'{args.dir}/g4/{sampleConfig[sample]['label']}/{sampleConfig[sample]['prefix']}_g4_{iFile:04d}.root'
        h5File = f'{args.dir}/g4/{sampleConfig[sample]['label']}/{sampleConfig[sample]['prefix']}_g4_{iFile:04d}.h5'

        print(f'Dumping {rootFile}...')
        dumpTree.dump(rootFile, h5File, True)