#!/usr/bin/env python

from midiutil import MIDIFile
import math

degrees  = [36, 38, 40, 42, 44, 46, 48, 50, 48, 46, 44, 42, 38, 36]  # MIDI note number
track    = 0
channel  = 0
time     = 4    # In beats
duration = 5    # In beats
tempo    = 100   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(degrees):
	# print(i,pitch)
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

class MIDIob:
	def __init__(self, SOL, label):
		self.SOL = SOL #sheet_object list
		self.labels = labels #note labels for each object

	#Adds a single object and label to the MIDIob
	def add_ob(self, ob, label):
		self.SOL.append(ob)
		self.labels.append(label)

	#Converts all MIDIob information into MIDI format, returning MIDI_File object
	def covnert_to_MIDI(self, track=0, channel=0, time=1, tempo=100, volume=100):
		MIDI_File = MIDIFile(1)

		MIDI_File.addTempo(track,time,tempo)

		degrees = self.calculate_degress(SOL)

		for time_inc, pitch in enumerate(degrees):
			MIDI_File.addNote(track, channel, pitch, time + time_inc, duration volume)

		return MIDI_File

	#Writes a MIDI object to a corresponding MIDI file
	def MIDI_to_file(self, MIDI_File, filename):
		with open(filename, "wb") as op:
			MIDI_File.writeFile(op)
