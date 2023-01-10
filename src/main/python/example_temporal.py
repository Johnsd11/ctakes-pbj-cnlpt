import asyncio
import cnlpt.api.temporal_rest as temporal_rest
import time
from ctakes_pbj.pbj_tools import create_type
from ctakes_pbj.pbj_tools import ctakes_types
from pprint import pprint
from ctakes_pbj.cas_handlers import cas_annotator
from ctakes_pbj.pbj_tools.token_tools import *
from ctakes_pbj.pbj_tools.get_common_types import get_event_mention
from ctakes_pbj.pbj_tools.create_relation import create_relation

sem = asyncio.Semaphore(1)


class ExampleTemporalAnnotator(cas_annotator.CasAnnotator):

    # Initializes the cNLPT, which loads its Temporal model.
    def initialize(self):
        # startup_event()
        print("starting init " + str(time.time()))
        asyncio.run(self.init_caller())

        print("done with init " + str(time.time()))

    # Process Sentences, adding Times, Events and TLinks found by cNLPT. 
    def process(self, cas):
        print("processing")
        doc_id = cas.select(ctakes_types.DocumentID)
        print(doc_id)
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
        asyncio.run(self.temporal_caller(cas, sentences, e_mentions, e_m_begins, tokens))
        print("done calling temporal " + str(time.time()))

    async def init_caller(self):
        await temporal_rest.startup_event()

    async def temporal_caller(self, cas, sentences, e_mentions, e_m_begins, tokens):
        event_type = cas.typesystem.get_type(ctakes_types.Event)
        event_properties_type = cas.typesystem.get_type(ctakes_types.EventProperties)
        timex_type = cas.typesystem.get_type(ctakes_types.TimeMention)
        tlink_type = cas.typesystem.get_type(ctakes_types.TemporalTextRelation)
        argument_type = cas.typesystem.get_type(ctakes_types.RelationArgument)

        # async with sem:
        for s in sentences:
            text = s.get_covered_text()

            first_sentence_token_index = get_token_index_by_offset(tokens, s.begin)
            if first_sentence_token_index == -1:
                print("index is -1", text)
                continue

            print(text)
            sentence_doc = temporal_rest.SentenceDocument(sentence=text)

            temporal_result = await temporal_rest.process_sentence(sentence_doc)
            rj = temporal_result.json()
            pprint(rj)

            events_times = {}
            i = 0
            for t in temporal_result.timexes:
                for tt in t:

                    begin_token = tokens[first_sentence_token_index + tt.begin]
                    end_token = tokens[first_sentence_token_index + tt.end]
                    timex = create_type.add_type(cas, timex_type, begin_token.begin, end_token.end)
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
                    begin_token = tokens[first_sentence_token_index + ee.begin]
                    end_token = tokens[first_sentence_token_index + ee.end]
                    event_mention = get_event_mention(cas, e_mentions, e_m_begins, begin_token.begin, end_token.end)
                    event_mention.event = event
                    events_times['EVENT-' + str(i)] = event_mention
                    i += 1

            for r in temporal_result.relations:
                for rr in r:

                    arg1 = argument_type()
                    arg1.argument = events_times[rr.arg1]
                    print("Arg1 =", events_times[rr.arg1])
                    arg2 = argument_type()
                    arg2.argument = events_times[rr.arg2]
                    print("Arg2 =", events_times[rr.arg2])
                    tlink = create_relation(tlink_type, rr.category, arg1, arg2)
                    cas.add(tlink)

                    print(rr.arg1, rr.arg2, rr.arg1_start, rr.arg2_start)





