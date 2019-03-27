#!/usr/bin/env python

from midiutil import MIDIFile
import math

# degrees  = [36, 38, 40, 42, 44, 46, 48, 50, 48, 46, 44, 42, 38, 36]  # MIDI note number
# track    = 0
# channel  = 0
# time     = 4    # In beats
# duration = 5    # In beats
# tempo    = 100   # In BPM
# volume   = 100  # 0-127, as per the MIDI standard

# # MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
# #                       # automatically)
# # MyMIDI.addTempo(track, time, tempo)

# for i, pitch in enumerate(degrees):
# 	# print(i,pitch)
#     MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

# with open("major-scale.mid", "wb") as output_file:
#     MyMIDI.writeFile(output_file)

class MIDIob:
	def __init__(self, SOL):
		self.SOL = SOL #sheet_object list

	def calculate_pitch(self, noteName, prevAccidental):
		lettersInOrder = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

		pitch = lettersInOrder[noteName[0]] + (36 + (int(noteName[1])-2)*12)

		if prevAccidental == 1:
			pitch += 1
		elif prevAccidental == 2:
			pitch -= 1

		return pitch


	#Converts all MIDIob information into MIDI format, returning MIDI_File object
	def convert_to_MIDI(self, track=0, channel=0, time=4, tempo=120, volume=100):
		print("SOL")
		print(self.SOL)
		MIDI_File = MIDIFile(1)

		MIDI_File.addTempo(track,time,tempo)

		currOctave = 1

		letters = ["C", "D", "E", "F", "G", "A", "B", "C", "D", "E", "F", "G", "A", "B", "C"]
		numbers = [4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6]


		prevAccidental = -1

		for ob in self.SOL:
			# if there is an accidental, say that the next note must be changed
			if ob.rest == 1:
				prevAccidental = 1
			elif ob.rest == 2:
				prevAccidental = 2

			# set the current octave to use for this one
			if ob.clef == 1:
				currOctave = 1
			elif ob.clef == 2:
				currOctave = 2
			elif ob.clef == 3:
				currOctave = 3

			if currOctave == 1:
				noteName = letters[ob.run] + str(numbers[ob.run])
				pitch = self.calculate_pitch(noteName, prevAccidental)
				prevAccidental = -1
			elif currOctave == 2:
				noteName = letters[ob.run + 1] + str(numbers[ob.run] - 2)
				pitch = self.calculate_pitch(noteName, prevAccidental)
				prevAccidental = -1
			elif currOctave == 3:
				noteName = letters[ob.run + 2] + str(numbers[ob.run] - 2)
				pitch = self.calculate_pitch(noteName, prevAccidental)
				prevAccidental = -1


			print("OB DURATION", ob.duration, track, pitch, time, volume)

			if ob.duration > 0:
				print("Adding with duration")
				MIDI_File.addNote(track, channel, pitch, time + ob.duration, ob.duration, volume)
				time = time + 1
				# time = time + ob.duration
			elif ob.rest > 0:
				print("Adding with rest")
				MIDI_File.addNote(track, channel, 2, time +1, 0.01, volume)
				time = time + 1
				# time = time + ob.rest

				
			# time += 1



		# for time_inc, pitch in enumerate(degrees):
			# MIDI_File.addNote(track, channel, pitch, time + time_inc, duration volume)
		filename = "hello.mid"
		with open(filename, "wb") as op:
			# print("WAS OPENED")
			# print(op)
			MIDI_File.writeFile(op)
		return MIDI_File


	#Writes a MIDI object to a corresponding MIDI file
	# def MIDI_to_file(self, MIDI_File, filename):
	# 	print("MIDIFILE")
	# 	print(MIDI_File)

	# 	degrees  = [36, 38, 40, 42, 44, 46, 48, 50, 48, 46, 44, 42, 38, 36]  # MIDI note number
	# 	track    = 0
	# 	channel  = 0
	# 	time     = 4    # In beats
	# 	duration = 5    # In beats
	# 	tempo    = 100   # In BPM
	# 	volume   = 100  # 0-127, as per the MIDI standard

	# 	MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
	# 	#                       # automatically)
	# 	MyMIDI.addTempo(track, time, tempo)

	# 	for i, pitch in enumerate(degrees):
	# 		# print(i,pitch)
	# 	    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

	# 	with open("major-scale.mid", "wb") as output_file:
	# 	    MyMIDI.writeFile(output_file)
		# with open(filename, "wb") as op:
		# 	print("WAS OPENED")
		# 	print(op)
		# 	MIDI_File.writeFile(op)
