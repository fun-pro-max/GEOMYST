import random

def pick_story(mysteries, state, seen_ids):
    state_events = [m for m in mysteries if m["state"] == state]

    if not state_events:
        return random.choice(mysteries)

    unseen = [m for m in state_events if m["id"] not in seen_ids]

    if unseen:
        return random.choice(unseen)

    # If all seen, rotate again
    return random.choice(state_events)
