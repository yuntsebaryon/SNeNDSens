SNeND Sensitivity
=================

## Directories

- `MCProd`: produce the MC samples
    - `gen`: scripts producing the events at the level of primary particles
    - `g4`: scripts running `edep-sim` (a GEANT4 wrapper)

## Environment setups

### Edep-sim

```shell
   source /Users/yuntse/opt/root-v6.36.00/bin/thisroot.sh
   source /Users/yuntse/opt/geant4-v10.7.4/bin/geant4.sh
   cd source/edep-sim
   source setup.sh
   export CMAKE_PREFIX_PATH=/Users/yuntse/opt/edep-sim/${EDEP_TARGET}
   cd /Users/yuntse/work/coherent/SNeNDSens/MCProd/g4
   python runG4.py --sample BRN --dir /Users/yuntse/data/coherent/SNeNDSens
```

### Dump the edep-sim output to a h5 file

```shell
   source /Users/yuntse/opt/root-v6.36.00/bin/thisroot.sh
   export LD_LIBRARY_PATH="/Users/yuntse/opt/edep-sim/edep-gcc-17.0.0-arm64-apple-darwin24.5.0/lib:/Users/yuntse/opt/root-v6.36.00/lib"
   python dumpTree.py <input.root> <output.h5> True
```
