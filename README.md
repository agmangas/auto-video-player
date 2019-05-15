# Simple Kiosk Video Player

This repo contains a super simple HTML5 fullscreen video player to deploy on a RPi-based kiosk. The list of videos is dynamically retrieved from the server using the *autoindex* feature of Nginx.

```
docker run -d --restart always --name kiosk_video -v /path/to/videos/:/usr/share/nginx/html/videos -p 80:80 agmangas/auto-video-player
```