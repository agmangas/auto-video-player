const videosPath = "/videos";
const videoRe = /"(.+\.mp4)"/g;

function createVideo(videoPath) {
  const video = document.createElement("video");

  video.src = videoPath;
  video.autoplay = true;
  video.loop = true;
  video.id = "the-video";

  return video;
}

function appendVideo(videoPath) {
  const video = createVideo(videoPath);
  console.log("Appending", video);
  document.body.appendChild(video);
}

fetch(videosPath)
  .then(response => {
    console.log("Response", response);
    return response.text();
  })
  .then(bodyText => {
    const matches = Array.from(bodyText.match(videoRe));

    console.log("Matches", matches);

    const videoNames = matches
      .map(item => item.slice(1, item.length - 1))
      .map(item => `${videosPath}/${item}`);

    console.log("Videos", videoNames);

    if (videoNames.length) {
      appendVideo(videoNames[0]);
    }
  })
  .catch(err => {
    console.error(err);
  });
