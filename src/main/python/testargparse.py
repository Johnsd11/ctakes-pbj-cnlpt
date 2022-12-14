import argparse


parser = argparse.ArgumentParser(
    prog='ProgramName',
    description='What the program does',
    epilog='Text at the bottom of help'
)
DEFAULT_COUNT = 5

parser.add_argument('filename')           # positional argument
parser.add_argument('-bla', '--count', default=DEFAULT_COUNT)      # option that takes a value
parser.add_argument('-ble', '--verbose',
                    action='store_true')  # on/off flag

args = parser.parse_args()


class Hee:

    def __init__(self, queue_name=args.filename, blah=args.count, blee=args.verbose):
        print(queue_name, blah, blee)


Hee()

