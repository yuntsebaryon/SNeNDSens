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

May try to disable the `BUILD_CAPTAIN` with the flag below (TPC): \
`cmake -Dcxx-FLAG="BUILD_CAPTAIN=0"`

### Dump the edep-sim output to a h5 file

```shell
   source /Users/yuntse/opt/root-v6.36.00/bin/thisroot.sh
   export LD_LIBRARY_PATH="/Users/yuntse/opt/edep-sim/edep-gcc-17.0.0-arm64-apple-darwin24.5.0/lib:/Users/yuntse/opt/root-v6.36.00/lib"
   python dumpTree.py <input.root> <output.h5> True
```


## Install the packages

### Compile GEANT4 10.7.4

```shell
   cmake -DCMAKE_INSTALL_PREFIX=/Users/yuntse/opt/geant4-v10.7.4 -DGEANT4_INSTALL_DATA=ON -DGEANT4_USE_GDML=ON -DGEANT4_USE_QT=ON -DGEANT4_USE_RAYTRACER_X11=ON -DGEANT4_USE_OPENGL_X11=ON -DGEANT4_BUILD_MULTITHREADED=ON -DCMAKE_PREFIX_PATH=/Users/yuntse/opt/xerces-c -DEXPAT_INCLUDE_DIR=/Users/yuntse/opt/expat-2.6.2/include -DEXPAT_LIBRARY=/Users/yuntse/opt/expat-2.6.2/lib/libexpat.dylib -DGEANT4_USE_SYSTEM_ZLIB=ON /Users/yuntse/source/geant4-v10.7.4
   make
   make install
```

### Compile edep-sim

Use `cv2.0` at my fork of Kazu's `edep-sim`:
[https://github.com/yuntsebaryon/edep-sim](https://github.com/yuntsebaryon/edep-sim)

`c` stands for `COHERENT`.

export HDF5_ROOT=/Users/yuntse/opt/hdf5
export PATH=$HDF5_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$HDF5_ROOT/lib:$LD_LIBRARY_PATH     # For Linux
export DYLD_LIBRARY_PATH=$HDF5_ROOT/lib:$DYLD_LIBRARY_PATH # For macOS

```shell
   source /Users/yuntse/opt/root-v6.36.00/bin/thisroot.sh
   source /Users/yuntse/opt/geant4-v10.7.4/bin/geant4.sh
   cd source/edep-sim
   source setup.sh
   export CMAKE_PREFIX_PATH=/Users/yuntse/opt/edep-sim/${EDEP_TARGET}
   cd ../edep-sim-build
   cmake -DCMAKE_INSTALL_PREFIX=/Users/yuntse/opt/edep-sim/edep-gcc-17.0.0-arm64-apple-darwin24.5.0 -DXercesC_INCLUDE_DIR=/Users/yuntse/opt/xerces-c/include -DXercesC_LIBRARY_RELEASE=/Users/yuntse/opt/xerces-c/lib/libxerces-c.dylib /Users/yuntse/source/edep-sim
   make
   make doc
   make install
```

