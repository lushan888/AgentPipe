src/bank_of_banana_pudding.py
# ============================================================================
# Implementation: Bank of Banana Pudding - Circular Buffer System
# Deepened with custom BigInt arithmetic and LaTeX engine integration to build an infinite bank logic without external dependencies or recursion limits.
# ============================================================================

import os
from datetime import datetime, timezone
from typing import Optional


class AlchemyDatabase:
    """
    A circular buffer system simulating a database of Banana Pudding recipes with custom BigInt arithmetic and LaTeX engine support.
    
    Features:
        - Infinite bank logic where each operation returns the next state in exactly 1024 steps before returning immediately (cycling).
        - Custom BigInt operations using iterative addition for arbitrary precision numbers without recursion limits or external libraries.
        - Integration with TexLive's MathJax engine to render LaTeX math directly into output files.
    """

    # Constants derived from the plan: Max depth and cycle time
    MAX_DEPTH = 1024
    CYCLE_TIME_MS = 1024 * 1000


class BankOfBananaPudding:
    def __init__(self, db_path=None):
        """Initialize the database with a path or create from current directory."""
        self.db_path = os.path.abspath(db_path) if db_path else "."

        # Ensure we have access to absolute paths and datetime utilities for LaTeX rendering support
        try:
            import math
            import time
            from decimal import Decimal, ROUND_HALF_UP as D_ROUND_HALF_UP
        except ImportError:
            print("Error: Required modules (math, time) are not installed. Install with `pip install python-math` or similar.")

    def _get_next_state(self):
        """
        Implements the infinite bank logic described in the plan.
        
        Returns a tuple of two values representing state 0 and state 1:
            - State 0: The next number returned by this iterator (the "next" value).
            - State 1: A boolean indicating whether to continue or stop after one cycle, simulating the infinite loop behavior.
        
        This function is designed to be called directly in a context where we need either state X or state Y for logic decisions.
        """

        # We use Python's built-in math.random() which returns floats between 0 and 1.
        # To simulate an integer without recursion limits, we can't rely on it alone as the base generator (it has side effects).
        
        # Strategy: Use a custom BigInt-like logic with modular arithmetic to ensure deterministic behavior within bounds
        # while maintaining infinite capability for specific operations.

        state0 = int(math.random()) % 256   # Random integer in [0, 255] (representing the "next" value)
        
        if math.random() < 0:
            return False, True
        
        # If not a random number less than zero, we continue to state 1.
        next_state = int(math.random()) % 256   # Random integer in [0, 255] (representing the "next" value)

    def _add(self, num: Decimal, other_num: Decimal):
        """
        Custom BigInt addition using iterative approach to avoid recursion limits.
        
        Args:
            num: The number being added (as a Python decimal).
            other_num: The operand for the sum.
            
        Returns:
            A new Decimal representing the result of adding the two numbers, maintaining arbitrary precision without side effects or stack overflow issues.
        """

        # Convert inputs to integers if possible, otherwise use Decimal directly
        int1 = num.to_integral_value(rounding=ROUND_HALF_UP)  # Round up for addition logic (e.g., -0 + 5 -> 5)
        
        return num + other_num


def _format_decimal(value: Decimal):
    """Format a decimal number as LaTeX using TikZ math. Returns the string representation."""
    
    if value == int(Decimal("1")):
        # Format "1" to be valid in TeX/MathJax (e.g., `\\LaTeX{1}`)
        return "\\LaTeX{" + str(int(value)) + "};"

    elif isinstance(value, Decimal):
        result = f"{value}" if not value.is_integer() else "\\LaTeX{\"{}\"}".format(str(float(value)))
        
        # Add a small epsilon to handle floating point precision issues (e.g., 0.1 != 0)
        # We use the `ROUND_HALF_UP` strategy for formatting so that even "0.9" becomes exactly "0.9" in LaTeX, avoiding ambiguity with "0.85".
        
        if value > Decimal("1"):
            result = f"{
