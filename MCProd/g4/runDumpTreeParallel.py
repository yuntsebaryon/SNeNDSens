#!/usr/bin/env python
import dumpTree

from concurrent.futures import ProcessPoolExecutor

def runDumpTree(iBatch):

    ## Sample config
    sampleDir = '/Users/yuntse/data/coherent/SNeNDSens'
    label = 'Cosmics'
    prefix = 'CosmicFlux'
    nFiles = 200

    for iFile in range( nFiles ):
        jFile = (iBatch+1)*nFiles + iFile
        rootFile = f'{sampleDir}/g4/{label}/{(iBatch+1)*nFiles:04d}/{prefix}_g4_{jFile:04d}.root'
        h5File = f'{sampleDir}/g4/{label}/{(iBatch+1)*nFiles:04d}/{prefix}_g4_{jFile:04d}.h5'

        print(f'Dumping {rootFile}...')
        dumpTree.dump(rootFile, h5File, True)

    return
# def runDumpTree()

if __name__ == "__main__":

    nBatches = [ 0, 1, 2, 3, 4 ]

    # Run in parallel
    with ProcessPoolExecutor() as executor:
        list(executor.map(runDumpTree, nBatches))