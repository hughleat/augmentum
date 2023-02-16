# Copyright (c) 2021, Hugh Leather
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
from pathlib import Path
from subprocess import TimeoutExpired
import uuid


from augmentum.sysUtils import run_command

logger = logging.getLogger(__name__)

class LLVMOutputVerifier:
    """
    Verify output of llvm test against a given reference output file

    Expectes the last line of the reference output to be an indicator for the exit code, e.g.:
    exit 0
    """

    CMP_TIME_OUT = 60

    def __init__(self, reference_file : Path, fpcmp_bin : Path, fpcmp_flags : str, verbose : bool = False):
        if not reference_file.is_file():
            raise ValueError("Given reference file for benchmark invalid: " + str(reference_file))

        self.__fpcmp_bin = fpcmp_bin
        self.__fpcmp_flags = fpcmp_flags
        self.__verbose = verbose
        self.__reference_dir = reference_file.parent

        # parse file content
        with reference_file.open('r') as f:
            lines = f.readlines()

            if len(lines) < 1:
                raise ValueError("Expected at least one line in reference output: " + str(reference_file))
            if not lines[-1].startswith("exit"):
                raise ValueError("Expected last line in reference output to contain exit code: " + str(reference_file))

            self.__reference = "".join(lines[:-1])
            self.__exit_code = int(lines[-1].split(" ")[1])


    def verify(self, output : str, prog_exit_code : int) -> bool:
        """
        Verify given output against reference using LLVM fpcmp comparison tool.
        """

        tmp_output_file = self.__reference_dir / f"prog_output_{uuid.uuid4()}.txt"
        with tmp_output_file.open('w') as f:
            f.write(output)

        tmp_reference_file = self.__reference_dir / f"ref_output_{uuid.uuid4()}.txt"
        with tmp_reference_file.open('w') as f:
            f.write(self.__reference)

        fpcmp_command = f"{self.__fpcmp_bin} {self.__fpcmp_flags} {tmp_reference_file} {tmp_output_file}"

        try:
            fpcmp_return, _ = run_command(fpcmp_command,
                                        timeout = LLVMOutputVerifier.CMP_TIME_OUT,
                                        verbose = self.__verbose)
        except TimeoutExpired:
            return False

        tmp_output_file.unlink(missing_ok=True)
        tmp_reference_file.unlink(missing_ok=True)

        return prog_exit_code == self.__exit_code and fpcmp_return == 0