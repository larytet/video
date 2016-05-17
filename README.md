# video

Intorduction
===============================
A PC application which takes raw video data deleivered over Ethernet and convert the data to a video stream.

How to run on Linux/MacOS
==============================
pip install -r requirements.txt
python convert_pcap.py -h

Windows 8
==============================
* Install Python 2.7 https://www.python.org/downloads/release/python-2711/
* Clone the repository git clone git@github.com:larytet/video.git or download and uncompess a ZIP
* cd video
* c:\Python27\scripts\pip.exe install -r requirements.txt
* python convert_pcap.py -h

Links
==============================

*  http://www.chioka.in/python-live-video-streaming-example/
*  http://docs.opencv.org/2.4/doc/tutorials/highgui/video-write/video-write.html
*  http://www.madox.net/blog/2011/06/06/converting-tofrom-rgb565-in-ubuntu-using-ffmpeg/ FFMPEG and RGB565
*  http://stackoverflow.com/questions/4092927/generating-movie-from-python-without-saving-individual-frames-to-file
*  http://stackoverflow.com/questions/5414638/using-numpy-and-pil-to-convert-56516bit-color-to-88824bit-color
*  http://stackoverflow.com/questions/12999674/ffmpeg-which-file-formats-support-stdin-usage
*  http://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python Another example with OpenCV
*  http://blog.extramaster.net/2015/07/python-pil-to-mp4.html How to generate video without ffmpeg. OpenCV is assumed


Tips
=============================
*  Convert raw RGB565 file to PNG
ffmpeg -y -vcodec rawvideo -f rawvideo  -pix_fmt rgb565 -s 320x240 -i ./test_320x240_rgb565_noudp.pcap.rgb565 -f image2 -vcodec png ./test_320x240_rgb565_noudp.pcap.rgb565.png

*  Get the data from stdin
cat ./test_320x240_rgb565_noudp.pcap.rgb565 | ffmpeg -y -vcodec rawvideo -f rawvideo  -pix_fmt rgb565 -s 320x240 -i pipe:0  -f image2 -vcodec png ./test_320x240_rgb565_noudp.pcap.rgb565.png

*  Create a video file from multiple PNG files
ffmpeg -y -start_number 0 -r 25 -i  ./test.127.0.0.1.60410.%d.png ./test.mpg
For lossless video try  -codec png out.mov or ffmpeg -r "24" -i "f_%%1d.png" -vcodec "libx264" -crf "0" "output.mkv"
