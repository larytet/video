# video

Intorduction
===============================
A PC application which takes raw video data deleivered over Ethernet and convert the data to a video stream.

How to run on Linux/MacOS
==============================
pip install -r requirements.txt
python convert_pcap.py -h

Links
==============================

*  http://www.chioka.in/python-live-video-streaming-example/
*  http://docs.opencv.org/2.4/doc/tutorials/highgui/video-write/video-write.html
*  http://www.madox.net/blog/2011/06/06/converting-tofrom-rgb565-in-ubuntu-using-ffmpeg/ FFMPEG and RGB565
*  http://stackoverflow.com/questions/4092927/generating-movie-from-python-without-saving-individual-frames-to-file
*  http://stackoverflow.com/questions/5414638/using-numpy-and-pil-to-convert-56516bit-color-to-88824bit-color
*  http://stackoverflow.com/questions/12999674/ffmpeg-which-file-formats-support-stdin-usage


Tips
=============================
*  Convert raw RGB565 file to PNG
ffmpeg -y -vcodec rawvideo -f rawvideo  -pix_fmt rgb565 -s 320x240 -i ./test_320x240_rgb565_noudp.pcap.rgb565 -f image2 -vcodec png ./test_320x240_rgb565_noudp.pcap.rgb565.png

*  Get the data from stdin
cat ./test_320x240_rgb565_noudp.pcap.rgb565 | ffmpeg -y -vcodec rawvideo -f rawvideo  -pix_fmt rgb565 -s 320x240 -i pipe:0  -f image2 -vcodec png ./test_320x240_rgb565_noudp.pcap.rgb565.png

*  Create a video file from multiple PNG files
ffmpeg -y -start_number 0  -i  ./test.127.0.0.1.60410.%d.png ./test.mpg
