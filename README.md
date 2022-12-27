# Narakeet Video Build API example in Python

This repository provides a quick example demonstrating how to access the Narakeet [markdown to video API](https://www.narakeet.com/docs/automating/rest/) from Python.

The example sends a request to generate a video from a local ZIP file (it creates the zip file from the contents of the [video](video) directory, then downloads the resulting video into a local temporary file. 

The example uses the [requests](https://requests.readthedocs.io/en/latest/) python library to send HTTPS requests to the Narakeet API.

## Prerequisites

To use this example, you will need Python (3.7 or more recent), and an API key for Narakeet.

## Running the example

1. set and export a local environment variable called `NARAKEET_API_KEY`, containing your API key (or modify [video.py](video.py) line 4 to include your API key).
2. optionally edit [video.py](video.py) and modify the video file directory, main video file, and the function that handles progress notification (lines 5, 6 and 8).
3. run `pip install -r requirements.txt` to install the required libraries
4. run `python video.py` to create the output audio.

## More information

Check out <https://www.narakeet.com/docs/automating/rest/> for more information on the Narakeet Markdown to Video API. 
