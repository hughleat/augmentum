# Building From Source

Requires CMake (>=3.20).

```sh
wget https://github.com/Kitware/CMake/releases/download/v3.20.5/cmake-3.20.5-linux-x86_64.sh -O cmake.sh
bash cmake.sh --prefix=$HOME/.local --exclude-subdir --skip-license
rm cmake.sh
export PATH=$HOME/.local/bin:$PATH
```

All dependencies are built together with Augmentum except for LLVM.

### LLVM

Augmentum requires LLVM binaries and was tested against LLVM version 10. To compile LLVM, 
do the following:

Download LLVM sources.
```bash
mkdir ${LLVM_DIR}
cd ${LLVM_DIR}
git clone --depth=100 --branch release/10.x https://github.com/llvm/llvm-project
```

Build LLVM with RTTI and EH from inside *LLVM_DIR*.

```bash
mkdir build install

cd build
cmake \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DLLVM_TARGETS_TO_BUILD=X86 \
    '-DLLVM_ENABLE_PROJECTS=clang;clang-tools-extra;libclc;libcxx;libcxxabi;libunwind;lld' \
    -DBUILD_SHARED_LIBS=True \
    -DCMAKE_INSTALL_PREFIX=${LLVM_DIR}/install \
    -DLLVM_ENABLE_RTTI=ON \
    -DLLVM_ENABLE_EH=ON \
    ../llvm-project/llvm

make -j`nproc` install
```

To build Augmentum, pass path of the `lib/cmake/llvm` subdirectory in ${LLVM_DIR}/install 
to `LLVM_DIR`:

```sh
$ cd ${AUGMENTUM_HOME}
$ mkdir build
$ cd build
$ cmake .. \
    -DLLVM_DIR=/path/to/llvm/lib/cmake/llvm
$ make -j`nproc`
```

You can test if the framework is build correctly and work as expected by running explicit and instrumented test cases:

```bash
$ cd ${AUGMENTUM_HOME}/build/extensions/test

$ ./explicit
...
$ ./instrumented-with-c
...
$ ./instrumented-with-none
...
$ ./uninstrumented
...
```

All those should run through without throwing assertions.

```instrumented-with-python``` is currently not supported and will fail.


### Driver

The driver is implemented in Python. All required packages can be found in ```driver/environment.yml```. You can build a conda environment using this file:

```sh
$ conda env create --file driver/environment.yml
...
$ conda activate augmentumdriver-env
# use the driver
$ conda deactivate
```
