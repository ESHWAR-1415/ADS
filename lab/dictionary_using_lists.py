# dictionary implemented using lists (hash table with chaining)

TABLE_SIZE = 10  # fixed number of buckets


def create_dict():
    """Create an empty dictionary (list of buckets)."""
    return [[] for _ in range(TABLE_SIZE)]


def hash_func(key):
    """Simple hash function: sum of char codes mod TABLE_SIZE."""
    return sum(ord(c) for c in str(key)) % TABLE_SIZE


def insert(d, key, value):
    """Insert or update key in dictionary."""
    index = hash_func(key)
    bucket = d[index]

    # check if key already exists -> update
    for pair in bucket:
        if pair[0] == key:
            pair[1] = value
            return

    # otherwise append new key–value pair
    bucket.append([key, value])


def search(d, key):
    """Search for a key and return its value or None."""
    index = hash_func(key)
    bucket = d[index]

    for pair in bucket:
        if pair[0] == key:
            return pair[1]
    return None


def delete(d, key):
    """Delete a key from dictionary, return True if deleted."""
    index = hash_func(key)
    bucket = d[index]

    for i, pair in enumerate(bucket):
        if pair[0] == key:
            bucket.pop(i)
            return True
    return False


def items(d):
    """Return all (key, value) pairs as a list."""
    all_items = []
    for bucket in d:
        for pair in bucket:
            all_items.append((pair[0], pair[1]))
    return all_items


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    mydict = create_dict()

    insert(mydict, "apple", 10)
    insert(mydict, "banana", 20)
    insert(mydict, "orange", 30)

    print("Dictionary items:", items(mydict))
    print("Search 'banana':", search(mydict, "banana"))

    insert(mydict, "banana", 25)  # update value
    print("After update:", items(mydict))

    delete(mydict, "apple")
    print("After delete:", items(mydict))
