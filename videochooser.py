#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, math, random, stat

from libavg import avg
from libavg import anim

aspectRatio = 720.0/400.0
minVideoWidth = 80
minVideoHeight = minVideoWidth/aspectRatio 
screenWidth = 1024
screenHeight = 768

shotNum = 0

def on_key():
    global shotNum
    key = Player.getCurEvent().keystring
    if key == "s":
        shotNum += 1
        Player.screenshot("videochooser"+str(shotNum)+".png")

def init_video_nodes():
    global numVideos
    numVideos = Player.getElementByID("main").getNumChildren()
    for i in range(numVideos):
        curNode = Player.getElementByID("video"+str(i+1))
        curNode.opacity = 0
        curNode.y = (screenHeight-minVideoHeight)/2

def get_video_files():
    global numVideos
    global videoDir
    files = os.listdir(videoDir)
    numVideos = len(files)
    curEntry = 0
    for i in range(numVideos):
        print videoDir+files[i]
        if not(stat.S_ISDIR(os.stat(videoDir+files[i]).st_mode)):
            curEntry+=1
            if curEntry <= Player.getElementByID("main").getNumChildren():
                curNode = Player.getElementByID("video"+str(curEntry))
                curNode.opacity = 1
                curNode.href = videoDir+files[i]
                curNode.width = minVideoWidth
                curNode.height = minVideoHeight
                curNode.play()
    numVideos = curEntry
    if numVideos >= Player.getElementByID("main").getNumChildren():
        numVideos = Player.getElementByID("main").getNumChildren()

def position_videos(offset, videoWidth, videoHeight):
    def playing(x):
        return x < screenWidth and x > -videoWidth
    global numVideos
    for i in range(numVideos):
        curVideo = Player.getElementByID("video"+str(i+1))
        lastpos = curVideo.x
        curVideo.x = i*(videoWidth+20)+offset
        curVideo.y = (screenHeight-videoHeight)/2
        curVideo.width = videoWidth
        curVideo.height = videoHeight
        if playing(curVideo.x) and not(playing(lastpos)):
            curVideo.play()
        if not(playing(curVideo.x)) and playing(lastpos):
            curVideo.pause()
       
frameNum = 0

def onframe():
    global numVideos
    global frameNum
    event = Player.getMouseState()
    if event.y > screenHeight-40:
        videoWidth = minVideoWidth
    else:
        videoWidth = ((1-event.y/(screenHeight-40.0))*(screenWidth-minVideoWidth)+
                     minVideoWidth)
    videoHeight = videoWidth/aspectRatio
    range = (numVideos)*(videoWidth+20)-screenWidth+20
#    offset = -random.random()*range
    offset = -(event.x*range)/screenWidth+10
    position_videos(offset, videoWidth, videoHeight)

if len(sys.argv) < 2:
    print "Usage: videochooser.py <videodir>"
else:
    Player = avg.Player()
    Log = avg.Logger.get()
    Player.setResolution(1, 0, 0, 0) 
    Log.setCategories(Log.APP |
                      Log.WARNING | 
                      Log.PROFILE |
                      Log.PROFILE_LATEFRAMES |
                      Log.CONFIG
#                  Log.MEMORY  |
#                  Log.BLTS    
#                  Log.EVENTS
                      )

    videoDir = sys.argv[1]
    print "Using "+videoDir+" as video directory." 
    Player.loadFile("videochooser.avg")
    anim.init(Player)
    init_video_nodes()
    get_video_files()
    position_videos(-100, minVideoWidth, minVideoHeight)
    Player.setInterval(10, onframe)
    Player.setFramerate(25)
    Player.play()
