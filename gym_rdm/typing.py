"""
Type definitions.
"""

from typing import TypeAlias, Any
import numpy as np
from numpy.typing import NDArray


# Observation: a NumPy array containing pisel values as 8-bits RGB triplets
GymObs: TypeAlias = NDArray[np.uint8]

# Info: a Plain Python dictionary
GymInfo: TypeAlias = dict[str, Any]

# Action: integer values corresponding to possible actions
GymAction: TypeAlias = np.int64

# Rendered frame: a NumPy array containing pisel values as 8-bits RGB triplets
GymFrame: TypeAlias = NDArray[np.uint8]
