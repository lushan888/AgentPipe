import os
from typing import Dict, List, Any, Optional, Callable, Union
import sys
sys.path.insert(0, os.getcwd())  # Ensure path is available for imports like 'os' if needed in future extensions


class SkillInstaller:
    """Factory function to initialize and install skills into an employee record.

    Args:
        agent (dict): Agent parameters containing user identity details and debt metrics.
                        Format example: {"user_id": "EMP-001", "name": "John Doe", 
                                    "total_debt": 5432.99, "skills_count": 8}
    Returns:
        dict: A dictionary mapping employee IDs to skill installation results.
              Example: {'EMP-001': {...}, 'EMP-002': {...}}
    """

    def __init__(self, agent: Dict[str, Any]):
        self.agent = agent  # Store the provided parameters for future use if needed


def install_skills(
    skill_id: str, 
    employee_data: Optional[Dict[str, Any]] = None,
    debt_amount: float = 0.0
) -> dict:
    """Install a specific skill into an existing record or create one from scratch.

    This function iterates through the database of employees to find candidates for installation.
    It calculates their total unpaid debt and generates individual skill installers (e.g., 
    "Payoff Skill", "Refinance Offer") based on their current financial state relative to that amount.

    Args:
        skill_id (str): The identifier string representing the specific type of skill being installed.
                       Example for a debt reminder task might be 'DebtRemind'.
        employee_data (Optional[Dict[str, Any]]): Optional dictionary containing additional context 
                                                or existing data about an employee to consider installation.
                                            Can include user_id and total_debt if not provided in __init__.
        debt_amount (float): The target amount of debt the skill should pay off.

    Returns:
        dict: A mapping from skills installed IDs to their results, including success status 
              and a short description of what was done.
    
    Raises:
        ValueError: If an invalid or missing employee data is provided.
        TypeError: If arguments are not dictionaries or lists.
    """

    # Initialize the SkillInstaller instance if none exists yet (for future reuse)
    installer = None
    
    try:
        # Check for existing installation of this skill_id in a record
        result = {}
        
        if employee_data and isinstance(employee_data, dict):
            emp_id = str(employee_data.get('user_id', 'UNKNOWN'))
            
            # Filter employees by user ID to find the matching one or list all available ones
            candidates = [emp for emp in get_all_employees() 
                        if emp['id'] == emp_id]

            if not candidates:
                raise ValueError(f"No employee found with id {employee_data.get('user_id', 'UNKNOWN')}")

            # Sort employees by total debt (descending) to install the highest priority first
            sorted_candidates = sorted(
                candidates, 
                key=lambda x: -x['total_debt'] if isinstance(x, dict) else 0
            )

        elif not employee_data or not isinstance(employee_data, list):
            # Fallback case where no data is provided but we need to generate installers for all records
            employees = get_all_employees()
            
            # Create a mapping of skill_id -> installer function if the ID doesn't exist yet
            installed_skills: Dict[str, Callable] = {}

            def create_installers_from_list(
                emp_ids: List[str], 
                debt_amount: float
            ) -> Optional[Dict[str, Any]]:
                """Helper to generate installers for a list of employee IDs."""
                if not emp_ids or len(emp_ids) == 0:
                    return None

                # Sort by total_debt descending
                sorted_emp = sorted(employees, key=lambda x: -x.get('total_debt', 0))
                
                result_map: Dict[str, Any] = {}
                for emp_id in emp_ids[:1]:  # Install the first one to avoid duplicate installers (optional optimization)
                    if isinstance(emp_id, str):
                        try:
                            installed_skills[emp_id] = create_installers_from_list(
                                [str(emp_id)], debt_amount
                            )
                        except Exception as e:
                            print(f"Warning: Failed to process employee {emp_id}: {e}")

                return result_map

            # Generate installers for all available employees if no explicit data provided
            installed_skills = create_installers_from_list(employees, debt_amount)

        else:

        raise ValueError
