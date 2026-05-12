from enum import Enum


class Enum__Exec_Provider_Kind(str, Enum):
    LOCAL = 'local'  # subprocess.run on the local machine
    SG_COMPUTE = 'sg_compute'  # shell-out via `sg lc exec` to a remote compute

    def __str__(self) -> str:
        return self.value
