#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, math, random, os
sys.path.append('/usr/local/lib/python2.3/site-packages/libavg')
sys.path.append('/usr/local/lib/python2.4/site-packages/libavg')
import avg
import anim

minVideoWidth = 80
minVideoHeight = 60
screenWidth = 1024
screenHeight = 768


def init_video_nodes():
    global numVideos
    numVideos = Player.getElementByID("main").getNumChildren()
    for i in range(numVideos):
        curNode = Player.getElementByID("video"+str(i+1))
        curNode.opacity = 0
        curNode.y = (screenHeight-minVideoHeight)/2

def get_video_files():
    global numVideos
    videoDir = "/home/uzadow/libavg/libavg/src/test/enterprise/"
    files = os.listdir(videoDir)
    numVideos = len(files)
    if numVideos > Player.getElementByID("main").getNumChildren():
        numVideos = Player.getElementByID("main").getNumChildren()
    for i in range(numVideos):
        curNode = Player.getElementByID("video"+str(i+1))
        curNode.opacity = 1
        curNode.href = videoDir+files[i]
        curNode.width = minVideoWidth
        curNode.height = minVideoHeight
        curNode.play()

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
    videoHeight = videoWidth*3/4.0
    range = (numVideos)*(videoWidth+20)-screenWidth+20
#    offset = -random.random()*range
    offset = -(event.x*range)/screenWidth+10
    position_videos(offset, videoWidth, videoHeight)

Player = avg.Player()
Log = avg.Logger.get()
Player.setResolution(1, 0, 0, 0) 
Log.setCategories(Log.APP |
                  Log.WARNING | 
                  Log.PROFILE |
#                  Log.PROFILE_LATEFRAMES |
                  Log.CONFIG
#                  Log.MEMORY  |
#                  Log.BLTS    
#                  Log.EVENTS
                  )

Player.loadFile("videochooser.avg")
anim.init(Player)
init_video_nodes()
get_video_files()
position_videos(-100, 80, 60)
Player.setInterval(10, onframe)
Player.setFramerate(100)
Player.play()
