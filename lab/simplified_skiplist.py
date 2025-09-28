import random

# Create a node with given level, key and value
def create_node(level, key, value):
    return {
        "key": key,
        "value": value,
        "forward": [None] * level  # Forward pointers for each level
    }

# Randomly choose the level for a new node (probability-based)
def random_level(max_level=16, p=0.5):
    level = 1
    while random.random() < p and level < max_level:
        level += 1
    return level

# Create a new skip list
def create_skiplist():
    max_level = 16
    p = 0.5
    head = create_node(max_level, float('-inf'), None)
    return {
        "head": head,
        "level": 1,
        "size": 0,
        "max_level": max_level,
        "p": p
    }

# Search for a key in the skip list
def search(skiplist, key):
    current = skiplist["head"]

    # Start from the top level and go down
    for level in reversed(range(skiplist["level"])):
        while current["forward"][level] and current["forward"][level]["key"] < key:
            current = current["forward"][level]

    # Move to next node
    current = current["forward"][0]

    # Check if it's the key we're looking for
    if current and current["key"] == key:
        return current["value"]
    return None

# Insert or update a key-value pair
def insert(skiplist, key, value):
    update = [None] * skiplist["max_level"]
    current = skiplist["head"]

    # Find the place to insert
    for level in reversed(range(skiplist["level"])):
        while current["forward"][level] and current["forward"][level]["key"] < key:
            current = current["forward"][level]
        update[level] = current

    # Move to next node at level 0
    next_node = current["forward"][0]

    # If the key already exists, update its value
    if next_node and next_node["key"] == key:
        next_node["value"] = value
        return

    # Otherwise, create a new node
    new_level = random_level(skiplist["max_level"], skiplist["p"])
    if new_level > skiplist["level"]:
        for i in range(skiplist["level"], new_level):
            update[i] = skiplist["head"]
        skiplist["level"] = new_level

    new_node = create_node(new_level, key, value)

    # Insert the new node into all relevant levels
    for i in range(new_level):
        new_node["forward"][i] = update[i]["forward"][i]
        update[i]["forward"][i] = new_node

    skiplist["size"] += 1

# Delete a key from the skip list
def delete(skiplist, key):
    update = [None] * skiplist["max_level"]
    current = skiplist["head"]

    for level in reversed(range(skiplist["level"])):
        while current["forward"][level] and current["forward"][level]["key"] < key:
            current = current["forward"][level]
        update[level] = current

    target = current["forward"][0]

    if target and target["key"] == key:
        for i in range(skiplist["level"]):
            if update[i]["forward"][i] != target:
                break
            update[i]["forward"][i] = target["forward"][i]

        # Reduce level if necessary
        while skiplist["level"] > 1 and skiplist["head"]["forward"][skiplist["level"] - 1] is None:
            skiplist["level"] -= 1

        skiplist["size"] -= 1
        return True

    return False

# Return all key-value pairs in order
def items(skiplist):
    current = skiplist["head"]["forward"][0]
    result = []
    while current:
        result.append((current["key"], current["value"]))
        current = current["forward"][0]
    return result


# Create a new skip list
sl = create_skiplist()

# Insert some key-value pairs
insert(sl, 10, "Apple")
insert(sl, 20, "Banana")
insert(sl, 15, "Cherry")

print("All items:", items(sl))  # [(10, 'Apple'), (15, 'Cherry'), (20, 'Banana')]

# Search for a key
print("Search 15:", search(sl, 15))  # "Cherry"

# Update a key
insert(sl, 15, "Updated Cherry")
print("After update:", items(sl))

# Delete a key
delete(sl, 20)
print("After delete:", items(sl))
