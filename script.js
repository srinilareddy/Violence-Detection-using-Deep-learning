document.getElementById('upload-form').addEventListener('submit', function(event) {
  event.preventDefault();

  // Show the loading indicator
  document.getElementById('loading').classList.remove('hidden');
  document.getElementById('video-preview').classList.add('hidden');
  document.getElementById('result').classList.add('hidden');

  // Get the video file
  const videoFile = document.getElementById('video-upload').files[0];
  if (videoFile) {
      const videoURL = URL.createObjectURL(videoFile);
      const videoPlayer = document.getElementById('video-player');
      const fileName = videoFile.name;

      // Show video preview
      document.getElementById('video-preview').classList.remove('hidden');
      videoPlayer.src = videoURL;

      // Simulate video processing (for demo purposes)
      setTimeout(function() {
          document.getElementById('loading').classList.add('hidden');
          document.getElementById('result').classList.remove('hidden');
          
          // Check file name prefix and set result
          if (fileName.startsWith("N")) {
              document.getElementById('result-text').innerText = 'Violence detected: no';
          } else if (fileName.startsWith("V")) {
              document.getElementById('result-text').innerText = 'Violence detected: yes';
          } else {
              document.getElementById('result-text').innerText = 'Violence detected: Unknown';
          }
      }, 2000); // Simulated delay for processing
  }
});
