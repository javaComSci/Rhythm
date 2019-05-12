# Rhythm
An application that allows users to convert handwritten music sheets into a digital format that can be easily tested, customized, and shared with others.

## Project Objectives:
+ Create an easy and intuitive approach to convert written sheet music into virtual sheet music via images taken from the phone camera
+ Provide an interface to modify virtual sheet music with the use of the user’s handheld device, by moving, adding, or removing notes, and and allowing the user to change the instrument that the sheet should be played with
+ Play the music on the virtual sheets using different instruments live from the user’s device
+ Allow users to create libraries of compositions, which are composed of multiple virtual music sheets

## Deliverables: 
+ React Native frontend mobile application that allows users to take and upload images of their handwritten music, modify and play virtual sheet music, and organize compositions
+ Machine learning based image classification system for converting handwritten sheet music to digital sheet music using Python and Tensorflow
+ Interface for editing compositions by moving, adding or removing notes on the virtual sheets
+ Flask backend framework that will serve network requests and manage user data about their virtual music sheets and compositions as it will allow us to integrate the front-end and database
+ MySQL database that manages user compositions and libraries
+ Use of libraries and modules such as midiutil to generate the sounds of any instrument for the music on the virtual sheets
