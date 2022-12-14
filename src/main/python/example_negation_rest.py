import cas_annotator
from ctakes_pbj.pbj_tools import ctakes_types

import requests


class ExampleNegationRest(cas_annotator.CasAnnotator):

    def process(self, cas):

        process_url = 'http://localhost:8000/negation/process'

        eventMentions = cas.select(ctakes_types.EventMention)
        sites = cas.select(ctakes_types.AnatomicalSiteMention)
        entities = eventMentions + sites

        t = []
        for e in entities:
            t.append([e.begin, e.end])

        doc = {'doc_text': cas.sofa_string, 'entities': t}
        r = requests.post(process_url, json=doc)
        rj = r.json()
        neglist = rj['statuses']

        i = 0
        for e in entities:
            # -1 represents that it had happened, 1 represents that it is negated
            e.polarity = neglist[i]
            i += 1


