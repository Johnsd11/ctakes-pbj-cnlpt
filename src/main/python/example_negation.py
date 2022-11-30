import cas_annotator
from ctakes_types import *
import asyncio
import requests
from cnlpt.api.cnlp_rest import EntityDocument
import cnlpt.api.negation_rest as negation_rest
import time

sem = asyncio.Semaphore(1)


class ExampleNegation(cas_annotator.CasAnnotator):

    def initialize(self):
        # startup_event()
        print("starting init " + str(time.time()))
        asyncio.run(self.init_caller())

        print("done with init " + str(time.time()))

    def process(self, cas):

        print("processing")
        eventMentions = cas.select(EventMention)
        sites = cas.select(AnatomicalSiteMention)
        entities = eventMentions + sites

        offsets = []
        for e in entities:
            offsets.append([e.begin, e.end])

        print("calling negation caller" + str(time.time()))
        asyncio.run(self.negation_caller(cas, entities, offsets))
        print("done calling negation " + str(time.time()))

    async def init_caller(self):
        await negation_rest.startup_event()

    async def negation_caller(self, cas, entities, offsets):
        # event_type = cas.typesystem.get_type(Event)
        # event_properties_type = cas.typesystem.get_type(EventProperties)
        text = cas.sofa_string
        eDoc = EntityDocument(doc_text=text, entities=offsets)

        #async with sem:
        negation_output = await negation_rest.process(eDoc)
        i = 0
        for e in entities:
            # -1 represents that it had happened, 1 represents that it is negated
            e.polarity = negation_output[i]
            i += 1
