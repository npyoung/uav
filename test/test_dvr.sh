W=1280
H=720
FPS=30
printf -v DATESTR '%(%Y%m%d_%H%M%S)T' -1
FNAME="$HOME/DVR/$DATESTR.mp4"
echo "Saving DVR to $FNAME"

gst-launch-1.0 -v -e v4l2src device=/dev/video0 ! video/x-h264, width=$W, height=$H, framerate=$FPS/1 ! h264parse ! mp4mux ! filesink location="$FNAME"
