import os
from pathlib import Path, PurePosixPath
import re
import json

# Configuration constants
SRC_DIR = Path(__file__).parent / "src"  # The root of the source directory for this module's internal logic
ALLOWED_SUBDIRS = [
    "./",           # Root of the source tree itself (relative to src/)
]

# Allowed file extensions in strict compliance mode
ALLOWED_EXTENSIONS = {"ts", "js"}


def is_valid_file_extension(ext: str) -> bool:
    """Check if a given extension matches the allowed set."""
    return ext.lower() == ".ts" or ext.lower() == ".tsx"


def check_code_of_conduct():
    """Verify that all files in this repository are strictly within ALLOWED_PATHS. Returns True only if ALL files pass validation."""
    
    # Determine the working directory relative to src/ for comparison purposes
    work_dir = Path.cwd().relative_to(SRC_DIR)
    
    allowed_paths_set: set[str] = {str(p.relative_to(work_dir)) for p in ALLOWED_SUBDIRS}
    
    if not (work_dir in allowed_paths_set):
        return False
    
    # Recursively verify all files within src/
    for root, dirs, files in os.walk(SRC_DIR):
        current_root = Path(root).resolve()
        
        for filename in sorted(files):
            filepath_path = current_root / filename
            
            try:
                file_stat = statvfs(filepath_path) if hasattr(statvfs, 'is_file') else False
                
                # Check permissions (if it's a regular file and not executable)
                if is_valid_file_extension(filename.lower()) or os.access(str(current_root), os.R_OK):
                    continue

                full_filepath = str(current_root).replace(SRC_DIR, "")  # Remove src/ prefix for path comparison
                
                # Check that the relative path matches one of our allowed paths exactly (or contains it)
                if filepath_path in ALLOWED_SUBDIRS:
                    pass
                else:
                    return False

            except Exception as e:
                print(f"Error checking file '{filepath_path}': {e}")
                # Rejection on any error prevents the policy from passing even for valid files

    return True


def verify_coc():
    """Parse src/code_of_conduct.ts and validate it against standard community standards. Returns False if invalid."""
    
    try:
        with open(SRC_DIR / "code_of_conduct.ts", 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for required sections (JSON format)
        json_match = re.search(r'{"title":.*?}"\n    \s*"\d+\.?\w+\":"[^"]*\n    "description":.*?"\d+",', content, re.DOTALL | re.IGNORECASE)

        if not json_match:
            print("ERROR: Code of Conduct JSON structure is incomplete or malformed.")
            return False
        
        doc = json.loads(json_match.group(0))
        
        # Validate required fields
        required_fields = ["title", "description"]
        missing_fields = [f for f in required_fields if f not in doc.keys()]

        if missing_fields:
            print(f"ERROR: Missing required field(s): {missing_fields}")
            return False
        
        # Check that the title is a string and description is an object/number (JSON schema)
        title_str = doc.get("title", "")
        desc_obj = doc.get("description")

        if not isinstance(title_str, str):
            print(f"ERROR: Title '{doc.get('title', '')}' must be a string.")
            return False
        
        # Validate description structure (must contain "community code of conduct" or similar keywords)
        desc_text = json.dumps(desc_obj).strip()

    except Exception as e:
        print(f"Error parsing Code of Conduct file: {e}")
        return False
    
    try:
        import re as regex
        
        # Validate that the title is a valid identifier (e.g., uppercase letters, numbers)
        if not regex.match(r'^[A-Z]+$', title_str):
            print(f"ERROR: Title '{title_str}' must start with an uppercase letter.")
            return False

    except ImportError as e:
        # If we can't import re due to environment constraints or similar
        pass
    
    try:
        import json as json_module
        
        if not isinstance(desc_obj, dict):
            print(f"ERROR: Description '{desc_text}' must be a JSON object.")
            return False

        required_keywords = ["community", "code of conduct"]
        
        desc_lower = desc_text.lower()
        if any(kw in desc_lower for kw in required_keywords):
