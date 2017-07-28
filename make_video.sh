#!/bin/bash

#ffmpeg -r 2 -f image2 -s 1280x800 -start_number 1 -i image-%07d.png -vframes 1000 -vcodec libx264 -crf 25 -pix_fmt yuv420p test.mp4
ffmpeg -r 24 -f image2 -s 1280x800 -i image-%07d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p auction_vis_all.mp4

