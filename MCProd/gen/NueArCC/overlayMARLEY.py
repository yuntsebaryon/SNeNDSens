#!/usr/bin/env python
import argparse
import os
import numpy as np

# Location and dimension of the hot of gas (HOG) pipe, unit: cm
HOG_CENTER = (0, 182.5, 146)
HOG_RADIUS = 10.2

gPdg = 22
# unit: GeV
gMass = 0
gEnergy = 511e-6

def readHepevt(filename, EvtNo):
    events = []
    with open(filename, 'r') as f:
        while True:
            header = f.readline()
            if not header:
                break  # End of file
            parts = header.strip().split()
            if len(parts) < 2:
                continue
            n_particles = int(parts[1])
            event_id = EvtNo

            particles = []
            for _ in range(n_particles):
                line = f.readline()
                data = line.strip().split()
                if len(data) < 15:
                    continue
                particle = {
                    "ISTHEP": int(data[0]),
                    "IDHEP": int(data[1]),
                    "JMOHEP1": int(data[2]),
                    "JMOHEP2": int(data[3]),
                    "JDAHEP1": int(data[4]),
                    "JDAHEP2": int(data[5]),
                    "PHEP1": float(data[6]),
                    "PHEP2": float(data[7]),
                    "PHEP3": float(data[8]),
                    "PHEP4": float(data[9]),
                    "PHEP5": float(data[10]),
                    "VHEP1": float(data[11]),
                    "VHEP2": float(data[12]),
                    "VHEP3": float(data[13]),
                    "VHEP4": float(data[14]),
                }
                particles.append(particle)

            events.append((event_id, particles))
            EvtNo += 1
    return events
# def readHepevt()

def assignXYZT(events, x, y ,z, t, firstEvtNo):
    lengths = [ len(events), len(x), len(y), len(z), len(t) ]
    if len(set(lengths)) != 1:
        raise ValueError( f'Array lengths are not identical!')
        
    for event_id, particles in events:
        ievt = event_id - firstEvtNo
        for p in particles:
            p['VHEP1'] = x[ievt]
            p['VHEP2'] = y[ievt]
            p['VHEP3'] = z[ievt]
            p['VHEP4'] = t[ievt]
    return events
# def assignXYZT()

def overlayANDwriteHepevt(events, filename, HOGxlim, HOGtlow, HOGthigh, HOGthetamin, HOGthetamax, numGammaPerEvent, firstEvtNo):
    nGammasPerVertex = 1
    # only supports the events with exactly one vertex, but can have multiple HOG in the same event
    with open(filename, 'w') as f:
        for event_id, particles in events:
            vertex_id = 0
            f.write(f'{event_id} {vertex_id} {len(particles)}\n')
            for p in particles:
                f.write(f"{p['ISTHEP']} {p['IDHEP']} {p['JMOHEP1']} {p['JMOHEP2']} {p['JDAHEP1']} {p['JDAHEP2']} "
                        f"{p['PHEP1']:.6f} {p['PHEP2']:.6f} {p['PHEP3']:.6f} {p['PHEP4']:.6f} {p['PHEP5']:.6f} "
                        f"{p['VHEP1']:.6f} {p['VHEP2']:.6f} {p['VHEP3']:.6f} {p['VHEP4']}\n")
            
            # HOG generation, each gamma is associated to a vertex
            i = event_id - firstEvtNo
            HOGxyzt = assignHOGXYZT(HOGxlim, HOGthetamin, HOGthetamax, HOGtlow, HOGthigh, numGammaPerEvent[i])
            HOGpxyz = assignHOGPXYZ(gEnergy, numGammaPerEvent[i])
            for iGamma in range(numGammaPerEvent[i]):
                f.write( f'{event_id} {iGamma+1} {nGammasPerVertex}\n')

                # ISTHEP IDHEP JMOHEP1 JMOHEP2 JDAHEP1 JDAHEP2 PHEP1 PHEP2 PHEP3 PHEP4 PHEP5 VHEP1 VHEP2 VHEP3 VHEP4
                # final-state particle
                ISTHEP = 1
                IDHEP = gPdg
                
                # The JMOHEP1, JMOHEP2, JDAHEP1, and JDAHEP2 entries record the indices (between 1 and NHEP, inclusive) 
                # of particles in the event record that correspond to the first mother, second mother, first daughter, 
                # and last daughter of the current particle, respectively. 
                JMOHEP1 = 0
                JMOHEP2 = 0
                JDAHEP1 = 0
                JDAHEP2 = 0
                
                # Fill momentum
                PHEP1 = HOGpxyz[iGamma][0]
                PHEP2 = HOGpxyz[iGamma][1]
                PHEP3 = HOGpxyz[iGamma][2]
                PHEP4 = gEnergy
                PHEP5 = gMass
                VHEP1 = HOGxyzt[iGamma][0]
                VHEP2 = HOGxyzt[iGamma][1]
                VHEP3 = HOGxyzt[iGamma][2]
                VHEP4 = HOGxyzt[iGamma][3]
                f.write( f"{ISTHEP} {IDHEP} {JMOHEP1} {JMOHEP2} {JDAHEP1} {JDAHEP2} "
                         f"{PHEP1:.6f} {PHEP2:.6f} {PHEP3:.6f} {PHEP4:.6f} {PHEP5:.6f} "
                         f"{VHEP1:.6f} {VHEP2:.6f} {VHEP3:.6f} {VHEP4:.6f}\n")
            

