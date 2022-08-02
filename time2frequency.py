#dsp ebook ch7 says that sin(x)/x (centered around x=0) is used to separate frequency bands. need to find out more about this.
#in also says "first devise a low-pass filter and then transform it to what you need, high-pass, band-pass, band-reject" 
from __future__ import division
import wave, sys, pygame, struct
from math import log, pi, sin

fn = sys.argv[1]
f = wave.open(fn, 'r')
length = f.getnframes()
sampfreq = f.getframerate()
sampwidth = f.getsampwidth()
numchannels = f.getnchannels()
firstfreq = 20
lastfreq = 20000
freqsperoctave = 10
freqs = []
sinewaves = []
differenceses = []
numfreqs = int(freqsperoctave*log(lastfreq/firstfreq,2))
runningsums = [0]*numfreqs
indexes = [0]*numfreqs
if sampwidth == 2: #other sample widths not supported at this time
  unpackstr = "<" + "h" * numchannels
maxval = 2**(8*sampwidth)/2

for freqn in range(numfreqs):
  freq = firstfreq*2**(freqn/freqsperoctave)
  freqs.append(freq) # missing the last three or so frequencies for some reason
  sinewave = []
  for sinesampn in range(int(sampfreq/freq)):
    #sinesamp = sin(sinesampn*2*pi/(sampfreq/freq))*2**(sampwidth*8)/2
    sinesamp = sin(sinesampn*2*pi/(sampfreq/freq))
    sinewave.append(sinesamp)
  sinewaves.append(sinewave)
  differenceses.append(list())

#print(sinewaves[0])

#sampfreq/freq = 10
#sampfreq/(firstfreq*2**(freqn/freqsperoctave))=10
#sampfreq/10=(firstfreq*2**(freqn/freqsperoctave))
#sampfreq/10/firstfreq=2**(freqn/freqsperocatve)
#freqn/freqsperoctave = log(sampfreq/10/firstfreq), 2)
#freqn = log(sampfreq/10/firstfreq, 2) * freqsperoctave

#print sinewaves[int(log(sampfreq/20/firstfreq, 2) * freqsperoctave)]
  
pygame.init()

width, height = pygame.display.Info().current_w, len(sinewaves)
screen = pygame.display.set_mode((width, height))

#print enumerate(sinewaves[int(log(sampfreq/20/firstfreq, 2) * freqsperoctave)])
#pygame.draw.lines(screen, (255, 255, 255), False, [(x*10, (y+32768)/65536*240) for x, y in enumerate(sinewaves[int(log(sampfreq/20/firstfreq, 2) * freqsperoctave)])])
  
#for x, samp in enumerate(sinewaves[50]):
#  screen.set_at((x, int((samp+1)*height/2)), (255, 255, 255))
  
maxrunningsum = 0

for s in range(length):
  samp = struct.unpack(unpackstr, f.readframes(1))[0]/maxval #not sure if [0] is needed for 1-channel audio
  #screen.set_at((s, int((samp+1)*height/2)), (255, 255, 255))
  for freqindex in range(numfreqs):
    indexn = indexes[freqindex]
    differences = differenceses[freqindex]
    
    #print 'samp: ',samp
    #print 'freqindex:',freqindex
    #print 'indexes[freqindex]:',indexes[freqindex]
    #print 'len(sinewaves[freqindex])',len(sinewaves[freqindex])
    #print 'sinewaves[freqindex][indexes[freqindex]]:',sinewaves[freqindex][indexes[freqindex]]
    sinewave = sinewaves[freqindex]
    product = samp*sinewave[indexn]
    #print(indexn, end=" ")
    runningsums[freqindex] += product
    if len(differences) < len(sinewave):
      differences.append(product)
    else:
      runningsums[freqindex] -= differences[indexn]
      differences[indexn] = product
      indexn = (indexn+1) % len(sinewave)
      indexes[freqindex] = indexn
    
    #wprint runningsums[freqindex]
    if runningsums[freqindex] > maxrunningsum:
      maxrunningsum = runningsums[freqindex]
    screen.set_at((int(s/50), numfreqs-freqindex), (min(abs(runningsums[freqindex]*200), 255),)*3)

print(maxrunningsum)
      
while 1:  
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
  pygame.display.flip()



