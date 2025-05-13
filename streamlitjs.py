import streamlit as st
import streamlit.components.v1 as components

components.html("""
<!DOCTYPE html>
<html>
  <body>
    <h4>🎤 Simple Audio Recorder</h4>
    <button id="start">Start</button>
    <button id="stop" disabled>Stop</button>
    <audio id="audio" controls></audio>
    
    <div id="status"></div>
    <hr>
    <div style="display: flex; gap: 20px;">
      <div style="width: 50%; background: #f0f0f0; padding: 10px; border-radius: 8px;">
        <h4>Original Transcript</h4>
        <div id="transcript"></div>
      </div>
      <div style="width: 50%; background: #e0ffe0; padding: 10px; border-radius: 8px;">
        <h4>Enhanced with Comedy</h4>
        <div id="enhanced"></div>
        <div><b>😂 Comedy Blocks:</b> <span id="comedy_count">0</span></div>
      </div>
    </div>

    <script>
      let mediaRecorder;
      let audioChunks = [];

      document.getElementById("start").onclick = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

        mediaRecorder.onstop = () => {
          const blob = new Blob(audioChunks, { type: 'audio/webm' });
          const url = URL.createObjectURL(blob);
          document.getElementById("audio").src = url;

          blob.arrayBuffer().then(buf => {
            fetch("http://localhost:8502/upload_enhanced", {
              method: "POST",
              headers: { "Content-Type": "application/octet-stream" },
              body: buf
            })
            .then(response => response.json())
            .then(data => {
              document.getElementById("status").innerText = "✅ Audio uploaded.";
              document.getElementById("transcript").innerText = data.transcript;
              document.getElementById("enhanced").innerText = data.enhanced;
              document.getElementById("comedy_count").innerText = data.comedy_count;
            })
            .catch(err => {
              document.getElementById("status").innerText = "❌ Upload failed.";
              console.error(err);
            });
          });
        };

        mediaRecorder.start();
        document.getElementById("start").disabled = true;
        document.getElementById("stop").disabled = false;
      };

      document.getElementById("stop").onclick = () => {
        mediaRecorder.stop();
        document.getElementById("start").disabled = false;
        document.getElementById("stop").disabled = true;
      };
    </script>
  </body>
</html>
""", height=600)