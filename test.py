import numpy as np
import sys
input_file = sys.argv[1]

########################################3
# PyROOT
from ROOT import TFile #, TF1, TCanvas, TH1
data = TFile(input_file)

tracks_tree = data.Get('Tracks') 
hits_tree = data.Get('Hits') 

n = 0
for evt in hits_tree:
    print evt.ID
    print evt.xPos
    print evt.xPos.size()
    n += 1
    if n > 10:
        break
    pass

#print tracks_tree, hits_tree
#print tracks_tree.GetListOfLeaves().At(0), hits_tree.GetListOfLeaves().At(0).GetName()
#print hits_tree.GetEntries()
########################################3
# uproot
import uproot as ur # https://hub.mybinder.org/user/scikit-hep-uproot-o2d8jf8i/notebooks/binder/tutorial.ipynb
#from root_pandas import read_root # https://github.com/scikit-hep/root_pandas
data = ur.open(input_file)

# TODO: add DUTHitNumber 

# individual access
#print data.keys()
#print data["Tracks"].keys()
#print data['Hits'].keys()
#print data['ZeroSuppressed'].keys()
#print len(data["Tracks"].keys())

track_evtnr = data['Tracks'].arrays(['eventNumber'], outputtype=tuple)[0]
track_ID = data['Tracks'].arrays(['planeID'], outputtype=tuple)[0]
track_x, track_y = data['Tracks'].arrays(['xPos', 'yPos'], outputtype=tuple)
print track_x.shape, len(track_x)
print track_x, len(track_x)

# stack it
#print len(np.hstack(track_evtnr))
#print len(np.hstack(track_ID))
#print len(np.hstack(track_x))/7
#print len(np.hstack(track_y))/7

hits_ID = data['Hits'].arrays(['ID'], outputtype=tuple)[0]
hits_x, hits_y, hits_z = data['Hits'].arrays(['xPos', 'yPos', 'zPos'], outputtype=tuple)
print hits_x.shape, len(hits_x)
print hits_x[0:10], len(hits_x)




exit()



#zs_ID = data['ZeroSuppressed'].arrays(['ID'], outputtype=tuple)
#print zs_ID
#zs_time = data['ZeroSuppressed'].arrays(['Time'], outputtype=tuple)
#print zs_time

# eventNumber array has gaps
# total track number is length of tracks/events plus multiplicity
# TODO: Why are events missing
print "event number", len(track_evtnr), track_evtnr
print "track ID", len(track_ID), track_ID
print "track x", len(track_x), track_x

# not all hits contain hits for each plane 
# TODO: add event number from Hits
#print hits_ID[0:6]

# events contain multiple tracks
max_multi = 12
tracks = np.zeros(max_multi)
plane_length = 7 # here 6xMimosa plus 1xFEI4
for index, value in enumerate(track_ID):
    #print index, value, track_x[index]
    length = len(value)/plane_length
    if length == 7:
        print index, track_evtnr[index], track_x[index]
    for i in range(max_multi):
        if length == i:
            tracks[i] += 1

print "multiplicity", tracks
print "entries of tracks", np.sum(tracks)
# total tracks 
print "total tracks", np.sum(tracks * np.arange(max_multi))


# discriminate possible duplicated tracks

# stack it
print "total tracks (check):", len(np.hstack(track_ID))/plane_length
#print len(np.hstack(track_x))/7
#print len(np.hstack(track_y))/7

# stack it and reshape to always 7 arrays
trackX = np.hstack(track_x).reshape(-1, plane_length)
trackY = np.hstack(track_y).reshape(-1, plane_length)

print trackX.shape
print trackX.size
print len(trackX)
# exemplary two tracks in one event and splitted
#print track_x[6:7]
#print trackX[6:8]

counts = np.zeros(max_multi)
#for index in range(len(trackX)):
for index in range(5):
    print trackX[index]#, np.where(trackX[index:index+10] == trackX[index])[0]
    #print np.where(trackX == trackX[index])[0]
    length = len(np.where(trackX[index:index+10] == trackX[index])[0])
    #length = len(np.where(trackX == trackX[index])[0])
    #print length
    for i in range(max_multi):
        if length == i * plane_length:
            counts[i] += 1
print np.array(counts, dtype=int)
print np.sum(counts)

# compare track with next track, if different not 0
#for i in range(1, 5):
#    compare_next = trackX[:-i] - trackX[i:]
#    print len(np.where(compare_next == np.zeros(plane_length))[0])/plane_length

#print trackX.T[0]
#print len(trackX.T[0])
for i in range(7):
    print len(np.unique(trackX.T[i]))

# tracks = total tracks - 

exit()


#print data['Tracks'].arrays(data["Tracks"].keys())
#print data['Tracks'].arrays(['eventNumber'])['eventNumber']
#print data['Tracks'].array('eventNumber')

print data.allkeys()
print data.items()

print data["Tracks"].allkeys()
print data["Hits"].allkeys()
print data["Hits"]["xPos"]

print data["Tracks"].show()
print data["Hits"].show()

print data["Tracks"].arrays(["xPos"])
print data["Hits"].arrays(["xPos"])
print data["Hits"]["xPos"].array()

print data["Hits"]["xPos"].numitems()

print data["Hits"]["xPos"].compressedbytes()
print data["Hits"]["xPos"].uncompressedbytes()
print data["Hits"]["xPos"].compressionratio()

print data["Hits"]["xPos"].basket_entrystart(0)
print data["Hits"]["xPos"].basket_entrystop(0)
print data["Hits"]["xPos"].basket_numitems(0)
print data["Hits"]["xPos"].basket_numentries(0)

print data["Hits"]["xPos"].array()
print data["Hits"]["xPos"].array(blocking=False)
