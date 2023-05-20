import argparse
import time

import shortestpath

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--shortdist", action="store_true")
    parser.add_argument("source", type=str, help="Article title 1")
    parser.add_argument("dest", type=str, help="Article title 2")

    args = parser.parse_args()

    if args.shortdist:
        source = args.source[0].upper() + args.source[1:]
        dest = args.dest[0].upper() + args.dest[1:]
        sp = shortestpath.ShortestPath()
        sp.prepare(source, dest)

        start_time = time.time()
        clicks = sp.compute()
        end_time = time.time()
        print("SHORTEST AMOUNT OF CLICK IS: " + str(clicks) + " (done in " + str(int(end_time - start_time)) + " seconds)")

    else:
        print("Nothing to do")
