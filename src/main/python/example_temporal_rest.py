from ctakes_pbj.cas_handlers import cas_annotator
from ctakes_pbj.pbj_tools import ctakes_types
from ctakes_pbj.pbj_tools import create_type
import requests
from pprint import *


class ExampleTemporalRest(cas_annotator.CasAnnotator):

    def process(self, cas):

        process_url = 'http://localhost:8000/temporal/process_sentence'
        event_mention_type = cas.typesystem.get_type(ctakes_types.EventMention)
        event_type = cas.typesystem.get_type(ctakes_types.Event)
        event_properties_type = cas.typesystem.get_type(ctakes_types.EventProperties)

        for sentence in cas.select(ctakes_types.Sentence):
            text = sentence.get_covered_text()
            sentenceBegin = sentence.begin
            r = requests.post(process_url, json={'sentence': text})
            rj = r.json()
            pprint(rj)
            # check first if events is not empty
            evlist = rj['events']
            for ev in evlist:
                for e in ev:
                    begin = -1
                    end = -1
                    dtr = ''
                    for k, v in e.items():
                        if k == 'begin':
                            begin = int(v) + sentenceBegin - 1
                        elif k == 'dtr':
                            dtr = v
                        elif k == 'end':
                            end = int(v)+2 + sentenceBegin
                        if begin != -1 and end != -1 and dtr != '':

                            eProps = event_properties_type()
                            # eProps.set("docTimeRel", dtr)
                            eProps.docTimeRel = dtr
                            cas.add(eProps)

                            event = event_type()
                            # event.set("properties", eProps)
                            cas.add(event)
                            event.properties = eProps

                            event_mention = create_type.add_type(cas, event_mention_type, begin, end)
                            event_mention.event = event




