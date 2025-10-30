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

    # 'q' validation
    if action == "search":
        q = payload.get("q")
        if not isinstance(q, str) or not q.strip():
            errors.append("Missing or empty 'q' for search action.")
            return {}, errors
        clean["q"] = q.strip()

    # 'k' validation
    k = payload.get("k", 3)
    try:
        k = int(k)
    except (ValueError, TypeError):
        errors.append("'k' must be a number. Defaulting to 3.")
        k = 3

    if not (1 <= k <= 5):
        errors.append("'k' must be between 1 and 5. Defaulting to 3.")
        k = 3

    clean["k"] = k

    return clean, errors