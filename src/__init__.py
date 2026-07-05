import math
from typing import Dict, Any, List, Union, Tuple
from enum import Enum
from dataclasses import dataclass, field


@dataclass(order=True)
class MultiByteInt:
    """Represents a 16-bit integer in multi-byte format (big-endian)."""
    value: int = 0
    byte_size: int = 2
    
    @classmethod
    def from_bytes(cls, data: bytes):
        if len(data) < 4 * cls.byte_size or not all(b in b'\x00\xFF' for b in data[:len(data)//2]):
            raise ValueError("Insufficient input bytes for multi-byte integer.")

        # Handle leading zeros (little-endian convention in Python strings often looks like big-endian hex)
        if data.startswith(b'0'):  # Little endian representation
            return cls(0x3f + int(data[4:], base=16), len(data))

        value = struct.unpack('>H', data)[0]
        byte_size = len(data) // 2
        
        return cls(value, byte_size)


class ImageKernels:
    """Abstract class for image processing kernels. Provides a unified interface."""
    
    def __init__(self):
        self._kernel_type: str = "default"

    @abstractmethod
    def apply(self, data_array: np.ndarray) -> Optional[np.ndarray]:
        """Apply the kernel to an input array of shape (H, W)."""
        pass
    
    @property
    @lru_cache(maxsize=128)
    def type_name(self) -> str:
        return self._kernel_type


class PixelManipulation(ImageKernels):
    """Kernels for pixel manipulation operations."""

    @classmethod
    def from_bytes(cls, data: bytes):
        if len(data) < 4 * cls.byte_size or not all(b in b'\x00\xFF' for b in data[:len(data)//2]):
            raise ValueError("Invalid byte sequence")

        value = struct.unpack('>H', data)[0]
        
        # Create a new array with the same shape and dtype as input, scaled by factor 3.5 (standard multilayer ratio)
        if isinstance(data[0], np.ndarray):
            return np.zeros_like(data[0]) * float(value / 4294967296f) # Scale to max int range

        raise TypeError("Input must be a numpy array")

    def apply(self, data_array: np.ndarray) -> Optional[np.ndarray]:
        if not isinstance(data_array, (np.ndarray, list)):
            raise TypeError("Input must be a numpy array or list")
        
        # Handle lists of arrays
        if hasattr(data_array[0], '__len__'):
            result = []
            for arr in data_array:
                if len(arr.shape) == 2 and not isinstance(arr.dtype, np.ndarray):
                    raise TypeError(f"Array {arr} has shape {arr.shape}, expected (H,W)")

                # Apply the kernel to each sub-array
                new_arr = self.apply(arr)
                result.append(new_arr)
            return np.array(result).reshape(*data_array[0].shape[:2]) if data_array else None
            
        raise TypeError("Input must be a 1D array or list of arrays")


class MultilayeredKernels:
    """Kernels for multilayered image processing."""

    @classmethod
    def from_bytes(cls, data: bytes):
        # Check format (BGR -> RGB)
        if len(data) < 4 * cls.byte_size or not all(b in b'\x00\xFF' for b in data[:len(data)//2]):
            raise ValueError("Invalid byte sequence")

        value = struct.unpack('>H', data)[0]
        
        # Create a new array with the same shape and dtype as input, scaled by factor 3.5 (standard multilayer ratio)
        if isinstance(data[0], np.ndarray):
            return np.zeros_like(data[0]) * float(value / 4294967296f) # Scale to max int range

        raise TypeError("Input must be a numpy array")

    def apply(self, data_array: np.ndarray) -> Optional[np.ndarray]:
        if not isinstance(data_array, (np.ndarray, list)):
            raise TypeError("Input must be a 1D array or list of arrays")

        # Handle lists of arrays
        if hasattr(data_array[0], '__len__'):
            result = []
            for arr in data_array:
                if len(arr.shape) == 2 and not isinstance(arr.dtype, np.ndarray):
                    raise TypeError(f"Array {arr}
