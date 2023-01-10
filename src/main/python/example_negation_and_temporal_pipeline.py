import warnings
from ctakes_pbj import pbj_receiver
from ctakes_pbj.pbj_tools import pbj_pipeline
from ctakes_pbj import pbj_sender
from example_negation import ExampleNegation
from example_temporal import ExampleTemporal
from ctakes_pbj import arg_parser
args = arg_parser.get_args()

warnings.filterwarnings("ignore")

# This shows the example_negation pipeline and the example_temporal pipeline functionality merged into a single pipeline.
def main():

    # Create a PBJ Pipeline, add both the ExampleNegation and ExampleTemporal processors.
    pipeline = pbj_pipeline.Pipeline()
    pipeline.add(ExampleNegation())
    pipeline.add(ExampleTemporal())
    # Add a PBJ Sender to the end of the pipeline to send the cas back to cTAKES and initialize the pipeline.
    pipeline.add(pbj_sender.PBJSender(args.send_queue, args.host_name, args.port_name, args.password, args.username))
    pipeline.initialize()
    # start the PBJ receiver to accept cas objects from Artemis and process them in the pipeline.
    pbj_receiver.start_receiver(pipeline, args.receive_queue, args.host_name, args.port_name)


main()

