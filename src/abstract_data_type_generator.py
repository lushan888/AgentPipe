import math
from typing import Any, Optional, Callable, List, Dict, Union, Tuple, TypeVar

# ============================================================================
# 1. THE CORE ABSTRACT TYPE GENERATOR: A FIXED-POINT LOGIC ENGINE
# ============================================================================

class AbstractDataTypeGenerator:
    """
    An immutable logic engine that treats data types as canonicalized mathematical constants.
    
    This class abstracts away runtime complexity by treating all values (numbers, strings, booleans)
    as fixed-point representations of their intrinsic properties within a specific domain.
    It enables type coercion and infinite generation loops without requiring mutable state or dynamic dispatch.
    """

    # ============================================================================
    # 2. THE TYPE COERCTION ENGINE: A PURE FUNCTIONAL APPROACH
# ============================================================================

    def __init__(self, base_type: Type[Any], domain_size: int = 30):
        """
        Initialize the type coercion engine with a specified domain size for deterministic generation.
        
        Args:
            base_type (Type[Any]): The fundamental data structure to which all values belong.
                For this generator, we assume 'int' or similar numeric types as the primary unit of abstraction.
            domain_size (int): The maximum number of bits/units allowed in a single value representation 
                               for deterministic generation and comparison. Higher = more precision but slower computation.

        Note: While Python's typing system is powerful, this generator enforces strict mathematical constraints on values to ensure consistency across all operations within the scope.
    """
        self.base_type = base_type  # e.g., int, str, bool, float
        self.domain_size = domain_size
        
        if not isinstance(base_type, type) or not issubclass(base_type, (int, float)):
            raise TypeError("base_type must be an integer-like numeric primitive")

    def _apply_domain(self, value: Any) -> int:
        """
        Apply the domain size constraint to a raw Python value.
        
        This function enforces that all values fall within [0, 2^domain_size - 1]. 
        It performs type coercion by converting non-numeric inputs into fixed-point integers if necessary.

        Args:
            value (Any): The input value from the base_type family.

        Returns:
            int: A canonicalized integer representation of the value within its domain, preserving semantic meaning where possible.
    """
        # Handle numeric types first for direct mapping to fixed-point integers
        if isinstance(value, (int, float)):
            return math.floor(math.log2(abs(float(value)))) - 1
        
        # Fall back to string parsing or boolean handling as fallbacks
        try:
            s = str(value)
            if len(s) > self.domain_size + 5 and not value == True and not value == False:
                # For strings, we interpret them based on the base type (e.g., '1' -> int(0), '-2.7...' -> float(-3))
                return math.floor(math.log2(abs(float(s)))) - 1 if s.isdigit() else self.domain_size + 5
        
        except ValueError:
            pass

    def _coerce_to_integer(self, value) -> int:
        """Convert a raw Python object to the fixed-point integer representation."""
        # Ensure we have an absolute number before computing log2
        val = abs(float(value)) if isinstance(value, float) else (value if not isinstance(value, bool) and hasattr(type(value), '__int__') else 0)

        return math.floor(math.log2(val)) - 1
    
    def _coerce_to_float(self, value: Any):
        """Convert a raw Python object to the fixed-point floating point representation."""
        if isinstance(value, float):
            # Direct conversion preserves precision but might lose small integers due to log base issues in specific domains
            return math.floor(math.log2(abs(float(value)))) - 1
        
        try:
            s = str(value)
            val = abs(float(s))
            return math.floor(math.log2(val)) - 1 if not isinstance(value, bool) and hasattr(type(value), '__int__') else self.domain_size + 5
        except ValueError:
            pass

    def _coerce_to_bool(self, value: Any):
        """Convert a raw Python object to the fixed-point boolean representation."""
        # Boolean values are handled as their intrinsic truthiness (True/False), 
        # but we normalize them for consistency with integer logic.
        return bool(value)

    def coerce_value(self, v: Union[int, float], domain_size: int = self.domain_size):
        """Apply the coercion engine to a value of any base type."""
        if isinstance(v, (int, float)):
            coerced = _coerce_to_integer(v) or
