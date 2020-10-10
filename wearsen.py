import numpy as np
import math
import pyaudio
import matplotlib.pyplot as graph
from numpy.fft import fft,fftfreq
import struct

sRate = 16000
audioDura=1
chunk = 1024
thresh = 2000


def rec_data(stream):
	recFrames = []
	for a in range(int(sRate/chunk*float(audioDura))):
		recData = stream.read(chunk)
		recFrames.append(np.fromstring(recData,dtype=np.int16))
	npData = np.hstack(recFrames)
	return npData




portAudio = pyaudio.PyAudio()
outStream = portAudio.open(format=pyaudio.paInt16,channels=1,rate=sRate,output=True)
recStream = portAudio.open(format=pyaudio.paInt16,channels=1,rate=sRate,input=True,frames_per_buffer=chunk)



outStream.stop_stream()
outStream.close()


graph.ion()
fig = graph.figure()
fig1 = graph.subplot(211)
fig2 = graph.subplot(212)
graph.gcf()
graph.show()

while True:
	x=[]
	y=[]
	nrf = {}
	npData = rec_data(recStream)
	fftVals = fft(npData)
	n = np.size(npData)
	fr = fftfreq(n)
	mask = fr>0
	theo = np.abs(fftVals)
	fig1.cla()
	fig1.plot(npData)
	fig2.cla()
	tempx = sRate*fr[mask]
	tempy = 2*theo[mask]/n
	for i in range(len(tempx)):
		if tempy[i]>=thresh:
			x.append(tempx[i])
			nrf[math.ceil(tempx[i])]=tempy[i]
			y.append(tempy[i])
	
	fig2.plot(x,y,label="Separated Frequencies")
	fig2.legend()
	fig.canvas.draw()

portAudio.terminate()









