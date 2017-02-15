'''

Autor: Gurkirt Singh
Data: 14th Feb 2016
purpose: of this file is to crosscheck duration obtained using ffprobe and provided in annotations

'''

import numpy as np
import cv2 as cv2
import math,pickle,shutil,os
import json

baseDir = "/mnt/jupiter-gamma/actnet/";
vidDir = "/mnt/jupiter-gamma/actnet/videos/";
imgDir = "/mnt/jupiter-gamma/actnet/rgb-images/";
annotFile = "../hfiles/activity_net.v1-3.min.json"
ffprobeFile = '../hfiles/videoInfo.json';
TSVFile = '../hfiles/info.tsv'

def getAnnotations():
    with open(annotFile) as f:
        annoData = json.load(f)
    taxonomy = annoData["taxonomy"]
    version = annoData["version"]
    database = annoData["database"]
    return taxonomy,version,database
    
def checkConverted(vids):
    print "this is checkConverted videos function"    
    vidlist = os.listdir(vidDir)
    vidlist = [vid for vid in vidlist if vid.endswith(".mp4")]
    print "Number of sucessfully donwloaded ",len(vidlist)
    vcount =0
    for videname in vidlist[15000:]:
        src = vidDir+videname
        numF = getNumFrames(src)
        if numF>0:
            imgname = imgDir+videname.split('.')[0]+"/"+str(numF-1).zfill(5)+".jpg"
            print 'last frame is ',imgname,' vocunt ',vcount
            vcount+=1
            dst = vidDirtemp+videname
            if not os.path.isfile(imgname):
                shutil.move(src,dst)
                print " moved this one to ", dst

def readTSV():
    with open(TSVFile) as f:
        tsvDB = dict();
        lines = f.readlines()
        for line in lines[1:]:
            line = line.rstrip('\r')
            line = line.rstrip('\n');
            line = line.split('\t')
            temp = dict();
            temp['duration'] = float(line[1])
            temp['frame-rate'] = float(line[2])
            temp['num-frames'] = int(line[3])
            tsvDB[line[0]]  = temp;
            
    return tsvDB
def main():
    taxonomy,version,database = getAnnotations()
    # tsvDB = readTSV()
    #actionIDs = getClassIds()
    with open(ffprobeFile,'r') as f:
        ffprobeDBinfo = json.load(f)
    ecount = 0;
    newdatabase = dict();
    verbose = 0
    count = 0;
    nullvids = [];
    for videoID in database.keys():      
            videoname = vidDir+'v_'+videoID;
            count+=1;
            print 'doing ',videoname,' ecount ',ecount,' out of ',count
            vidinfo = database[videoID]
            # vidinfo = tsvDB['v_'+videoID]
            mydict = {'isnull':0}
            if 'v_'+videoID in ffprobeDBinfo.keys():
                storageDir = imgDir+'v_'+videoID+"/"
                #print vidinfo
                ffvidinfo =  ffprobeDBinfo['v_'+videoID]
                # ffvidinfo = tsvDB['v_'+videoID]
                #print ffvidinfo
                dur = float(vidinfo['duration'])
                ffdur = float(ffvidinfo['duration'])
                if abs(ffdur-dur)>0.8:
                    cmd  = 'ffprobe -v quiet -print_format json  -show_streams -count_frames {} >>{}'.format(vidfile,tfile)
                    ecount +=1
            print 'diff more than 1 sec is ', ecount


if __name__ == '__main__':
    downloaded = os.listdir(baseDir+'videos') # get list of file
    vids = [d for d in downloaded if d.endswith('.mp4') or d.endswith('.mkv')]  # keep only .mp4 files
    print 'number of videos downloded are ', len(downloaded) 
    ############################
    fps = 15; # set fps = 0 if you want to extract at original frame rate
    main()
    # extractframes(vids,fps)
    ###########################    
    # saveVidInfo(sorted(vids))
    
    
