#!/usr/bin/env python

from midiutil import MIDIFile
import math
import json
import partition

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


class MIDImaker:
	def __init__(self):
		self.SOLset = [] #List of all sheet objects, post-labeling, from the provided sheet music
		self.MIDI = None #The MIDI file

		self.tracks = 0 #Number of tracks in given MIDI file, 1 indexed
		self.channel = 0 #Number of channels in a given MIDI file, 0 indexed
		self.start_time = 0 #Starting time of first note placed
		self.tempo = 100 #BPM of MIDI file
		self.volume = 100 #Volume of MIDI file

	def add_track(SOL):
		self.SOLset.append(SOL)
		tracks += 1

	#Return MIDI note ID
	def note_id(self, row, currOctave):

		#Letter and Note combo that make up note ID
		#L = ["C", "D", "E", "F", "G", "A", "B", "C", "D", "E", "F", "G", "A", "B", "C"]
		#N = [4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6]
		L = ["C", "B", "A", "G", "F", "E", "D", "C", "B", "A", "G", "F", "E", "D", "C"]
		N = [6, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4]

		#print(row, currOctave, (L[row + currOctave - 1],N[row] - currOctave + 1))
		return (L[row + currOctave - 1],N[row] - currOctave + 1)

	#calculates the MIDI note pitch
	def note_pitch(self, id, prevAccid):
		letter_index = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

		pitch = letter_index[id[0]] + 12 + id[1]*12

		#update pitch based on sharp or flat
		if prevAccid == 1: #sharp
			pitch += 1
		elif prevAccid == 2: #flat
			pitch -= 1

		return pitch

	#verify track count
	def verify_track(self, tracks):
		#if the number of tracks does not equal the number of seperate sheet objects
		if tracks != len(self.SOLset):
			raise Exception("Track count ({}) does not match with number of music sheets ({})".format(tracks, len(self.SOLset)))
			return False

		return True

	#Adjusts instruments list to match with tracks if necessary
	def set_instruments(self, instr, tracks):
		#Converts instrument to corresponding MIDI number
		instrument_dict = {"Piano":1, "Harp":47, "Violin":41, "Flute":74, "Trombone":58, "Cello":43, "Bass":44, "Guitar":25, "Tuba":59, "Viola":42}
		instr_conv = []
		#if there are more instrument then tracks, notify
		if len(instr) > tracks:
			raise Exception("Track count ({}) does not match with number of instruments ({})".format(tracks, len(instr)))
			return False
		#if correct number of instruments, convert to instrument numbers
		elif len(instr) == tracks:
			#Add all instruments from instr to instr_conv
			for i in instr:
				instr_conv.append(instrument_dict[i])
		#makeup for difference in instruments and tracks
		elif len(instr) < tracks:
			#filler instrument to be apended to end of instr_conv
			filler = instrument_dict[instr[len(instr)-1]]

			#Add all instruments from instr to instr_conv
			for i in instr:
				instr_conv.append(instrument_dict[i])

			#Fill in remaining instr to match with track count
			for i in range(tracks-len(instr)):
				instr.append(filler)

		return instr_conv

	#Adjusts start times of tracks to match with number of tracks if necessary
	def set_start_times(self, times, tracks):
		#if there are more start times then tracks, notify
		if len(times) > tracks:
			raise Exception("Track count ({}) does not match with number of times ({})".format(tracks, len(times)))
			return False
		#makeup for difference in start times and tracks
		elif len(times) < tracks:
			filler = times[len(times)-1]
			for i in range(tracks-len(times)):
				times.append(filler)

	#Adjust track tempos to match with number of tracks if necessary
	def set_tempos(self, tempos, tracks):
		#if there are more tempos then tracks, notify
		if len(tempos) > tracks:
			raise Exception("Track count ({}) does not match with number of tempos ({})".format(tracks, len(tempos)))
			return False
		#makeup for difference in tempos and tracks
		elif len(tempos) < tracks:
			filler = tempos[len(tempos)-1]
			for i in range(tracks-len(tempos)):
				tempos.append(filler)

	#Convertes the provided list of data into a MIDI File
	def convert_to_MIDI(self, instruments = ["Piano"], start_times = [4], tempos=[80],
	 tracks=1, channel=0, volume=100):

		if not self.verify_track(tracks):
			return

		#Adjusts instrument, start_times, and tempos to match with number of specified tracks
		instr = self.set_instruments(instruments, tracks)
		self.set_start_times(start_times, tracks)
		self.set_tempos(tempos, tracks)

		MIDI_File = MIDIFile(2, adjust_origin=False)

		#for every track of the Midi File
		for t in range(tracks):

			MIDI_File.addTempo(t,0,tempos[t]) #Adds tempo t
			MIDI_File.addProgramChange(t,0,0,instr[t]) #sets instrument for tempo t

			prevAccidental = -1 #if the previous sheet object was a sharp or flat
			currOctave = 1
			time = start_times[t] #Current time placement of a not in the given track

			#For every object in a single sheet object list
			for ob in self.SOLset[t]:
				#print(ob.clef,ob.duration,ob.run)

				#If object is an accidental, set variable and finish current iteration
				if ob.accidental != -1:
					prevAccidental = ob.accidental
					continue

				#If the object is a clef, set currOctave and finish current iteration
				if ob.clef != -1:
					currOctave = ob.clef
					continue

				#Calculate note id and pitch
				note_id = self.note_id(ob.run, currOctave)
				pitch = self.note_pitch(note_id, prevAccidental)

				#Reset accidental to base value
				prevAccidental = -1

				if ob.duration > 0: #If the object has a note duration, add it as a note
					MIDI_File.addNote(t, t, pitch, time + ob.duration, ob.duration, volume)
					time = time + ob.duration
				elif ob.rest > 0: #If the object has a rest duration, add it as a rest
					MIDI_File.addNote(t, t, 0, time + ob.rest, ob.rest, 0)
					time = time + ob.rest


		self.MIDI = MIDI_File

	def JSON_file_to_SOL(self,filepath):
		#New sheet object list
		SOL = []

		with open(filepath) as json_file:
			music_sheet = json.load(json_file)

			for ob in music_sheet['notes']:
				new_ob = partition.sheet_object((-1,-1),-1)
				if ob['note'] == 0:#GClef
					new_ob.clef = 1
					new_ob.run = 1
					new_ob.duration = 0
				elif ob['note'] == 6:#CClef
					new_ob.clef = 2
					new_ob.run = 1
					new_ob.duration = 0
				elif ob['note'] == 7:#FClef
					new_ob.clef = 3
					new_ob.run = 1
					new_ob.duration = 0
				elif ob['note'] == 5 or ob['note'] == 1 or ob['note'] == 2 or ob['note'] == 3 or ob['note'] == 8: #Note
					new_ob.run = ob['pitch']
					new_ob.duration = ob['length']
				elif ob['note'] == 9 or ob['note'] == 10 or ob['note'] == 11 or ob['note'] == 12: #rest
					new_ob.rest = 1
					new_ob.run = ob['pitch']
					new_ob.duration = ob['length']
				elif ob['note'] == 13: #sharp
					new_ob.accidental = 1
					new_ob.run = ob['pitch']
					new_ob.duration = 0
				elif ob['note'] == 14: #flat
					new_ob.accidental = 1
					new_ob.run = ob['pitch']
					new_ob.duration = 0

				#print(ob['note'],new_ob.clef,new_ob.run,new_ob.duration,new_ob.accidental)

				SOL.append(new_ob)

		return SOL

	def JSON_string_to_SOL(self,json_string):
		#New sheet object list
		SOL = []

		music_sheet = json.load(json_string)

		for ob in music_sheet['notes']:
			new_ob = partition.sheet_object((-1,-1),-1)
			if ob['note'] == 0:#GClef
				new_ob.clef = 1
				new_ob.run = 1
				new_ob.duration = 0
			elif ob['note'] == 6:#CClef
				new_ob.clef = 2
				new_ob.run = 1
				new_ob.duration = 0
			elif ob['note'] == 7:#FClef
				new_ob.clef = 3
				new_ob.run = 1
				new_ob.duration = 0
			elif ob['note'] == 5 or ob['note'] == 1 or ob['note'] == 2 or ob['note'] == 3 or ob['note'] == 8: #Note
				new_ob.run = ob['pitch']
				new_ob.duration = ob['length']
			elif ob['note'] == 9 or ob['note'] == 10 or ob['note'] == 11 or ob['note'] == 12: #rest
				new_ob.rest = 1
				new_ob.run = ob['pitch']
				new_ob.duration = ob['length']
			elif ob['note'] == 13: #sharp
				new_ob.accidental = 1
				new_ob.run = ob['pitch']
				new_ob.duration = 0
			elif ob['note'] == 14: #flat
				new_ob.accidental = 1
				new_ob.run = ob['pitch']
				new_ob.duration = 0

			#print(ob['note'],new_ob.clef,new_ob.run,new_ob.duration,new_ob.accidental)

			SOL.append(new_ob)

		return SOL

	def jsons_to_MIDI(self, json_arr, sheet_id, instruments=["Piano"], start_times=[1]):

		for json_str in json_arr:
			self.SOLset.append(self.JSON_string_to_SOL(json_str))

		self.convert_to_MIDI(len(json_arr), instruments, start_times)

		self.MIDI_to_file("{}.mid".format(sheet_id))

	#Writes MIDI file to disk
	def MIDI_to_file(self, filepath):
		with open(filepath, "wb") as op:
			self.MIDI.writeFile(op)


def test1():
	MM = MIDImaker()

	MM.SOLset.append(MM.JSON_file_to_SOL("../../Frontend/components/jsons/MusicSheet3.json"))
	MM.SOLset.append(MM.JSON_to_SOL("../../Frontend/components/jsons/MusicSheet3.json"))

	MM.convert_to_MIDI(tracks = 2, instruments=["Flute", "Violin"], start_times=[1,0])

	MM.MIDI_to_file("first_test.mid")

# test1()