# def overlayANDwriteHepevt()

def xyzInBox(xmin, xmax, ymin, ymax, zmin, zmax, n):
    rng = np.random.default_rng()
    x = rng.uniform(xmin, xmax, n)
    y = rng.uniform(ymin, ymax, n)
    z = rng.uniform(zmin, zmax, n)
    return x, y, z
# def xyzInBox()

def xyzDirt( r, zmin, zmax, xIn, yIn, zIn, n):
    xlist = []
    ylist = []
    zlist = []

    while len(xlist) < n:
        # Generate in batches (e.g., 2×n to improve efficiency)
        batch_size = n * 2
        x = np.random.uniform(-r, r, batch_size)
        y = np.random.uniform(-r, r, batch_size)
        z = np.random.uniform(zmin, zmax, batch_size)
        r = np.sqrt(x**2 + y**2)

        # Apply geometric cut
        mask = (r <= 46.) & ~((np.abs(x) < xIn) & (np.abs(y) < yIn) & (np.abs(z) < zIn))

        # Keep only passing events
        x_valid = x[mask]
        y_valid = y[mask]
        z_valid = z[mask]

        # Append valid values
        xlist.extend(x_valid.tolist())
        ylist.extend(y_valid.tolist())
        zlist.extend(z_valid.tolist())

    # Trim to exactly n entries
    vtxx = np.array(xlist[:n])
    vtxy = np.array(ylist[:n])
    vtxz = np.array(zlist[:n])

    return vtxx, vtxy, vtxz
# def xyzDirt

def getNSamples(xmin, xmax, N):
    return rng.uniform(xmin, xmax, N)
# def getNSamples()

def isAccepted(n, vPDF, maxPDF):
    return rng.uniform(0., maxPDF, n) < vPDF
# def isAccepted()

def rejectSampling(PDF, tmin, tmax, nSamples):
    outSamples = getNSamples(tmin, tmax, nSamples)
    outSampleBins = np.floor(outSamples/10).astype(int)
    outPDF = PDF[outSampleBins]
    maxPDF = PDF.max()

    mask = isAccepted(len(outSamples), outPDF, maxPDF)
    reject, = np.where(~mask)

    while reject.size > 0:
        fill = getNSamples(tmin, tmax, reject.size)
        fillBins = np.floor(fill/10).astype(int)
        
        fillPDF = PDF[fillBins]
        mask = isAccepted(len(fill), fillPDF, maxPDF)
        outSamples[reject[mask]] = fill[mask]
        reject = reject[~mask]

    return outSamples
# def rejectSampling()

# location and time in [cm, ns]
def assignHOGXYZT(xlim, thetamin, thetamax, tlow, thigh, nSamples):
    theta_pos = np.random.uniform(thetamin, thetamax, nSamples)
    x_pos = HOG_CENTER[0] + np.random.uniform(-xlim, xlim, nSamples)
    y_pos = HOG_CENTER[1] + HOG_RADIUS * np.cos(theta_pos)
    z_pos = HOG_CENTER[2] + HOG_RADIUS * np.sin(theta_pos)
    
    xyzt = np.column_stack((x_pos, y_pos, z_pos, np.random.uniform(tlow, thigh, nSamples)))
    return xyzt
