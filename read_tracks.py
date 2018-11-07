import numpy as np
import sys
import uproot as ur

input_file = sys.argv[1]
data = ur.open(input_file)

#####################################################
track_evtnr = data['Tracks'].arrays(['eventNumber'], outputtype=tuple)[0]
track_trigID = data['Tracks'].arrays(['triggerID'], outputtype=tuple)[0]
track_planeID = data['Tracks'].arrays(['planeID'], outputtype=tuple)[0]
track_x, track_y = data['Tracks'].arrays(['xPos', 'yPos'], outputtype=tuple)
track_chi2 = data['Tracks'].arrays(['chi2'], outputtype=tuple)[0]

# eventNumber array has gaps
# total track number is length of tracks/events plus multiplicity
# Why are events missing --> no tracks found, or no hits on all telescope planes
print "event number", len(track_evtnr), track_evtnr
print "trigger ID  ", len(track_trigID), track_trigID
print "plane ID    ", len(track_planeID), track_planeID
print "track x     ", len(track_x), track_x
print "chi2        ", len(track_chi2), track_chi2

#####################################################
print "\n"
tracks_in_evts = 7
print "events contain multiple tracks:", tracks_in_evts
max_multi = 12
tracks = np.zeros(max_multi)
plane_length = 7 # here 6xMimosa plus 1xFEI4
for index, value in enumerate(track_planeID):
    #print index, value, track_x[index]
    length = len(value)/plane_length
    if length == tracks_in_evts:
        print "\n", index, ": event number", track_evtnr[index], ": trigger ID", track_trigID[index]
        for i in range(tracks_in_evts):
            print np.around(track_x[index].reshape(-1, plane_length)[i], decimals=4), round(track_chi2[index].reshape(-1, plane_length)[i][0], 2)
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
print "total tracks (check):", len(np.hstack(track_planeID))/plane_length

# stack it and reshape to always 7 arrays
trackX = np.hstack(track_x).reshape(-1, plane_length)
trackY = np.hstack(track_y).reshape(-1, plane_length)
#print len(trackX.T[0])
print "total tracks (stacked shape):", trackX.shape, "size:", trackX.size, "length:", len(trackX)

#####################################################
#print "\n"
#print "beam profile, alignment check & testing"

#diffX = trackX.T[-1]-trackX.T[0]
#diffY = trackY.T[-1]-trackY.T[0]
#print np.mean(diffX), np.std(diffX)
#print np.mean(diffY), np.std(diffY)


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

#print "numpy-style: compare track with next track, if different it is Zero:"
#for i in range(1, 100):
#    compare_next = trackX[:-i] - trackX[i:]
#    print len(np.where(compare_next == np.zeros(plane_length))[0])/plane_length

###############################
# TODO: add DUTHitNumber 
print "\n"

hits_ID = data['Hits'].arrays(['ID'], outputtype=tuple)[0]
hits_x, hits_y, hits_z = data['Hits'].arrays(['xPos', 'yPos', 'zPos'], outputtype=tuple)
#print hits_x.shape, len(hits_x)

print "first track in example"
test = 4
print "event number", track_evtnr[test]
print "trigger ID  ", track_trigID[test]
print "plane ID    ", track_planeID[test]
print "track x     ", track_x[test]
print "chi2        ", track_chi2[test]          # only one value
print "hits ID     ", hits_ID[track_evtnr[test]-1]
print "hits x      ", hits_x[track_evtnr[test]-1]

print hits_ID[track_evtnr-1], len(hits_ID[track_evtnr-1])
print hits_ID[~(track_evtnr-1)], len(hits_ID[~track_evtnr-1])

#print len(np.where(track_chi2 < 
final_array_length = len(np.hstack(track_planeID))/plane_length
chi_cut = 20
chi2_okay = np.array([])

# single track id

index = 0
single_track_ID = np.zeros(final_array_length, dtype=int)
i = 0
while i < final_array_length:
    #print "index i", i, index
    #print track_planeID[index] 
    multiplicity = len(track_planeID[index])/plane_length
    #print multiplicity
    for n in range(multiplicity):
        #print track_evtnr[index]
        single_track_ID[i+n] = track_evtnr[index]
    i += multiplicity
    index += 1
print single_track_ID

trackXs =  np.hstack(track_x).reshape(-1, plane_length)
trackYs =  np.hstack(track_y).reshape(-1, plane_length)
planeIDs = np.hstack(track_planeID).reshape(-1, plane_length)
chi2 = np.hstack(track_planeID).reshape(-1, plane_length)

for index, evtnr in enumerate(single_track_ID):
    


exit()



for index, evtnr in enumerate(track_evtnr[0:10]):
    print evtnr, len(track_trigID[index])/plane_length
    for multiplicity in range(1,len(track_trigID)/plane_length):
        multiplicity = 1
    if len(track_trigID)/plane_length > multiplicity:
        #track_trigID
        print evtnr, index





exit()

#print len(trackX.T[0])
print "total tracks (stacked shape):", trackX.shape, "size:", trackX.size, "length:", len(trackX)

