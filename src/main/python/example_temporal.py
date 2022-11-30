import cas_annotator
from ctakes_types import *
import asyncio
# from cnlpt.api.dtr_rest import *
from cnlpt.api.dtr_rest import startup_event as dtr_init
from cnlpt.api.dtr_rest import process as dtr_process
from cnlpt.api.cnlp_rest import EntityDocument
import cnlpt.api.dtr_rest as dtr_rest
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
        entities = cas.select(EventMention)

        offsets = []
        for e in entities:
            offsets.append([e.begin, e.end])

        print("calling dtr caller" + str(time.time()))
        asyncio.run(self.dtr_caller(cas, entities, offsets))
        print("done calling dtr " + str(time.time()))

    async def init_caller(self):
        await dtr_rest.startup_event()

    async def dtr_caller(self, cas, entities, offsets):
        event_mention_type = cas.typesystem.get_type(EventMention)
        event_type = cas.typesystem.get_type(Event)
        event_properties_type = cas.typesystem.get_type(EventProperties)
        text = cas.sofa_string
        eDoc = EntityDocument(doc_text=text, entities=offsets)

        #async with sem:
        dtr_output = await dtr_rest.process(eDoc)
        i = 0
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
