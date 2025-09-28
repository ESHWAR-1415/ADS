DELETED = "<deleted>"

def create_dict(capacity=10, method="chaining"):
    """Create a dictionary with chosen collision handling method."""
    return {
        "capacity": capacity,
        "size": 0,
        "table": [[] for _ in range(capacity)] if method=="chaining" else [None]*capacity,
        "method": method
    }

# ---------------- Hash Functions ----------------
def _hash1(d, key):
    return hash(key) % d["capacity"]

def _hash2(d, key):
    return 1 + (hash(key) % (d["capacity"] - 1))

# ---------------- Rehashing ----------------
def _rehash(d):
    old_items = items(d)
    d["capacity"] *= 2
    if d["method"] == "chaining":
        d["table"] = [[] for _ in range(d["capacity"])]
    else:
        d["table"] = [None] * d["capacity"]
    d["size"] = 0
    for k, v in old_items:
        insert(d, k, v)

# ---------------- Insert ----------------
def insert(d, key, value):
    method = d["method"]

    if method == "chaining":
        index = _hash1(d, key)
        bucket = d["table"][index]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        d["size"] += 1

    else:  # open addressing
        index = _hash1(d, key)
        i = 0
        while i < d["capacity"]:
            if method == "linear":
                new_index = (index + i) % d["capacity"]
            elif method == "quadratic":
                new_index = (index + i**2) % d["capacity"]
            elif method == "double":
                new_index = (index + i * _hash2(d, key)) % d["capacity"]

            slot = d["table"][new_index]
            if slot is None or slot == DELETED:
                d["table"][new_index] = [key, value]
                d["size"] += 1
                break
            elif slot[0] == key:
                slot[1] = value
                break
            i += 1
        else:
            raise Exception("Hashtable full!")

    if d["size"] / d["capacity"] > 0.7:
        _rehash(d)

# ---------------- Search ----------------
def search(d, key):
    method = d["method"]

    if method == "chaining":
        index = _hash1(d, key)
        bucket = d["table"][index]
        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return None

    else:  # open addressing
        index = _hash1(d, key)
        i = 0
        while i < d["capacity"]:
            if method == "linear":
                new_index = (index + i) % d["capacity"]
            elif method == "quadratic":
                new_index = (index + i**2) % d["capacity"]
            elif method == "double":
                new_index = (index + i * _hash2(d, key)) % d["capacity"]

            slot = d["table"][new_index]
            if slot is None:
                return None
            if slot != DELETED and slot[0] == key:
                return slot[1]
            i += 1
        return None

# ---------------- Delete ----------------
def delete(d, key):
    method = d["method"]

    if method == "chaining":
        index = _hash1(d, key)
        bucket = d["table"][index]
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                d["size"] -= 1
                return True
        return False

    else:  # open addressing
        index = _hash1(d, key)
        i = 0
        while i < d["capacity"]:
            if method == "linear":
                new_index = (index + i) % d["capacity"]
            elif method == "quadratic":
                new_index = (index + i**2) % d["capacity"]
            elif method == "double":
                new_index = (index + i * _hash2(d, key)) % d["capacity"]

            slot = d["table"][new_index]
            if slot is None:
                return False
            if slot != DELETED and slot[0] == key:
                d["table"][new_index] = DELETED
                d["size"] -= 1
                return True
            i += 1
        return False

# ---------------- Items ----------------
def items(d):
    method = d["method"]
    if method == "chaining":
        result = []
        for bucket in d["table"]:
            for pair in bucket:
                result.append((pair[0], pair[1]))
        return result
    else:
        return [(slot[0], slot[1]) for slot in d["table"] if slot not in (None, DELETED)]

# ---------------- Show ----------------
def show(d):
    return str(d["table"])


# Separate chaining
d1 = create_dict(method="chaining")
insert(d1, "apple", 10)
insert(d1, "banana", 20)
insert(d1, "orange", 30)
print("Chaining:", show(d1))

# Linear probing
d2 = create_dict(method="linear")
insert(d2, "apple", 10)
insert(d2, "banana", 20)
insert(d2, "orange", 30)
print("Linear probing:", show(d2))

# Quadratic probing
d3 = create_dict(method="quadratic")
insert(d3, "apple", 10)
insert(d3, "banana", 20)
insert(d3, "orange", 30)
print("Quadratic probing:", show(d3))

# Double hashing
d4 = create_dict(method="double")
insert(d4, "apple", 10)
insert(d4, "banana", 20)
insert(d4, "orange", 30)
print("Double hashing:", show(d4))
