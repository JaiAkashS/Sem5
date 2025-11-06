````markdown
# Speech-to-Text Pronunciation Evaluator

A tiny, single-file Python app that listens to your speech (English), transcribes it, and scores how closely it matches a target phrase. It prints simple feedback.

## Quick start

1) Create/activate a Python 3.10+ environment.

2) Install dependencies:

```bash
pip install -r requirements.txt
```

On Windows, if `PyAudio` fails to install via pip, try:

```bash
pip install pipwin
pipwin install pyaudio
```

3) Run (English only):

```bash
python app.py --phrase "Practice makes progress"
```

If you omit `--phrase`, you'll be prompted to enter one.

## Notes

- Recognition language is fixed to English (en-US).
- Requires internet for the Google recognizer and a working microphone.
- Defaults are tuned for simplicity: just run and speak after the prompt.

````
