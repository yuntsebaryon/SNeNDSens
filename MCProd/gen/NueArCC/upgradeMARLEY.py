#!/usr/bin/env python
import argparse
import os
import numpy as np

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

def writeHepevt(events, filename):
    # only supports the events with exactly one vertex
    vertex_id = 0
    with open(filename, 'w') as f:
        for event_id, particles in events:
            f.write(f'{event_id} {vertex_id} {len(particles)}\n')
            for p in particles:
                f.write(f"{p['ISTHEP']} {p['IDHEP']} {p['JMOHEP1']} {p['JMOHEP2']} {p['JDAHEP1']} {p['JDAHEP2']} "
                        f"{p['PHEP1']:.6f} {p['PHEP2']:.6f} {p['PHEP3']:.6f} {p['PHEP4']:.6f} {p['PHEP5']:.6f} "
                        f"{p['VHEP1']:.6f} {p['VHEP2']:.6f} {p['VHEP3']:.6f} {p['VHEP4']}\n")
# def writeHepevt()

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

if __name__ == "__main__":

    parser = argparse.ArgumentParser( description = 'signal or dirt nue-Ar CC samples; default on signal')

    parser.add_argument('--dirt', action = 'store_false', dest = 'isSignal', help = 'specify it is the dirt background sample.')
    
    args = parser.parse_args()

    indir = '/Users/yuntse/data/coherent/SNeNDSens/NueArCC/marley'
    outdir = '/Users/yuntse/data/coherent/SNeNDSens/NueArCC/marley_xyzt'

    if args.isSignal:
        print(f'Processing signal events...')
    else:
        indir = '/Users/yuntse/data/coherent/SNeNDSens/NueArCCdirt/marley'
        outdir = '/Users/yuntse/data/coherent/SNeNDSens/NueArCCdirt/marley_xyzt'
        print('Processing dirt events...')

    if os.path.exists(outdir):
        raise FileExistsError(f"Output directory '{outdir}' already exists.")
    else:
        os.makedirs(outdir)

    # detector boundary
    ## signal volume
    xlim = 25
    ylim = 20
    zlim = 25
    ## dirt volume
    rOutlim = 46
    zOutlim = 60

    # Numbers of events, files
    firstEvtNo = 0
    nEventsPerFile = 10000
    nFiles = 10
    if not args.isSignal:
        nFiles = 40

    for iFile in range(nFiles):
        firstEvtNo = nEventsPerFile*iFile

        infile = f'{indir}/nueArCC_sns_yDir_{iFile:02d}.hepevt'
        outfile = f'{outdir}/nueArCC_sns_yDir_{iFile:02d}.hepevt'

        # Set x, y, z
        if args.isSignal:
            x, y, z = xyzInBox( -xlim, xlim, -ylim, ylim, -zlim, zlim, nEventsPerFile)
        else:
            x, y, z = xyzDirt( rOutlim, -zOutlim, zOutlim, xlim, ylim, zlim, nEventsPerFile)

        # Set t, currently all at 0
        t = np.full(nEventsPerFile, 0)

        # Read in the events
        events = readHepevt(infile, firstEvtNo)
        # Assign x, y, z, t
        updatedEvents = assignXYZT(events, x, y, z, t, firstEvtNo)
        # Write the events
        writeHepevt(updatedEvents, outfile)