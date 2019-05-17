# Simple Kiosk Video Player

This repo contains a super simple HTML5 fullscreen video player that is being used on a RPi-based kiosk. The list of videos is dynamically retrieved from the server using the *autoindex* feature of Nginx.

## Deployment steps on `chilipie-kiosk`

Create the server container:

```
docker run -d --restart always --name kiosk_video -v /home/pi/Videos/:/usr/share/nginx/html/videos -p 80:80 agmangas/auto-video-player:latest-arm32v7
```

Disable Chrome autoplay policy on:

```
chrome://flags/#autoplay-policy
```

Copy the `copy-video.py` script to `/home/pi`. This script will automatically look for an MP4 video in a USB flash drive. The first video to be found will be copied to `/home/pi/Videos`.

Add the following to `/home/pi/.xsession` (before Chromium starts):

```
echo "raspberry" | sudo -S /home/pi/copy-video.py > /home/pi/copy-video.log
```