import uproot as ur
import numpy as np
import sys

def inspect_file(data):
    for index, value in enumerate(data.keys()):
        key_name = value[:-2]
        print "\n\n", index, value, len(data[key_name].keys())
        print data[key_name].keys()
        for index2, value2 in enumerate(data[key_name].keys()):
            key_name2 = value2
            print "\n  ", index2, value2, data[key_name].arrays([key_name2], outputtype=tuple)[0].size
            if True:
                #print "  ", data[key_name].arrays([key_name2], outputtype=tuple)
                # just the first element
                print "  ", data[key_name].arrays([key_name2], outputtype=tuple)[0][:7]
                print "  ", data[key_name].arrays([key_name2], outputtype=tuple)[0][-6:]

input_file = sys.argv[1]
data = ur.open(input_file)
inspect_file(data)
