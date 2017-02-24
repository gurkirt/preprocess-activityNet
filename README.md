## Introduction 
This repository is intended to provide utility scripts to pre-process ActivityNet dataset for detection task. 
Also, it provide a script to cross check if your downloaded video files are same they were suppose to be.
There could be multiple reasons that downloaded video files has been altered from the original video files on which annotations were annotated. 
For instance, video could is altered by youtube user, or it could be altered by youtube to encode it better for  efficiency etc.

Finally, after dataset cross check. We will go for original aim of [actNet-inAct](https://github.com/gurkirt/actNet-inAct) 
to generate frame level (start frame and end frame for an activity instance) annotations rather than time level (start time and end time of activity instance).

## Dependencies 
**ffmpeg** is only dependency. You install it on Ubuntu using **sudo apt-get install ffmpeg**

Also, download the video files using [Crawler](https://github.com/activitynet/ActivityNet)

## Extract images from video files of ActivityNet

All the utility scripts are in *python-scripts* directory.

### Script No. 1: *extractMP4toJPG-ffmpeg.py*

It takes base path to videos directory as input. Change **baseDir** according to your uses.

It will create **images** directory base path along with with *videos* directory.

It will extract images from video at a set fps (15); you can change fps. If fps set to 0 then it uses the video's default fps.

Next, it has another function that saves the meta information about video using **ffprobe**. This will dump videoname.json file in subdirectory **videinfos**. 
Finally, single file contain meta data of all the videos is dumped in **../hfiles/videinfo.json**.

### Script No. 2: *crossCheck.py*

It reads *../hfiles/videinfo.json* and annotations. It cross check the discrepancy between duration of video provided in annotation and videinfo.json. 

please let me know if you find any bug or have suggestions on <guru094> at <gmail> dot <com>
