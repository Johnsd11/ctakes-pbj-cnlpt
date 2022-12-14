# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

# These are the lines that ignore the typesystem errors

# import sys
# sys.path.append(r'C:\Users\ch229935\Desktop\cTakes2\ctakes-pbj\src\main\python')
# sys.path.append(r'C:\Users\ch229935\Desktop\cTakes2\ctakes-pbj\src\main\python\ctakes_pbj')
#
# from ctakes_pbj import pbj_receiver
# from pbj_tools import pbj_pipeline
# from ctakes_pbj import pbj_sender
# from ctakes_pbj import pbj_util
# from example_negation import ExampleNegation

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

