import asyncio
# from cnlpt.api.temporal_rest import *
# from cnlpt.api.temporal_rest import SentenceDocument
import cnlpt.api.temporal_rest as temporal_rest
import time
from ctakes_pbj.pbj_tools import create_type
from ctakes_pbj.pbj_tools import ctakes_types
from pprint import pprint

import cas_annotator

sem = asyncio.Semaphore(1)


# In this example EventMentions have already been created.
# When cnlpt returns an Event, this example attempts to match it
# to an existing EventMention before creating a new one.

class ExampleTemporal2(cas_annotator.CasAnnotator):

    def initialize(self):
        # startup_event()
        print("starting init " + str(time.time()))
        asyncio.run(self.init_caller())

        print("done with init " + str(time.time()))

    def process(self, cas):
        print("processing")
        sentences = cas.select(ctakes_types.Sentence)
        e_mentions = cas.select(ctakes_types.EventMention)
        e_m_begins = []
        for e in e_mentions:
            e_m_begins.append(e.begin)
        tokens = cas.select(ctakes_types.BaseToken)
        token_begins = []
        for t in tokens:
            token_begins.append(t.begin)

        print("calling temporal caller" + str(time.time()))
        asyncio.run(self.temporal_caller(cas, sentences, e_mentions, e_m_begins, tokens, token_begins))
        print("done calling temporal " + str(time.time()))

    @staticmethod
    def get_event_mention(cas, e_mentions, e_m_begins, tokens, token_begins, begin):
        i = 0
        for b in e_m_begins:
            if b == begin:
                return e_mentions[i]
            i += 1
        i = 0
        for b in token_begins:
            if b == begin:
                return create_type.create_type(cas, 'EventMention', begin, tokens[i].end)
            i += 1
        return create_type.create_type(cas, 'EventMention', begin, begin)

    async def init_caller(self):
        await temporal_rest.startup_event()

    async def temporal_caller(self, cas, sentences, e_mentions, e_m_begins, tokens, token_begins):
        event_type = cas.typesystem.get_type(ctakes_types.Event)
        event_properties_type = cas.typesystem.get_type(ctakes_types.EventProperties)
        timex_type = cas.typesystem.get_type(ctakes_types.TimeMention)
        tlink_type = cas.typesystem.get_type(ctakes_types.TemporalTextRelation)
        argument_type = cas.typesystem.get_type(ctakes_types.RelationArgument)

        # async with sem:
        for s in sentences:
            text = s.get_covered_text()
            s_begin = s.begin
            sentence_doc = temporal_rest.SentenceDocument(sentence=text)

            temporal_result = await temporal_rest.process_sentence(sentence_doc)
            rj = temporal_result.json()
            pprint(rj)

            events_times = {}
            i = 0
            for t in temporal_result.timexes:
                for tt in t:
                    timex = create_type.add_type(cas, timex_type, s_begin + tt.begin, s_begin + tt.end)
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
                    e_begin = s_begin + ee.begin
                    event_mention = self.get_event_mention(cas, e_mentions, e_m_begins, e_begin, tokens, token_begins)
                    event_mention.event = event
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
