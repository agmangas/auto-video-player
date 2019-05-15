const videosPath = "/videos";
const videoRe = /href="(.+\.mp4)"/g;

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
    const matches = Array.from(bodyText.matchAll(videoRe));

    console.log("Matches", matches);

    const videoNames = matches
      .map(match => {
        return match.length === 2 ? `${videosPath}/${match[1]}` : null;
      })
      .filter(val => val !== null);

    console.log("Videos", videoNames);

    if (videoNames.length) {
      appendVideo(videoNames[0]);
    }
  })
  .catch(err => {
    console.error(err);
  });
