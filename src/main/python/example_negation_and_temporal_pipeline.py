import warnings
from ctakes_pbj import pbj_receiver
from ctakes_pbj.pbj_tools import pbj_pipeline
from ctakes_pbj import pbj_sender
from example_negation import ExampleNegation
from example_temporal import ExampleTemporal
from ctakes_pbj import arg_parser
args = arg_parser.get_args()

warnings.filterwarnings("ignore")


def main():

    pipeline = pbj_pipeline.Pipeline()
    pipeline.add(ExampleNegation())
    pipeline.add(ExampleTemporal())
    pipeline.add(pbj_sender.PBJSender(args.send_queue, args.host_name, args.port_name, args.password, args.username))
    pipeline.initialize()
    pbj_receiver.start_receiver(pipeline, args.receive_queue, args.host_name, args.port_name)


main()

