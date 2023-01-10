import warnings
from ctakes_pbj import pbj_receiver
from ctakes_pbj.pbj_tools import pbj_pipeline
from ctakes_pbj import pbj_sender
from example_negation import ExampleNegation
from ctakes_pbj import arg_parser
args = arg_parser.get_args()

warnings.filterwarnings("ignore")


def main():

    # Create a new PBJ Pipeline, add a class that interacts with cNLPT to add Negation to Events. 
    pipeline = pbj_pipeline.Pipeline()
    pipeline.add(ExampleNegation())
    # Add a PBJ Sender to the end of the pipeline to send the processed cas back to cTAKES and initialize the pipeline.
    pipeline.add(pbj_sender.PBJSender(args.send_queue, args.host_name, args.port_name, args.password, args.username))
    pipeline.initialize()
    # Start a PBJ receiver to accept cas objects from Artemis and process them in the pipeline. 
    pbj_receiver.start_receiver(pipeline, args.receive_queue, args.host_name, args.port_name)


main()

