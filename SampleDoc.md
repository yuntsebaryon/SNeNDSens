Documentation of the Samples and the Detector
=============================================

## MC sample generation: 2025.6.19

- NueAr CC signal: 1e5 events
    - 10000 events/file, 10 files
- NueAr CC dirt: 4e5 events
    - 10000 events/file, 40 files
- Cosmic muons: 2e7 events, sampling a 6x6 $m^2$ area, event duration of 200µs, 
  ending up with 1 cosmic muon per event
    - 5000 events/file, 4000 files
- Beam related neutrons (BRN): 5e5 events
    - 10000 events/file, 50 files

## Scale the event rate: Want to revisit

## Coordinate system: 2025.7.3

- right hand coordinate system
- z: vertical upwards
- y: neutrino direction
- x: drift direction (+x or -x in either side of the cathode), horizontal.
- origin (0, 0, 0) at the center of the LArTPC active volume

## Detector geometry: 2025.7.3

- TPC active volume: 60x50x60cm$^3$
- Signal volume for $\nu_e$-Ar CC signals: 50x40x50cm$^3$
- LAr: a cylinder with the radius of 46cm and the height of 120cm
- Pixel tiles 50x60cm$^2$ at the y-z plane, at x = 30cm and x = -30cm
- Cathode at the middle, x = 0cm, y-z plane
- GEANT4 geometry file at MCProd/g4/gdml/COHAr250.gdml

## Previous analysis

- Analysis done in early 2024: only at the GEANT4 level, visually determined
  the selection criteria, and confirmed the signal amount is comparable with 
  the background
- No significance calculated
- Code at [Github](https://github.com/yuntsebaryon/SimpleCosmics)
    - The selection criteria at [G4Analysis](https://github.com/yuntsebaryon/SimpleCosmics/tree/main/G4Analysis)
- Event selection [spreadsheet](https://docs.google.com/spreadsheets/d/1xM5-7c4KjCEbuB2rtwNQnvj_wIaUg7_NrJqVkks3xrg/edit?usp=sharing)
