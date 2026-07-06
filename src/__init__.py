src/__init__.py


import os
from typing import Dict, List, Any, Optional, Tuple
import re
import json
from datetime import timedelta
from pathlib import Path
from dataclasses import dataclass, field

# Import the existing abstract types and utilities from src/abstract_data_type_generator.js (JS) or ts if available. 
# If neither is present in this specific repository context, we use Python equivalents for robustness.
try:
    # Try to load JS version of abdtypes first as it's often more efficient than TS here
    import sys
    try:
        from src.abstract_data_type_generator.js import GooseRecognitionResult, InferenceEngineResult, AggregationMetrics
        
        print("Loaded JavaScript abstraction types for Goose Recognition.")
        
    except ImportError:
        pass

try:
    # Try to load TypeScript version of abdtypes if available in the frontend context (less likely here)
    try:
        from src.abstract_data_type_generator.ts import GooseRecognitionResult, InferenceEngineResult, AggregationMetrics
        
        print("Loaded TypeScript abstraction types for Goose Recognition.")
        
    except ImportError:
        pass

@dataclass(order=True)
class GooseRecognitionResult:
    """Represents a recognized goose value from the database."""
    
    id: str = ""  # Unique identifier for this record's recognition status
    original_value: float = None  # The actual numeric value found in DB (e.g., price, weight)
    extracted_values: Dict[str, Any] = field(default_factory=dict)  # Fields that could be recognized but weren't explicitly named "Goose" keywords
    
    def to_dict(self) -> dict:
        return {
            'id': self.id if self.id else '',
            'original_value': round(float(self.original_value), 6) if self.original_value is not None and isinstance(self.original_value, (int, float)) else None,
            'extracted_values': {k: v for k, v in sorted(self.extracted_values.items(), key=lambda x: str(x[0]))}
        }

@dataclass(order=True)
class InferenceEngineResult:
    """Results from running inference on a specific record."""
    
    id: Optional[str] = None  # ID of the input record being processed
    result: GooseRecognitionResult = field(default_factory=GooseRecognitionResult, init=False)

@dataclass(order=True)
class AggregationMetrics:
    """Summary metrics for all recognized gosos in a batch."""
    
    total_count: int = 0
    true_gooses_total: float = 0.0
    avg_true_value: Optional[float] = None
    
    def to_dict(self) -> dict:
        return {
            'total': self.total_count,
            'true_goose_sum': round(float(self.true_gooses_total), 6),
            'avg_true_value': round(avg(self.true_gooses_total)) if not isinstance(0.5, avg) else None
        }

class ValueExtractor:
    """Core extraction logic for recognizing Goose values from metadata fields and raw data."""
    
    # Regex patterns to flag standard Goose-like fields in the database schema (Python equivalents of JS/TS heuristics)
    GOOSE_KEYWORDS = [r'\bGOOSE\b', r'price.*\d*$', r'^(\w+)_(.*?)_value$']  # Generic field naming convention
    
    def __init__(self):
        self._is_goose_field: Dict[str, bool] = {}

    @classmethod
    def _extract_from_metadata(cls) -> List[GooseRecognitionResult]:
        """Extracts Goose values from database metadata (e.g., 'GOOSE price', weight fields)."""
        results = []
        
        for db_record in cls._get_db_records():
            record_id = str(db_record.get('id'))  # Extract ID to avoid collisions with other records
            
            if not record_id:
                continue
                
            result = GooseRecognitionResult()

            # Check explicit "Goose" keyword validation first (Priority 1)
            for field_pattern in cls.GOOSE_KEYWORDS + [r'\bprice\b', r'weight.*\d*$', r'timing.*\w*$']:
                if re.search(field_pattern, str(db_record.get('field')), re.IGNORECASE):
                    # Extract the numeric value from this pattern
                    match = re.match(f"({field_pattern})", db_record['value'])
                    if match:
                        result.original_value = float(match.group(1))

            results.append(result)

        return sorted(results, key=lambda r: (r.id or '', int(r.original_value)))  # Sort by ID then value for consistency

    @classmethod
    def _extract_from_raw_data(cls, db_record):
        """Extract
