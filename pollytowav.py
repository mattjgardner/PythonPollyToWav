import boto3
import sys
import wave
import easygui
import os
import glob
from os import path
import array

##These access keys need to be your own but I will leave mine in for Rui to test

##Will create speech files in the folder with your speech.txt file in a folder called "Slide Speeches"

def PollySpeechCreation(TextsToBeSynthesised, Directory):
    i = 0
    for text in TextsToBeSynthesised:
        i+=1
        polly_client = boto3.Session(
            aws_access_key_id="",                     
            aws_secret_access_key="",
            region_name='eu-west-2').client('polly')

        response = polly_client.synthesize_speech(VoiceId='Matthew',
                OutputFormat='pcm',
                Engine='neural',
                Text = text)
        
        outputfilename = "SlideSpeech" + str(i) + ".pcm"

        fullpath = os.path.join(Directory, outputfilename)
        
        file = open(fullpath, 'wb')
        file.write(response['AudioStream'].read())



def PCMtoWAV(Directory):
    for file in glob.glob(os.path.join(Directory, '*.pcm')):
        print(file)
        with open(file, 'rb') as pcmfile:
            pcmdata = pcmfile.read()
        with wave.open(file[:-4]+'.wav', 'wb') as wavfile:
            ##creates a wav file with the same bitrate and number of channels as the original PCM file
            wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata)


def CreateSeparateTexts(inText):
    ##Speeches must be in a text file separated by a blank line I.e. type then press return/enter twice
    SlideSpeeches = open(inText, "r").read().split("\n\n")

    return SlideSpeeches


file = easygui.fileopenbox()

texts = CreateSeparateTexts(file)

##Create new directory for speech files
TextsDirectory = os.path.splitext(file)[0]

if path.exists(TextsDirectory) == True:
    pass
else:
    os.mkdir(TextsDirectory)

PollySpeechCreation(texts, TextsDirectory)
PCMtoWAV(TextsDirectory)
