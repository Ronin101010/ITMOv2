subscribers = set()
MAX_SUBSCRIBERS = 100


def subscribe(name):
    # Feature A: reject empty or overly long names (basic input validation)
    if not name.strip():
        raise ValueError("empty name")
    if len(name) > 255:
        raise ValueError("name too long")

    # Feature B: simulate dependency failure handling
    # For demo purposes, a test may toggle service.fail_dependency = True
    if globals().get("fail_dependency"):
        # In a real app this could be a timeout or external error; here we raise a clear error
        raise RuntimeError("dependency failure: LLM timeout or upstream error")
    norm = name.strip()
    # Capacity limit: do not count duplicates; only block when adding a new unique subscriber over capacity
    if norm not in subscribers and len(subscribers) >= MAX_SUBSCRIBERS:
        raise RuntimeError("capacity exceeded")
    subscribers.add(norm)
    return {"subscribed": True}
