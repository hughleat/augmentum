# Copyright (c) 2021, Hugh Leather
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import augmentum
print("The script is running!")

def incr_ret(pt, ret, *args):
    ret.value += 1

augmentum.extend_after(incr_ret, name_pred = "_Z3addii")
