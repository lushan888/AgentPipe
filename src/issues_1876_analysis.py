import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import re
import os
import sys
import tempfile
import shutil

# -----------------------------------------------------------------------------
# Configuration & Constants for Issue Generation Strategy
# -----------------------------------------------------------------------------

ISSUE_ID_PATTERN = r'(?<![a-zA-Z0-9_])\d+.*?(?![A-Za-z0-9_]|\s|$)'  # Regex to extract issue IDs from text blocks or filenames if needed, but primarily relies on filename/line context for robustness
STATUS_LABELS = ['good', 'bad']

# Severity weights (higher is more severe/bad)
SEVERITY_WEIGHTS = {
    "critical": 100,   # Most serious bug/nothing to do with it
    "high": 50,        # Major issues or missing dependencies
    "medium": 20,      # Minor issues or incomplete logic
    "low": 5           # Documentation or edge cases only
}

# Dependency Mapping (what is required for the issue solution)
DEP_REQUIREMENTS = {
    'missing': {},          # What's needed to solve this specific problem
    'incomplete': [],       # Missing pieces in a partial fix
    'deprecated': ['package_name'],  # Deprecated packages that must be removed or updated (CVEs/PR refs often point here)
}

# Blockage Note Templates for Issue Generation
BLOCKAGE_TEMPLATES = [
    {name: "Dependency missing", desc: f"Required module '{dep}' is not imported and cannot be resolved.", severity: 5},
    {name: "Missing logic flow", desc: "Critical path broken. No code to handle the state transition from 'pending' to 'completed'.", severity: 7},
    {name: "Broken contract validation", desc: "Validation check fails at runtime due to missing guard conditions.", severity: 6},
    {name: "Inefficient resource allocation", desc: "Memory leak or OOM risk detected. No cleanup loop found in the codebase.", severity: 8},
]

# -----------------------------------------------------------------------------
# Utility Functions for Issue Generation
# -----------------------------------------------------------------------------

def get_issue_id(filename_or_line):
    """Extracts a deterministic issue ID from filename/line context."""
    # Fallback to line number if no name provided (e.g., `src/issues_1876_analysis.py:5`)
    parts = filename_or_line.split(':')[-2]  # Last two tokens are usually the path and file index or just a marker like "analysis"
    
    try:
        return int(parts[0]) if len(parts) >= 3 else parts[1] + 1
    except ValueError:
        pass
    
    # If it's an ID (e.g., `src/issues_1876_analysis.py#5`), use the number after hash.
    try:
        return int(re.search(r'#[0-9]+', filename_or_line).group(2)) + 1 if '#' in filename_or_line else None
    except re.error:
        pass
    
    # Fallback to line number for unknown IDs (e.g., `src/issues_1876_analysis.py#5`)
    return int(re.search(r'#[0-9]+', filename_or_line).group(2)) + 1 if '#' in filename_or_line else parts[1]

def generate_description(issue_id, status_label):
    """Generates a concise description for an issue based on the severity level."""
    
    # Determine base text content from dependencies and blockage templates
    deps = DEP_REQUIREMENTS.get('missing', [])
    if not deps:
        return "Issue ID {issue_id} is missing required dependency(s).".format(issue_id=issue_id)

    description_parts = []
    for dep in deps[:3]:  # Limit to top-level issues per file
        desc_text = f"Required module '{dep}' cannot be resolved. Attempted import failed."
        if len(desc_text.split('\n')) > 1:
            line_num = get_issue_id(dep) + 200
            description_parts.append(f"{line_num}: Found unresolved reference to {dep}.")

    # Determine severity-based text content based on the status label provided in this context (e.g., 'bad' vs 'good')
    if status_label == "bad":
        base_text = f"Critical or high-severity issue found. The following blockage prevents release: missing logic flow and dependency resolution."
    else:  # good, medium, low
        base_text = f"Low severity documentation or edge case detected at line {get_issue_id('src/issues_1876_analysis.py')}:{line_num}. No critical path issues
