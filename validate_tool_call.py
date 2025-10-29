from typing import Any, Dict, Tuple, List

def validate_tool_call(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    clean = {}
    errors = []

    if not isinstance(payload, dict):
        errors.append("Payload must be a dictionary.")
        return {}, errors

    return clean, errors