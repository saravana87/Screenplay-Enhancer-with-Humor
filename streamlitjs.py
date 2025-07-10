import streamlit as st
import streamlit.components.v1 as components

components.html("""
<!DOCTYPE html>
<html>
  <head>
    <style>
      body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
      .recorder-container { text-align: center; margin: 20px 0; }
      .btn { padding: 12px 24px; margin: 8px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s; }
      .btn-start { background: #4CAF50; color: white; }
      .btn-stop { background: #f44336; color: white; }
      .btn:disabled { background: #ccc; cursor: not-allowed; }
      .btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
      .status { margin: 15px 0; padding: 10px; border-radius: 5px; }
      .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
      .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
      .recording { animation: pulse 1s infinite; }
      @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    </style>
  </head>
  <body>
    <div class="recorder-container">
      <h2>🎬 Screenplay Enhancer with Humor</h2>
      <div style="margin: 20px 0;">
        <label for="comedy-style">Comedy Style:</label>
        <select id="comedy-style" style="padding: 8px; margin-left: 10px; border-radius: 4px;">
          <option value="subtle">Subtle</option>
          <option value="witty">Witty</option>
          <option value="slapstick">Slapstick</option>
          <option value="dry">Dry</option>
          <option value="satirical">Satirical</option>
        </select>
      </div>
      <button id="start" class="btn btn-start">🎤 Start Recording</button>
      <button id="stop" class="btn btn-stop" disabled>⏹️ Stop Recording</button>
      <audio id="audio" controls style="display: block; margin: 20px auto;"></audio>
      <div id="status" class="status"></div>
    </div>
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

          // Show loading state
          document.getElementById("status").innerHTML = "🔄 Processing audio...";
          document.getElementById("status").className = "status";

          blob.arrayBuffer().then(buf => {
            fetch("http://localhost:8502/upload_enhanced", {
              method: "POST",
              headers: { "Content-Type": "application/octet-stream" },
              body: buf
            })
            .then(response => {
              if (!response.ok) throw new Error(`HTTP ${response.status}`);
              return response.json();
            })
            .then(data => {
              document.getElementById("status").innerHTML = "✅ Audio processed successfully!";
              document.getElementById("status").className = "status success";
              document.getElementById("transcript").innerHTML = `<p><strong>Original:</strong></p><p>${data.transcript}</p>`;
              document.getElementById("enhanced").innerHTML = `<p><strong>Enhanced:</strong></p><p>${data.enhanced.replace(/\[COMEDY_BLOCK\](.*?)\[\/COMEDY_BLOCK\]/g, '<span style="background: yellow; padding: 2px 4px; border-radius: 3px;">$1</span>')}</p>`;
              document.getElementById("comedy_count").innerText = data.comedy_count;
            })
            .catch(err => {
              document.getElementById("status").innerHTML = "❌ Processing failed. Please try again.";
              document.getElementById("status").className = "status error";
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