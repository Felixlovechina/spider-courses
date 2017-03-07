import argparse
import protocol_constants as pc

parser = argparse.ArgumentParser(prog='CrawlerClient', description='Start a crawler client')
parser.add_argument('-S', '--host-all', type=str, nargs=1, help='Host server for all services')
parser.add_argument('-s', '--host', type=str, nargs=1, help='Crawler host server address, default is localhost')
parser.add_argument('-p', '--host-port', type=int, nargs=1, help='Crawler host server port number, default is 10000')
parser.add_argument('-m', '--mongo', type=str, nargs=1, help='Mongo Server address, default is localhost')
parser.add_argument('-n', '--mongo-port', type=int, nargs=1, help='Mongo port number, default is 27017')
parser.add_argument('-r', '--redis', type=str, nargs=1, help='Redis server address, default is localhost')
parser.add_argument('-x', '--redis-port', type=int, nargs=1, help='Redis port number, default is 6379')

class arguments:
    pass

args = arguments()

parser.parse_args(namespace=args)

if args.host_all is not None:
    args.host = args.mongo = args.redis = args.host_all

if args.host is None:
    args.host = 'localhost'

if args.mongo is None:
    args.mongo = 'localhost'

if args.redis is None:
    args.redis = 'localhost'

if args.host_port is None:
    args.host_port = 9999

if args.mongo_port is None:
    args.mongo_port = 27017

if args.redis_port is None:
    args.redis_port = 6379 