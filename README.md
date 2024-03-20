# Captcha

## General
This exhibit instructs you to position your face in a well-defined position, then takes your picture from two separate cmeras and shows them side by side, and saves them locally.
Finally, it raises the question on why even though the picutres taken are of the same size, your nose appears larger in one of them, pondering on the effect of perspective.
It is designed to work following a start button push for each language in a timely manner, which in turn simulate keyboard commands to the exhibit.

## Installation & Run
The exhibit runs using python 3 on linux, using the opencv library (known as cv2), and pygame (just to play sounds).
The exhibit is designed for a screen of 1920x1080 resolution, with two webcams connected.

After the latest python 3 installation, use:

```
pip3 install numpy
pip3 install imutils
pip3 install opencv-python
pip3 install pygame
```

To install all necessary packages.

Then, to run, go to the root project dir and run:

```
python3 selfie.py
```

## Log
The exhibit supports a rotating log named captcha-dc.log in the root directory, that logs the following events:
* INIT (exhibit was started and initalization is done)
* START|L (the exhibit was started in language L that can be en/he/ar)
* SHOW (images taken were shown to the user)
* SAVE (images shown were saved locally to png file, see section below)
* In case of an error, the message will consits the error message with its start trace

Each event will be prefixed by a timestamp (year-month-day hour:minute:seconds.mili with year as 4 digit, all rest as 2 digit and milliseconds as 3 digits), a | separator and then INFO or ERROR, another | separator, SELFIE, another | separator, then the memory size the exhibit takes in MB (i.e. 100MB), and finally another | separator, then the actual message specified above.

So a sample line will look like this (note the timestamp format, that includes milliseconds):
```
2023-03-15 14:45:30.123|INFO|SELFIE|10MB|START|en
```

## Keyboard Input Interface
For simplicity, the exhibit simply reacts to keyboard.
Then, by having the start buttons simulate keyboard inputs, no special code is needed in the exhibit itself.

The exhibit reacts to the following keyboard characters:

The **h** key starts the exhibit in Hebrew.
The **a** key starts the exhibit in Arabic.
The **e** key starts the exhibit in English.

Upon start, any previous running sequence stops immediately and the exhibit restarts.

Finally, a keyboard input of the **'q'** character quits the exhibit (this is intended to be used with an actual keyboard if wanting to stop the exhibit software from running).

## Image Saving
Each pair of images taken is saved to the /images folder (from root exhibit dir) in one file, showing bot images side by side.
The file name will consist of a time string shown as year-month-day-hour-minute-second-image.png format, with 4-digit for year and 2-digit for the rest. For example: 2023-03-15-14-45-30.png.
The exhibit simply saves the images locally, it doesn't upload them or do any further processing with them.
This is left for an offline process that suits the needs of the exhibit.