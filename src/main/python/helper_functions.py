

def get_offset(entities):
    offsets = []
    for e in entities:
        offsets.append([e.begin, e.end])

    return offsets


def get_event_mention(cas, e_mentions, e_m_begins, begin, end):
    i = 0
    for b in e_m_begins:
        if b == begin:
            return e_mentions[i]
        i += 1
    i = 0
    event_men_type = cas.typesystem.get_type(ctakes_types.Procedure)
    return create_type.add_type(cas, event_men_type, begin, end)

def get_event_mention(cas, e_mentions, e_m_begins, begin, end):
    i = 0
    for b in e_m_begins:
        if b == begin:
            return e_mentions[i]
        i += 1
    i = 0
    event_men_type = cas.typesystem.get_type(ctakes_types.EventMention)
    return create_type.add_type(cas, event_men_type, begin, end)

def get_event_mention(cas, e_mentions, e_m_begins, begin, end):
    i = 0
    for b in e_m_begins:
        if b == begin:
            return e_mentions[i]
        i += 1
    i = 0
    event_men_type = cas.typesystem.get_type(ctakes_types.EventMention)
    return create_type.add_type(cas, event_men_type, begin, end)