# def assignHOGXYZT()

def assignHOGPXYZ(p_total, nSamples):

    costheta = np.random.uniform(-1., 1., nSamples)
    sintheta = np.sqrt( 1. - costheta**2 )
    phi = np.random.uniform(0., 2.*np.pi, nSamples)
    px = p_total*sintheta*np.cos(phi)
    py = p_total*sintheta*np.sin(phi)
    pz = p_total*costheta

    return np.column_stack((px, py, pz))
# def assignHOGPXYZ()

if __name__ == "__main__":

    parser = argparse.ArgumentParser( description = 'signal or dirt nue-Ar CC samples; default on signal')

    parser.add_argument('--dirt', action = 'store_false', dest = 'isSignal', help = 'specify it is the dirt background sample.')
    
    args = parser.parse_args()

    indir = '/Users/yuntse/data/coherent/SNeNDSens/gen/NueArCC/marley'
    outdir = '/Users/yuntse/data/coherent/SNeNDSens/gen/NueArCC_Overlay'

    if args.isSignal:
        print(f'Processing signal events...')
    else:
        indir = '/Users/yuntse/data/coherent/SNeNDSens/gen/NueArCCdirt/marley'
        outdir = '/Users/yuntse/data/coherent/SNeNDSens/gen/NueArCCdirt_Overlay'
        print('Processing dirt events...')

    if os.path.exists(outdir):
        # raise FileExistsError(f"Output directory '{outdir}' already exists.")
        print(f"Output directory '{outdir}' already exists.")
    else:
        os.makedirs(outdir)

    nuTime = np.load('/Users/yuntse/work/coherent/SNeNDSens/SNS/DelayedNeutrinosPer10ns.npy')


    # detector boundary
    ## signal volume
    xlim = 25
    ylim = 20
    zlim = 25
    ## dirt volume
    rOutlim = 46
    zOutlim = 60
    ## Hot of gas generation volume
    HOGxlim = 50
    HOGtlow = -30000
    HOGthigh = 188000
    HOGthetamin = 0
    HOGthetamax = 2*np.pi

    # Numbers of events, files
    firstEvtNo = 0
    nEventsPerFile = 10000
    nFiles = 10
    if not args.isSignal:
        nFiles = 40

    for iFile in range(nFiles):
        firstEvtNo = nEventsPerFile*iFile

        infile = f'{indir}/nueArCC_sns_{iFile:04d}.hepevt'
        outfile = f'{outdir}/nueArCC_sns_{iFile:04d}.hepevt'

        # Set x, y, z
        if args.isSignal:
            x, y, z = xyzInBox( -xlim, xlim, -ylim, ylim, -zlim, zlim, nEventsPerFile)
        else:
            x, y, z = xyzDirt( rOutlim, -zOutlim, zOutlim, xlim, ylim, zlim, nEventsPerFile)

        # Set t, currently all at 0
        # t = np.full(nEventsPerFile, 0)
        rng = np.random.default_rng()
        t = rejectSampling(nuTime, 0., 15000., nEventsPerFile)

        # Read in the events
        events = readHepevt(infile, firstEvtNo)
        # Assign x, y, z, t
        updatedEvents = assignXYZT(events, x, y, z, t, firstEvtNo)

        # Calculate the number of hot of gas gammas per event
        ## Average number of gammas
        avgNumGammaPerEvent = 2*(HOGthetamax - HOGthetamin)*25*152.4*HOGxlim*(HOGthigh - HOGtlow)*1.e-9
        ## Poisson distributions for the number of gammas in each event
        numGammaPerEvent = np.random.poisson( lam = avgNumGammaPerEvent, size = nEventsPerFile)

        # Overlay the hot of gas and write the events
        overlayANDwriteHepevt(updatedEvents, outfile, HOGxlim, HOGtlow, HOGthigh, HOGthetamin, HOGthetamax, numGammaPerEvent, firstEvtNo)
