# VirtualAssistantAvator

A Python Virtual Assistant Project

### Requirements

- Python3
- Virtual environment(python3 venv)
- git

### Clone repository

```
git clone https://github.com/georgie105/VirtualAssistantAvator.git
```

### Setup a virtual environment

The Virtual environment is useful for isolating your project files such that any pip3 installations
are only installed to the project and not globally to your computer.

## Linux

```
python3 -m venv venv
source venv/bin/activate
```

## Windows

```
python3 -m venv venv
venv\Scripts\activate.bat
```

### External Library Installations

1. SpeechRecognition: `pip3 install SpeechRecognition` -> Library for performing speech recognition
2. PyAudio: `pip3 install PyAudio` -> required for using microphone input
3. gTTS: `pip3 install gTTS` -> CLI tool to interface with Google Translate's text-to-speech
4. playsound `pip3 install playsound` -> For playing sounds
