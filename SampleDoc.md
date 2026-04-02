Documentation of the Samples and the Detector
=============================================

##  Some notes:

- G4 defines from the center to the edge, i.e. half of the length in each edge. gdml uses the full length
- the unit of the hepevt reader of edep-sim: GeV, cm, ns

## MC sample generation: 2025.6.19 (outdated, see below)

- NueAr CC signal: 1e5 events
    - 10000 events/file, 10 files
- NueAr CC dirt: 4e5 events
    - 10000 events/file, 40 files
- Cosmic muons: 2e7 events, 
    - sampling a 6x6 $m^2$ area at z = +7m, 
    - event duration of 284µs (-30000.0, 215821.0422812193)ns, 
    - ending up with 1 cosmic muon per event
    - 100000 events/file, 200 files
- Beam related neutrons (BRN): 5e5 events, 
    - sampling among x = (-50, 50)cm, y = -54cm, z = (-60, 60)cm, 
    - t = 0ns
    - 10000 events/file, 50 files

## Scale the event rate: Want to revisit

## Coordinate system: 2025.7.3

- right hand coordinate system
- z: vertical upwards
- y: ~~neutrino direction~~ (updated in Fall 2025) neutrino direction is (x, y, z) = (0.0, 1.0, -0.337)
- x: drift direction (+x or -x in either side of the cathode), horizontal.
- origin (0, 0, 0) at the center of the LArTPC active volume

## Detector geometry: 2025.7.3

- TPC active volume: 60x50x60cm$^3$
- Signal volume for $\nu_e$-Ar CC signals: 50x40x50cm$^3$
- LAr: a cylinder with the radius of 46cm and the height of 120cm
- Pixel tiles 50x60cm$^2$ at the y-z plane, at x = 30cm and x = -30cm
- Cathode at the middle, x = 0cm, y-z plane
- GEANT4 geometry file at MCProd/g4/gdml/COHAr250.gdml

## GEANT4 simulation: 2025.7.9

- Use `edep-sim` GEANT4 wrapper.  Use `cv1.0` (outdated) at my fork of Clark's `edep-sim`:
  [https://github.com/yuntsebaryon/edep-sim](https://github.com/yuntsebaryon/edep-sim)
    - `c` stands for `COHERENT`.

## The latest samples: 2026.3.XX

### Configurations

- `edep-sim` cv2.0 (in my laptop it is in `~/source/edep-sim-origin`)
- Configuration files in `SNeNDSens` v2.0
- `Ecomug` to generate cosmic muons: [forked github](https://github.com/yuntsebaryon/EcoMug) v2.0
- The main change is the geometry: `SNeNDSens` v2.0, `MCProd/g4/gdml/COHAr250.gdml`
    - Pb tube of HOG
    - Stainless steel cryostat
    - Reconfigure the CRT panels
    - Shift the floor, ceiling, and the walls, while keeping the origin (0, 0, 0) as the center
    of the LArTPC.
- SNS neutrino and BRN direction has been updated in the previous run (fall 2025), although not logged here.

### Samples

- NueAr CC signal: 1e5 events
    - 10000 events/file, 10 files
- NueAr CC outside: 4e5 events
    - 10000 events/file, 40 files
- Cosmic muons: 1.2e8 events, 
    - sampling a 10x10 $m^2$ area at z = +6.81m, 
    - event duration of 232µs (-30000.0, 202000)ns, 
    - ending up with 1 cosmic muon per event
    - 100000 events/file, 1200 files
- Beam related neutrons (BRN): 8e5 events, `MCProd/gen/BRN/genBRN.ipynb`
    - sampling among x = -59cm, y = (-59, 59)cm, z = (-82, 82)cm, 
    - t follows the prompt neutrino time distribution
    - 10000 events/file, 80 files

-----------------------------------------------------------------------------------------------

## Previous analysis

- Analysis done in early 2024: only at the GEANT4 level, visually determined
  the selection criteria, and confirmed the signal amount is comparable with 
  the background
- No significance calculated
- Code at [Github](https://github.com/yuntsebaryon/SimpleCosmics)
    - The selection criteria at [G4Analysis](https://github.com/yuntsebaryon/SimpleCosmics/tree/main/G4Analysis)
- Event selection [spreadsheet](https://docs.google.com/spreadsheets/d/1xM5-7c4KjCEbuB2rtwNQnvj_wIaUg7_NrJqVkks3xrg/edit?usp=sharing)
