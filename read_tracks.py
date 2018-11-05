import numpy as np
import sys
import uproot as ur # https://hub.mybinder.org/user/scikit-hep-uproot-o2d8jf8i/notebooks/binder/tutorial.ipynb
#from root_pandas import read_root # https://github.com/scikit-hep/root_pandas

input_file = sys.argv[1]
data = ur.open(input_file)

# TODO: add trigger ID
# TODO: add DUTHitNumber 

#####################################################
track_evtnr = data['Tracks'].arrays(['eventNumber'], outputtype=tuple)[0]
track_trigID = data['Tracks'].arrays(['triggerID'], outputtype=tuple)[0]
track_ID = data['Tracks'].arrays(['ID'], outputtype=tuple)[0]
track_x, track_y = data['Tracks'].arrays(['xPos', 'yPos'], outputtype=tuple)
track_chi2 = data['Tracks'].arrays(['chi2'], outputtype=tuple)[0]

# eventNumber array has gaps
# total track number is length of tracks/events plus multiplicity
# TODO: Why are events missing
print "event number", len(track_evtnr), track_evtnr
print "trigger ID  ", len(track_trigID), track_trigID
print "track ID    ", len(track_ID), track_ID
print "track x     ", len(track_x), track_x
print "chi2        ", len(track_chi2), track_chi2

#####################################################
print "\n"
tracks_in_evts = 7
print "events contain multiple tracks:", tracks_in_evts
max_multi = 12
tracks = np.zeros(max_multi)
plane_length = 7 # here 6xMimosa plus 1xFEI4
for index, value in enumerate(track_ID):
    #print index, value, track_x[index]
    length = len(value)/plane_length
    if length == tracks_in_evts:
        print index, ": event number", track_evtnr[index], ": trigger ID", track_trigID[index][0] # just first entry, since duplicated
        for i in range(tracks_in_evts):
            print np.around(track_x[index].reshape(-1, plane_length)[i], decimals=2), round(track_chi2[index].reshape(-1, plane_length)[i][0], 2)
    for i in range(max_multi):
        if length == i:
            tracks[i] += 1

print "\n"
print "multiplicity"
print tracks.astype(int)
print "events with tracks", np.sum(tracks)
# total tracks 
total_tracks = np.sum(tracks * np.arange(max_multi))
print "total tracks", total_tracks

# discriminate possible duplicated tracks
# stack it
print "total tracks (check):", len(np.hstack(track_ID))/plane_length

# stack it and reshape to always 7 arrays
trackX = np.hstack(track_x).reshape(-1, plane_length)
trackY = np.hstack(track_y).reshape(-1, plane_length)
#print len(trackX.T[0])
print "total tracks (stacked shape):", trackX.shape, trackX.size, len(trackX)

#####################################################
print "\n"
print "TO TEST: find duplicated tracks"
counts = np.zeros(max_multi)
for index in range(len(trackX)):
#for index in range(10):
    #print trackX[index]
    length = len(np.where(trackX[index:index+10] == trackX[index])[0]) / plane_length
    #if length == 10:
    #    print index#, ": event number"
    #    print trackX[index]
    # this takes too long
    #length = len(np.where(trackX == trackX[index])[0])
    for i in range(max_multi):
        if length == i:
            counts[i] += 1

print "result [0, 1, 2, ..] x track:"
print counts.astype(int), np.sum(counts)
#print np.sum(counts.astype(int) * np.arange(max_multi))

print "check how many track positions are the same:"
for i in range(plane_length):
    print "plane ID:", i, ":", total_tracks - len(np.unique(trackX.T[i]))


print "numpy-style: compare track with next track, if different it is Zero:"
#for i in range(1, 100):
#    compare_next = trackX[:-i] - trackX[i:]
#    print len(np.where(compare_next == np.zeros(plane_length))[0])/plane_length
