from typing import Any, Dict, Tuple, List

def validate_tool_call(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    clean = {}

    if not isinstance(payload, dict):
        return {}, errors

    return clean