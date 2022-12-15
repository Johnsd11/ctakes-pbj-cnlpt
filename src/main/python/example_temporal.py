import asyncio
# from cnlpt.api.temporal_rest import *
# from cnlpt.api.temporal_rest import SentenceDocument
import cnlpt.api.temporal_rest as temporal_rest
import time
from ctakes_pbj.pbj_tools import ctakes_types
from pprint import pprint

import cas_annotator

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
        event_properties_type = cas.typesystem.get_type(ctakes_types.EventProperties)
        event_men_type = cas.typesystem.get_type(ctakes_types.EventMention)
        timex_type = cas.typesystem.get_type(ctakes_types.TimeMention)
        tlink_type = cas.typesystem.get_type(ctakes_types.TemporalTextRelation)
        argument_type = cas.typesystem.get_type(ctakes_types.RelationArgument)

        # async with sem:
        for s in sentences:
            text = s.get_covered_text()
            sentence_begin = s.begin
            sentence_doc = temporal_rest.SentenceDocument(sentence=text)

            temporal_result = await temporal_rest.process_sentence(sentence_doc)
            rj = temporal_result.json()
            pprint(rj)

            events_times = {}
            i = 0
            for t in temporal_result.timexes:
                for tt in t:
                    # Will this work?
                    # begin = sentence_begin + tt.begin
                    # end = sentence_begin + tt.end
                    # timex = add_type(cas, timex_type, begin, end)
                    timex = timex_type()
                    timex.begin = sentence_begin + tt.begin
                    timex.end = sentence_begin + tt.end
                    cas.add(timex)
                    # end Will this work?
                    # timex_list.append(timex)
                    events_times['TIMEX-' + str(i)] = timex
                    i += 1

            i = 0
            for e in temporal_result.events:
                for ee in e:
                    e_props = event_properties_type()
                    e_props.set("docTimeRel", ee.dtr)
                    event = event_type()
                    event.properties = e_props
                    cas.add(event)
                    # Will this work? 1
                    # begin = sentence_begin + ee.begin
                    # end = sentence_begin + ee.end
                    # event_mention = add_type(cas, event_men_type, begin, end)
                    event_mention = event_men_type()
                    event_mention.begin = sentence_begin + ee.begin
                    event_mention.end = sentence_begin + ee.end
                    # end Will this work? 1
                    event_mention.event = event
                    # wtw? 2
                    cas.add(event_mention)
                    # end wtw? 2
                    events_times['EVENT-' + str(i)] = event_mention
                    i += 1

            for r in temporal_result.relations:
                for rr in r:
                    arg1 = argument_type()
                    arg1.argument = events_times[rr.arg1]
                    arg2 = argument_type()
                    arg2.argument = events_times[rr.arg2]
                    tlink = tlink_type()
                    tlink.category = rr.category
                    tlink.arg1 = arg1
                    tlink.arg2 = arg2
                    cas.add(tlink)

                    print(rr.arg1, rr.arg2, rr.arg1_start, rr.arg2_start)
