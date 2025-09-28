# ----------------- Core Dictionary -----------------
def create_dict(capacity=10):
    return {"capacity": capacity, "size": 0, "table": [[] for _ in range(capacity)]}


def _hash(d, key):
    return hash(key) % d["capacity"]


def _rehash(d):
    """Double the capacity and reinsert all items."""
    old_items = items(d)
    d["capacity"] *= 2
    d["table"] = [[] for _ in range(d["capacity"])]
    d["size"] = 0
    for k, v in old_items:
        insert(d, k, v)


def insert(d, key, value):
    """Insert or update a key-value pair."""
    index = _hash(d, key)
    bucket = d["table"][index]

    # update if exists
    for pair in bucket:
        if pair[0] == key:
            pair[1] = value
            return

    # otherwise insert new
    bucket.append([key, value])
    d["size"] += 1

    # resize if load factor > 0.7
    if d["size"] / d["capacity"] > 0.7:
        _rehash(d)


def search(d, key):
    """Return value for key, or None if not found."""
    index = _hash(d, key)
    for pair in d["table"][index]:
        if pair[0] == key:
            return pair[1]
    return None


def delete(d, key):
    """Delete a key from dictionary. Return True if deleted."""
    index = _hash(d, key)
    bucket = d["table"][index]
    for i, pair in enumerate(bucket):
        if pair[0] == key:
            bucket.pop(i)
            d["size"] -= 1
            return True
    return False


def items(d):
    """Return all (key, value) pairs."""
    result = []
    for bucket in d["table"]:
        for pair in bucket:
            result.append((pair[0], pair[1]))
    return result


def show(d):
    """Pretty print dictionary content."""
    return "{" + ", ".join(f"{k}: {v}" for k, v in items(d)) + "}"
