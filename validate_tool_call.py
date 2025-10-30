from typing import Any, Dict, List, Tuple

def validate_tool_call(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    clean = {}
    errors = []

    if not isinstance(payload, dict):
        errors.append("Payload must be a dictionary.")
        return {}, errors

    action = payload.get("action")
    if not isinstance(action, str):
        errors.append("Missing or invalid 'action'. Must be 'search' or 'answer'.")
        return {}, errors

    action = action.strip().lower()
    if action not in ["search", "answer"]:
        errors.append("Invalid 'action' value. Must be 'search' or 'answer'.")
        return {}, errors

    clean["action"] = action

    if action == "search":
        q = payload.get("q")
        if not isinstance(q, str) or not q.strip():
            errors.append("Missing or empty 'q' for search action.")
            return {}, errors
        clean["q"] = q.strip()

    return clean, errors