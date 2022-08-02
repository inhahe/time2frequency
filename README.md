# time2frequency
A failed attempt at a novel way of computing spectrograms

I think I read in a book on DSP that, when you perform a correlation between two signals, a signal can be rotated without changing the result. I also figured you could get the amplitude of a time-domain signals at any given frequency by correlating the signal with a single sine wave of that frequency.

So, I figured, we could create a spectogram of some audio by correlating the input audio with sine waves of every frequency we want to measure, but taking a shortcut: if we just take the product of the current audio sample and the sine wave sample at the current index, add that to a running sum, subtract the product at (index+1) % lengthofsinewave, and then set index to (index+1) % lengthofsinewave, that should be mathematically equivalent to rotating the sine wave by one sample and then correlating the whole thing for each audio sample.

Time complexity is O(n*f), where n is the number of samples in the audio and f is the number of frequencies you're computing.

The result doesn't seem quite correct, but it does bear some resemblance to an actual spectogram, so I thought maybe someone who's better at DSP than I am could tweak it a little somehow and perhaps persuade it to give an accurate result.

Change the `50` in `s/50` to some other value to shrink or expand the spectrogram laterally.

Here's the output of time2frequency for a file called ringin.wav.

![image](https://user-images.githubusercontent.com/61786/182276250-8115cb92-4024-47db-bcf0-fa47cb6ad827.png)

Here's the output for the same file by https://academo.org/demos/spectrum-analyzer/

![image](https://user-images.githubusercontent.com/61786/182276169-bc451c55-9ffa-40d8-9fa2-904d4fa9303b.png)

(The results are somewhat confounded by the fact that the two methods are using different lateral (time) and vertical (frequency) scaling factors.)
