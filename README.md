# System Sound Recorder using Python (for Linux)

### Setup

We use PulseAudio Volume Control (pavucontrol) to monitor the signal.
The scripts are written in Python3.8 and we use PyAudio & sounddevice to capture the data from the InputStream.
The data is then written onto .WAV files.

To ensure a memory overflow does not occur, an episode parameter can be passed with the record.py which ensures each file is written for the episode length.
By default, the episode length is set to 30 minutes.

To stop the recording, press the ESC key.


### Recording Sound

#### First Time Use

1. Install PulseAudio VC and create a virtualenv using `venv`.
2. Activate the virtualenv and install required libraries using `pip install -r requirements.txt`.
2. Start PulseAudio Volume Control and go to the Recordings tab.
3. While PulseAudio VC is running, use the command prompt to execute `python record.py --episode 5`.
4. Go to the PulseAudio VC wndow and ALSA plug-in [python x.x] appear under Recordings tab.
5. Select `Monitor of Built-in Audio Analogue Stereo` from the drop-down list.
6. Go to the recordings folder and check if new .wav files have been created.


#### Regular Use

1. Start PulseAudio VC.
2. While PulseAudio VC is running, use the command prompt to execute `python record.py --episode xx`.

The recordings will be available under `recordings/XYZ/`.


### Splitting WAVs

1. For long recordings, the recorded data can also be split into different tracks based on silence.
2. After the recording is completed, use the command prompt to execute `python process.py --recordings <recordings/XYZ/>`.
NOTE: The silence threshold is set to -48 DBFS because testing showed this is an optimal value for splitting.

The split WAV files will be saved under `data/XYZ/` as `track_1.wav`, `track_2.wav` and so on.