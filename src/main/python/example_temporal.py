import cas_annotator
from ctakes_pbj.pbj_tools import ctakes_types
from ctakes_pbj.pbj_tools import create_type

import asyncio

# from cnlpt.api.temporal_rest import *
from cnlpt.api.temporal_rest import startup_event as temporal_init
from cnlpt.api.temporal_rest import process as temporal_process
from cnlpt.api.cnlp_rest import EntityDocument
# from cnlpt.api.temporal_rest import SentenceDocument
import cnlpt.api.temporal_rest as temporal_rest
import time

from pprint import pprint

sem = asyncio.Semaphore(1)


class ExampleTemporal(cas_annotator.CasAnnotator):

    def initialize(self):
        # startup_event()
        print("starting init " + str(time.time()))
        asyncio.run(self.init_caller())

        print("done with init " + str(time.time()))

    def process(self, cas):
        print("processing")
        sentences = cas.select(ctakes_types.Sentence)

        print("calling temporal caller" + str(time.time()))
        asyncio.run(self.temporal_caller(cas, sentences))
        print("done calling temporal " + str(time.time()))

    async def init_caller(self):
        await temporal_rest.startup_event()

    async def temporal_caller(self, cas, sentences):
        event_type = cas.typesystem.get_type(ctakes_types.Event)
        event_men_type = cas.typesystem.get_type(ctakes_types.EventMention)
        timex_type = cas.typesystem.get_type(ctakes_types.TimeMention)
        relation_type = cas.typesystem.get_type(ctakes_types.TemporalRelation)
        event_properties_type = cas.typesystem.get_type(ctakes_types.EventProperties)

        #async with sem:
        # dtr_output = await temporal_rest.process(eDoc)
        i = 0
        for s in sentences:
            text = s.get_covered_text()
            sentence_begin = s.begin
            sentence_doc = temporal_rest.SentenceDocument(sentence=text)

            temporal_result = await temporal_rest.process_sentence(sentence_doc)
            rj = temporal_result.json()
            pprint(rj)

            for t in temporal_result.timexes:
                for tt in t:

                    timex = timex_type()
                    timex.set('begin', tt.begin)
                    # timex.begin = tt.begin
                    # timex.end = tt.end
                    timex.set('end', tt.end)
                    cas.add(timex)

            for e in temporal_result.events:
                for ee in e:

                    eProps = event_properties_type()
                    eProps.set("docTimeRel", ee.dtr)
                    event = event_type()
                    event.properties = eProps
                    # event.begin = ee.begin
                    # event.end = ee.end
                    # event.set('begin', ee.begin)
                    # event.set('end', ee.end)
                    event_mention = event_men_type()
                    event_mention.event = event
                    event_mention.begin = ee.begin
                    event_mention.end = ee.end
                    cas.add(event)
                    cas.add(event_mention)

            for r in temporal_result.relations:
                for rr in r:
                    print(rr.arg1, rr.arg2, rr.arg1_start, rr.arg2_start)





