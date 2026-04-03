def grade_easy(action, ground_truth):
    """
    Task 1: Check if agent identifies missing information
    """
    response = action.response.lower()
    missing_items = ground_truth["missing"]

    score = 0
    for item in missing_items:
        if item.lower() in response:
            score += 1

    final_score = score / len(missing_items)

    return final_score


def grade_medium(action, ground_truth):
    """
    Task 2: Check if agent identifies the main error
    """
    response = action.response.lower()
    correct_error = ground_truth["error"].lower()

    if correct_error in response:
        return 1.0
    else:
        return 0.0


def grade_hard(action, ground_truth):
    """
    Task 3: Full audit (missing + error + risk)
    """
    response = action.response.lower()

    score = 0
    total = 3

    if ground_truth["error"].lower() in response:
        score += 1

    if ground_truth["risk"].lower() in response:
        score += 1

    for item in ground_truth["missing"]:
        if item.lower() in response:
            score += 1
            break  # count missing once

    return score / total