#!/usr/bin/env python

from midiutil import MIDIFile
import math

degrees  = [36, 38, 40, 42, 44, 46, 48, 50, 48, 46, 44, 42, 38, 36, 34, 42, 32, 32, 44, 48, 50, 36, 36, 12]  # MIDI note number
track    = 0
channel  = 0
time     = 4    # In beats
duration = 5    # In beats
tempo    = 100   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(2, adjust_origin=False)  # One track, defaults to format 1 (tempo track is created
                      # automatically)

MyMIDI.addTempo(track, time, tempo)
MyMIDI.addProgramChange(0,0,0,123)
MyMIDI.addProgramChange(0,1,0,41)



for i, pitch in enumerate(degrees):
	# print(i,pitch)
    MyMIDI.addNote(i % 2, channel, pitch, time + i, 1, volume)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

class MIDIob:
	def __init__(self, SOL):
		self.SOL = SOL #sheet_object list

	def calculate_pitch(self, noteName, prevAccidental):
		lettersInOrder = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

		pitch = lettersInOrder[noteName[0]] + 36 + int(noteName[1]-2)*12

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
				noteName = letters[ob.run + 1] + str(numbers[ob.run] - 1)
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
				MIDI_File.addNote(track, channel, 2, time + ob.rest, ob.rest, volume)
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


class MIDImaker:
	def __init__(self):
		self.SOLset = [] #List of all sheet objects, post-labeling, from the provided sheet music
		self.FOL = -1 #FOL (final object list), for easy conversion to midifile

		self.tracks = 0 #Number of tracks in given MIDI file, 1 indexed
		self.channel = 0 #Number of channels in a given MIDI file, 0 indexed
		self.start_time = 0 #Starting time of first note placed
		self.tempo = 100 #BPM of MIDI file
		self.volume = 100 #Volume of MIDI file

	def add_track(SOL):
		self.SOLset.append(SOL)
		tracks += 1

	#Return MIDI note ID
	def note_id(row, currOctave):

		#Letter and Note combo that make up note ID
		L = ["C", "D", "E", "F", "G", "A", "B", "C", "D", "E", "F", "G", "A", "B", "C"]
		N = [4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6]

		return (L[row + currOctave - 1],N[row] - currOctave + 1)

	#calculates the MIDI note pitch
	def note_pitch(self, id, prevAccid):
		letter_index = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

		pitch = letter_index[id[0]] + id[1]*12 #NO IDEA WHY THIS WAS 36 + (id[1]-2)*12

		#update pitch based on sharp or flat
		if prevAccid == 1: #sharp
			pitch += 1
		elif prevAccid == 2: #flat
			pitch -= 1

		return pitch

	#verify track count
	def verify_track(tracks):
		#if the number of tracks does not equal the number of seperate sheet objects
		if tracks != len(self.SOLset):
			return False
		return True

	#Adjusts instruments list to match with tracks if necessary
	def set_instruments(instr, tracks):
		#if there are more instrument then tracks, notify
		if len(instr) > tracks:
			print("Too many instruments for number of tracks")
			return False
		#makeup for difference in instruments and tracks
		elif len(instr) < tracks:
			filler = instr[len(instr)-1]
			for i in range(tracks-len(instr)):
				instr.append(filler)

	#Adjusts start times of tracks to match with number of tracks if necessary
	def set_start_times(times, tracks):
		#if there are more start times then tracks, notify
		if len(times) > tracks:
			print("Too many start times for number of tracks")
			return False
		#makeup for difference in start times and tracks
		elif len(times) < tracks:
			filler = times[len(times)-1]
			for i in range(tracks-len(times)):
				times.append(filler)

	#Adjust track tempos to match with number of tracks if necessary
	def set_tempos(tempos, tracks):
		#if there are more tempos then tracks, notify
		if len(tempos) > tracks:
			print("Too many tempos for number of tracks")
			return False
		#makeup for difference in tempos and tracks
		elif len(tempos) < tracks:
			filler = tempos[len(tempos)-1]
			for i in range(tracks-len(tempos)):
				tempos.append(filler)

	#Convertes the provided list of data into a MIDI File
	def convert_to_MIDI(self, instruments = [123], start_times = [4], tempos=[120],
	 tracks=1, channel=0, volume=100):

		if not verify_track(tracks):
			print("Track count does not match with number of music sheets")
			return

		#Adjusts instrument, start_times, and tempos to match with number of specified tracks
		set_instruments(instruments, tracks)
		set_start_times(start_times, tracks)
		set_tempos(tempos, tracks)

		MIDI_File = MIDIFile(2)

		#for every track of the Midi File
		for t in range(tracks):

			MIDI_File.addTempo(tracks[t],start_times[t],tempos[t]) #Adds tempo t
			MyMIDI.addProgramChange(t,0,0,instruments[t]) #sets instrument for tempo t

			prevAccidental = -1 #if the previous sheet object was a sharp or flat
			time = start_times[t] #Current time placement of a not in the given track

			#For every object in a single sheet object list
			for ob in self.SOLset[t]:

				#If object is an accidental, set variable and finish current iteration
				if ob.accidental != -1:
					prevAccidental = ob.accidental
					continue

				#Calculate note id and pitch
				note_id = note_id(ob.run, ob.clef)
				pitch = note_pitch(note_id, prevAccidental)

				#Reset accidental to base value
				prevAccidental = -1

				if ob.duration > 0: #If the object has a note duration, add it as a note
					MIDI_File.addNote(t, channel, pitch, time + ob.duration, ob.duration, volume)
				elif ob.rest > 0: #If the object has a rest duration, add it as a rest
					MIDI_File.addNote(t, channel, 0, time + ob.rest, ob.rest, volume)
				
				#increment time for next note
				time = time + 1

		return MIDI_File










