import warnings
from ctakes_pbj import pbj_receiver
from ctakes_pbj.pbj_tools import pbj_pipeline
from ctakes_pbj import pbj_sender
from example_temporal import ExampleTemporal
from ctakes_pbj import arg_parser
args = arg_parser.get_args()

warnings.filterwarnings("ignore")


def main():

    # Create a new PBJ Pipeline, add a class that interacts with cNLPT to add Temporal information.
    pipeline = pbj_pipeline.Pipeline()
    pipeline.add(ExampleTemporal())
    # Add a PBJ Sender to the end of the pipeline to send the cas back to cTAKES and initialize the pipeline.
    pipeline.add(pbj_sender.PBJSender(args.send_queue, args.host_name, args.port_name, args.password, args.username))
    pipeline.initialize()
    # Start the PBJ Receiver, listening to the Artemis broker and processing all received cas objects. 
    pbj_receiver.start_receiver(pipeline, args.receive_queue, args.host_name, args.port_name)


main()

