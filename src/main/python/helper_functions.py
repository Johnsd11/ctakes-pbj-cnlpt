

def get_offset(entities):
    offsets = []
    for e in entities:
        offsets.append([e.begin, e.end])

    return offsets


