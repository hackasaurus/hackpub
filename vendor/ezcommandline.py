import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

def command(func):
    func.subparser = subparsers.add_parser(func.__name__, help=func.__doc__)
    func.subparser.set_defaults(func=func)
    return func

def arg(*args, **kwargs):
    def wrap(func):
        func.subparser.add_argument(*args, **kwargs)
        return func
    return wrap

def run():
    args = parser.parse_args()
    args.func(args)
