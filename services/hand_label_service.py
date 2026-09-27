def get_hand_label(results, hand_index=0):
    if not results.multi_handedness:
        return "Unknown"

    return results.multi_handedness[hand_index].classification[0].label