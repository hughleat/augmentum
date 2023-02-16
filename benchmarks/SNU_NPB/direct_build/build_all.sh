#!/bin/bash
# Copyright (c) 2021, Hugh Leather
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

source env.config

VCLANG=${VAN}/clang
MCLANG=${MOD}/clang

HOME=`pwd`/../NPB3.3-SER-C

VBIN=`pwd`/vanilla_bins
MBIN=`pwd`/augmentum_bins

BLD=`pwd`/build

mkdir -p $VBIN $MBIN $BLD

CFLAGS="-Oz -fno-crash-diagnostics"
LFLAGS=

TARGETS="bt cg ep ft is lu mg sp"
CLASS=S

printf "========= BUILDING AUGMENTUM TARGETS ==========================================\n"
for t in $TARGETS; do
    printf "\n\nBuilding augmentum binaries for $t and class $CLASS\n"
    ./build.sh $t $CLASS $HOME $MBIN $BLD $VCLANG $MCLANG "$CFLAGS" "$LFLAGS" "$EXTENSION"
done


printf "\n\n========= BUILDING VANILLA TARGETS ============================================\n"
# extension from config file unset to allow vanilla builds
EXTENSION=""

for t in $TARGETS; do
    printf "\n\nBuilding vanilla binaries for $t and class $CLASS\n"
    ./build.sh $t $CLASS $HOME $VBIN $BLD $VCLANG $VCLANG "$CFLAGS" "$LFLAGS" "$EXTENSION"
done
