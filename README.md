# Winnow Vision - Video Playback Control Service

This repository contains a proof-of-concept prototype for a Video Playback Control Service. The goal of this tool is to automate test scenarios for the Winnow Vision system by programmatically triggering pre-recorded waste event videos on a local monitor.

## 1. Design Description

**Overall Design**
The solution is a local web server built with Python and Flask. It acts as an intermediary between the Automated Test Runner and a local media player (VLC). It listens for HTTP requests and uses Python's native `subprocess` module to launch, monitor, and kill the video player process.

**Proposed API Interface**
The service exposes three simple REST endpoints:

* `POST /play`
    * **Payload:** `{"video_name": "test_apple.mp4"}`
    * **Action:** Starts playing the specified video in fullscreen. If another video is already playing, it stops it first to prevent overlapping windows.
    * **Error Handling:** Returns `404 Not Found` if the video file doesn't exist on disk, or `400 Bad Request` if the payload is missing.
* `POST /stop`
    * **Action:** Forcibly terminates the current video process. Returns a `200 OK`.
* `GET /status`
    * **Action:** Checks the system state by polling the OS process. 
    * **Response:** `{"status": "playing", "current_video": "test_apple.mp4"}` or `{"status": "idle", "current_video": null}`.

**Main Components**
1.  **Flask API:** Handles the incoming HTTP routing and JSON parsing.
2.  **Process Manager Logic:** Uses `subprocess.Popen` to trigger the video player and `.terminate()` to kill it.
3.  **Local Storage (`/videos` folder):** A dedicated directory where the pre-recorded MP4 test scenarios are stored.

**Supporting Automated Testing**
This design makes automated testing very reliable. A test script can trigger a video via `POST /play`, and then continuously poll the `GET /status` endpoint. Once the status returns to `idle`, the test runner knows the video has finished playing and can proceed to evaluate the Winnow Vision system's identification results.

---

## 2. Run Instructions and Notes

**Prerequisites & Dependencies**
* **Python 3.x** installed.
* **VLC Media Player** installed on the machine.
* **Flask** (install via `pip install -r requirements.txt`).

**How to Run the Prototype**
1. Clone this repository.
2. Create a folder named `videos` in the root directory and place at least one test video inside (e.g., `test.mp4`).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
