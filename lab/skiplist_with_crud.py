import random

MAX_LEVEL = 16  # maximum height of the skiplist
P = 0.5         # probability factor for level generation


def create_node(level, key, value):
    """Create a skiplist node as a dict."""
    return {"key": key, "value": value, "forward": [None] * level}


def random_level():
    """Randomly generate a level for a new node."""
    lvl = 1
    while random.random() < P and lvl < MAX_LEVEL:
        lvl += 1
    return lvl


def create_skiplist():
    """Initialize an empty skiplist."""
    head = create_node(MAX_LEVEL, float("-inf"), None)
    return {"head": head, "level": 1, "size": 0}


def search(skiplist, key):
    """Search for a key in the skiplist."""
    x = skiplist["head"]
    for i in range(skiplist["level"] - 1, -1, -1):
        while x["forward"][i] and x["forward"][i]["key"] < key:
            x = x["forward"][i]
    x = x["forward"][0]
    if x and x["key"] == key:
        return x["value"]
    return None


def insert(skiplist, key, value):
    """Insert or update a key in the skiplist."""
    update = [None] * MAX_LEVEL
    x = skiplist["head"]

    for i in range(skiplist["level"] - 1, -1, -1):
        while x["forward"][i] and x["forward"][i]["key"] < key:
            x = x["forward"][i]
        update[i] = x

    next_node = x["forward"][0]
    if next_node and next_node["key"] == key:
        next_node["value"] = value  # update value
        return

    lvl = random_level()
    if lvl > skiplist["level"]:
        for i in range(skiplist["level"], lvl):
            update[i] = skiplist["head"]
        skiplist["level"] = lvl

    new_node = create_node(lvl, key, value)
    for i in range(lvl):
        new_node["forward"][i] = update[i]["forward"][i]
        update[i]["forward"][i] = new_node

    skiplist["size"] += 1


def delete(skiplist, key):
    """Delete a key from the skiplist."""
    update = [None] * MAX_LEVEL
    x = skiplist["head"]

    for i in range(skiplist["level"] - 1, -1, -1):
        while x["forward"][i] and x["forward"][i]["key"] < key:
            x = x["forward"][i]
        update[i] = x

    target = x["forward"][0]
    if target and target["key"] == key:
        for i in range(skiplist["level"]):
            if update[i]["forward"][i] != target:
                break
            update[i]["forward"][i] = target["forward"][i]

        while skiplist["level"] > 1 and not skiplist["head"]["forward"][skiplist["level"] - 1]:
            skiplist["level"] -= 1

        skiplist["size"] -= 1
        return True
    return False


def items(skiplist):
    """Return all (key, value) pairs in sorted order."""
    result = []
    x = skiplist["head"]["forward"][0]
    while x:
        result.append((x["key"], x["value"]))
        x = x["forward"][0]
    return result


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    sl = create_skiplist()

    # Insert values
    insert(sl, 10, "A")
    insert(sl, 20, "B")
    insert(sl, 15, "C")

    print("Items:", items(sl))  # [(10, 'A'), (15, 'C'), (20, 'B')]

    # Search
    print("Search 15:", search(sl, 15))  # "C"

    # Update
    insert(sl, 15, "Updated")
    print("After update:", items(sl))

    # Delete
    delete(sl, 20)
    print("After delete:", items(sl))
