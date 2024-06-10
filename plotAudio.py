import numpy as np
import matplotlib.pyplot as plt
from scipy import signal # spectrogram function
from matplotlib import cm # colour map
from pydub import AudioSegment
from pydub.playback import play
import argparse

parser = argparse.ArgumentParser(
                    prog='plotAudio',
                    description='Plot the waveform of the supplied audio file')

parser.add_argument('filename')
args = parser.parse_args()

# import audio and store in a numpy array
sound = AudioSegment.from_file(args.filename)

# convert to mono: as get_array_of_samples in serialized, we need mono content
# for that, pan all the way right and then export right channel.
sound = sound.pan(1)
sound = sound.split_to_mono()[1]
array = np.array(sound.get_array_of_samples())

# compute Audio file time characteristics
sample_rate = sound.frame_rate
duration_s = len(sound) / 1000

# generate time reference
timestamps_secs = np.arange(sample_rate*duration_s) / sample_rate

# extract the spectrum
freq_bins, timestamps, spec = signal.spectrogram(array, sample_rate)

# remove values below 0
spec[spec<0] = 0

# truncate data
first_index = 0
last_index = 50

# 3d plot
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_axis_off()
ax.plot_surface(freq_bins[:, None][first_index:last_index], timestamps[None, :], 10.0*np.log10(spec)[first_index:last_index], cmap=cm.pink)
plt.show()
