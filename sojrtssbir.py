#you can change these↓

times=15
p=11
notenum = [[60,64,67],[60,65,69],[62,65,71],[64,67,72]]
b=3

##  times           how many times? (You shouldn't set too much.)
##      The processing time increases about 4 times for every 1 increase.
##  p               set ppqn to 2^(c+3)
##  notenum         you can set the chord (0~127)
##  b               set the first bpm to 234375/(b*16384)

#you can change these↑

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import math

a,d,m=0,0,0
for i in notenum: a += len(i)
mid=mido.MidiFile()
mid.ticks_per_beat=2**(p+3)
for i in range(times+1):mid.add_track()
print("making:")
print("  notes:")
for i in range(times):
    print("    step: "+str(i+1), end="\n      ")
    for j in range(len(notenum)):
        for k in range(3**i):
            for l in range(len(notenum[j])):mid.tracks[i+1].append(Message("note_on" ,channel=i%15+(i%15>=9),note=notenum[j][l],velocity=127,time=0 if j+k+l else d))
            for l in range(len(notenum[j])):mid.tracks[i+1].append(Message("note_off",channel=i%15+(i%15>=9),note=notenum[j][l],             time=0 if l else math.ceil(2**(p-i))))
        print(str(j+1), end="")
    mid.tracks[i+1].append(MetaMessage("end_of_track"))
    print("\n    finished(step: "+str(i+1)+", notes: "+str(a*3**i)+")")
    d+=len(notenum)*(2**(p-i if i<p else 0)*3**i)
print("\n  conductor(track:0):")
for i in range(times):
    print("    step: "+str(i+1), end="\n      ")
    for j in range(len(notenum)):
        for k in [bin(i).count("1") for i in range(2**i)]:
            mid.tracks[0].append(MetaMessage("set_tempo",tempo=b*2**(22-k-(i-p if i>p else 0)),time=i+j+k and 2**(p+m)))
            #print(mid.tracks[0][-1])
            m=k-(i if i<p else p)
        print(str(j+1), end="")
    print("\n    finished(step: "+str(i+1)+", bpmevents: "+str(len(notenum)*2**i)+")")
mid.tracks[0].append(MetaMessage("end_of_track"))
print("\nfinished(totalnotes: "+str(a*(3**times-1)//2)+", totalbpmevents: "+str(len(notenum)*(2**times-1))+")")
print("writing")
mid.save("Song Of Just Repeating The Same Sounds But It's Recursive.mid")
