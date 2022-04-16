printf -v DATESTR '%(%Y%m%d_%H%M%S)T' -1
FNAME="$HOME/DVR/$DATESTR.h264"
echo "Saving DVR to $FNAME"

raspivid -n -w 1280 -h 720 -sa 10 -sh 10 -b 1000000 -fps 30 -ex sports -t 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! tee name=splitter ! queue ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.193.1 port=5600 splitter. ! queue ! filesink location="$FNAME"
