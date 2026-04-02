import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

VIDEO_DIR = os.path.join(os.path.dirname(__file__), 'videos')
current_process = None
current_video_name = None

def stop_current_video():
    global current_process, current_video_name
    if current_process is not None:
        current_process.terminate()
        current_process.wait()
        current_process = None
        current_video_name = None

@app.route('/play', methods=['POST'])
def play_video():
    global current_process, current_video_name
    
    data = request.get_json()
    if not data or 'video_name' not in data:
        return jsonify({"error": "Please specify 'video_name' in the JSON payload"}), 400
        
    video_name = data['video_name']
    video_path = os.path.join(VIDEO_DIR, video_name)
    
    # verifying the existnce of the file
    if not os.path.exists(video_path):
        return jsonify({"error": f"Video file '{video_name}' not found."}), 404
        
    stop_current_video()
    
    try:
        # lauch the video(vlc)
        vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe" 
        player_command = [vlc_path, "--fullscreen", "--play-and-exit", video_path]
        
        current_process = subprocess.Popen(
            player_command, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        current_video_name = video_name
        
        return jsonify({"message": f"Play started: {video_name}"}), 200
        
    except Exception as e:
        return jsonify({"error": f"There was an error starting the video: {str(e)}"}), 500

@app.route('/stop', methods=['POST'])
def stop_video():
    stop_current_video()
    return jsonify({"message": "Redarea a fost oprita."}), 200

@app.route('/status', methods=['GET'])
def get_status():
    global current_process, current_video_name
    
    # verify the status of the video
    if current_process is not None:
        if current_process.poll() is not None: 
            current_process = None
            current_video_name = None
            
    if current_process is None:
        return jsonify({"status": "idle", "current_video": None}), 200
    else:
        return jsonify({"status": "playing", "current_video": current_video_name}), 200

if __name__ == '__main__':
    os.makedirs(VIDEO_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)