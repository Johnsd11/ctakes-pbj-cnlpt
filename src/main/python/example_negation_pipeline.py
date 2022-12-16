from ctakes_pbj import pbj_receiver
from ctakes_pbj.pbj_tools import pbj_pipeline
from ctakes_pbj import pbj_sender
from ctakes_pbj import pbj_util
from example_negation import ExampleNegation

import warnings
warnings.filterwarnings("ignore")


def main():

    hostname = pbj_util.DEFAULT_HOST
    port = pbj_util.DEFAULT_PORT
    queue_receive_cas = 'test/JavaToPython'
    queue_send_cas = 'test/PythonToJava'

    pipeline = pbj_pipeline.Pipeline()
    pipeline.add(ExampleNegation())
    pipeline.add(pbj_sender.PBJSender(queue_send_cas))
    pipeline.initialize()
    pbj_receiver.start_receiver(pipeline, queue_receive_cas)


main()

