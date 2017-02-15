'''

Autor: Gurkirt Singh
Start data: 2nd May 2016
purpose: of this file is to take all .mp4 videos and convert them to jpg images

'''

import numpy as np
import cv2 as cv2
import math,pickle,shutil,os
import json

baseDir = "/mnt/jupiter-gamma/actnet/";
vidDir = "/mnt/jupiter-gamma/actnet/videos/";
imgDir = "/mnt/jupiter-gamma/actnet/rgb-images/";
annotFile = "../hfiles/activity_net.v1-3.min.json"

def getAnnotations():
    with open(annotFile) as f:
        annoData = json.load(f)
    taxonomy = annoData["taxonomy"]
    version = annoData["version"]
    database = annoData["database"]
    print len(database),version,len(taxonomy)
    
def getsmallestDimto256(width,height):
    if width>=height:
        newH = 256
        newW = int(math.ceil((float(newH)/height)*width))
    else:
        newW = 256
        newH = int(math.ceil((float(newW)/width)*height))
    return newW,newH

def getframelabels(annotations,numf):
    framelabels = np.ones(numf,dtype='uint16')*200;
    for annot in annotations:
        actionId = annot['class']
        startframe = annot['sf']
        endframe = annot['ef']
        framelabels[startframe:endframe] = int(actionId)-1
    return framelabels
               
def extractframes(vids,fps): # take all .mp4 videos and extract frames using ffmpeg
    
        for idx,vid in enumerate(vids):
            vidfile = baseDir+'videos/'+vid
            imgdir = baseDir+'images/'+vid.split('.')[0]+'/'
            print idx, vid 
            if not os.path.isdir(imgdir):
                os.mkdir(imgdir)
                
            imglist = os.listdir(imgdir);
            imglist = [i for i in imglist if i.endswith('.jpg')];
            
            if len(imglist)<10:
                if fps>0:
                    cmd = 'ffmpeg -i {} -qscale:v 5 -r {} {}%05d.jpg'.format(vidfile,fps,imgdir); #-vsync 0
                else:
                    cmd = 'ffmpeg -i {} -qscale:v 5 {}%05d.jpg'.format(vidfile,imgdir); #-vsync 0
                # PNG format is very storage heavy so I choose jpg.
                # images will be generated in JPG format with quality scale = 5; you can adjust according to you liking 
                # In appearence it doen't look that deblurred as opposed to default settings by ffmpeg
                # @v 5 images will take alomst 145GB
                #f.write(cmd+'\n')
                os.system(cmd)

def saveVidInfo(vids):
    vidinfo = dict();
    count = 0;
    for idx,vid in enumerate(vids):
        vidfile = baseDir+'videos/'+vid
        imgdir = baseDir+'images/'+vid.split('.')[0]+'/'
        imglist = os.listdir(imgdir);
        imglist = [i for i in imglist if i.endswith('.jpg')];
        tfile = 'vidInfos/{}.json'.format(vid.split('.')[0])
        print idx, tfile
        if not os.path.isfile(tfile):
        #os.remove(tfile);
        	cmd  = 'ffprobe -v quiet -print_format json  -show_streams -count_frames {} >>{}'.format(vidfile,tfile)
        # -count_frames option takes the most of the time to run ffprobe
        	print idx,cmd
        	os.system(cmd)
        with open(tfile,'r') as f:
            ffdata = json.load(f)

        if ffdata["streams"][0]['codec_type'] == 'video':
            ffdata = ffdata["streams"][0]
        else:
            ffdata = ffdata["streams"][1]
    
        #os.remove('temp{}.json'.format('0'))
        vinfo = dict();
        vinfo['duration']=float(ffdata['duration']); # frame rate info provided by ffprobe does not always match with ffmpeg framte_rate
        vinfo['extract-num-frames']=len(imglist)
        vinfo['read-num-frames'] = int(ffdata['nb_frames']); # nb_frame provided by ffprobe does not always match with ffmpeg number of frames
        vinfo['frame-rate-info'] = ffdata['r_frame_rate'] # frame rate info provided by ffprobe does not always match with ffmpeg frame_rate
        r_rate = ffdata['r_frame_rate'].split('/');
        r_rate = float(r_rate[0])/float(r_rate[1]);
        vinfo['frame-rate'] = r_rate;
        vinfo['avg-frame-rate'] = ffdata['avg_frame_rate'] # frame rate info provided by ffprobe does not always match with ffmpeg frame_rate
        vidinfo[vid.split('.')[0]] = vinfo;
        print vinfo
        
        #if idx%100 == 0:
          #  print '\n\nwriting video info\n\n'
           # with open('../hfiles/videoInfo.json','w') as f:
           #   json.dump(vidinfo,f)
    with open('../hfiles/videoInfo.json','w') as f:
        json.dump(vidinfo,f)
        
if __name__ == '__main__':
    downloaded = os.listdir(baseDir+'videos') # get list of file
    downloaded = [d for d in downloaded if d.endswith('.mp4') or d.endswith('.mkv')]  # keep only .mp4 files
    print 'number of videos downloded are ', len(downloaded) 
    ############################
    fps = 15; # set fps = 0 if you want to extract at original frame rate
    #extractframes(sorted(downloaded),fps)
    ###########################    
    saveVidInfo(sorted(downloaded))
    # checkConverted(sorted(downloaded))
