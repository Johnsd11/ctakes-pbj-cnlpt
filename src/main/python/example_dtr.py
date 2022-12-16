from ctakes_pbj.cas_handlers import cas_annotator
from ctakes_pbj.pbj_tools import ctakes_types
import asyncio
from cnlpt.api.cnlp_rest import EntityDocument
import cnlpt.api.dtr_rest as dtr_rest
import time

from pprint import pprint

sem = asyncio.Semaphore(1)


class ExampleDtr(cas_annotator.CasAnnotator):

    def initialize(self):
        # startup_event()
        print("starting init " + str(time.time()))
        asyncio.run(self.init_caller())

        print("done with init " + str(time.time()))

    def process(self, cas):
        print("processing")
        entities = cas.select(ctakes_types.EventMention)

        offsets = []
        for e in entities:
            offsets.append([e.begin, e.end])

        print("calling dtr caller" + str(time.time()))
        asyncio.run(self.dtr_caller(cas, entities, offsets))
        print("done calling dtr " + str(time.time()))

    async def init_caller(self):
        await dtr_rest.startup_event()

    async def dtr_caller(self, cas, entities, offsets):
        event_type = cas.typesystem.get_type(ctakes_types.Event)
        event_properties_type = cas.typesystem.get_type(ctakes_types.EventProperties)
        text = cas.sofa_string
        eDoc = EntityDocument(doc_text=text, entities=offsets)

        #async with sem:
        dtr_output = await dtr_rest.process(eDoc)
        i = 0
        rj = dtr_output.json()
        pprint(rj)
        for e in entities:
            eProps = event_properties_type()
            eProps.set("docTimeRel", dtr_output.statuses[i])

            eProps.docTimeRel = dtr_output.statuses[i]
            cas.add(eProps)

            event = event_type()
            cas.add(event)
            event.properties = eProps

            e.event = event

            print(e.get_covered_text() + " " + dtr_output.statuses[i])
            i += 1
