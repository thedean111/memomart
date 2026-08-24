'''
File:
customCamera.py

Purpose:
Dedicated file for all camera-related operations that memomart should use. Contains
modular helper functions that can be called to control the camera behavior throughout
the logic.

Author:
Dean Badr - 06/2025
'''
import cv2
from picamera2 import Picamera2
from PIL import Image
import os
import threading
import queue
import time
import pyaudio
import wave
import settings

camera = None
video = None
audio = None
cam_lock = None

gain_incr = 0
brightness_incr = 0
exposure_incr = 0

# -------------------------------------------------------------------
# SetupCamera: Based on user definition, attempt to connect to a 
# camera plugged into the raspberry pi
# -------------------------------------------------------------------
def SetupCamera():
    global camera, video, cam_lock, gain_incr, brightness_incr, exposure_incr

    try:
        if settings.USE_WEBCAM:
            settings.ROTATION = 90
            camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
            if not camera.isOpened():
                print("Could not open webcam.")
                return False
                # exit()

            camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            camera.set(cv2.CAP_PROP_GAIN, settings.MIN_GAIN)
            camera.set(cv2.CAP_PROP_BRIGHTNESS, settings.MIN_BRIGHTNESS)
            camera.set(cv2.CAP_PROP_EXPOSURE, settings.MIN_EXPOSURE)

        elif settings.USE_PICAM:
            settings.ROTATION = -90
            camera = Picamera2()
            config = camera.create_still_configuration(
                main={"size": (2000, 1500)},
                controls={
                    "Sharpness": 2, 
                    "Contrast": 1,       
                    "Brightness": 0.1,
                    "HdrMode": 1 
            })
            camera.configure(config)
            camera.start()

        cam_lock = threading.Lock()
        print("Camera opened successfully!")

    except Exception as e:
        print("Failed to open the camera:", e)
        return False
        # exit()

    gain_incr = (settings.MAX_GAIN - settings.MIN_GAIN) / settings.CAM_MODE_INCREMENTS
    brightness_incr = (settings.MAX_BRIGHTNESS - settings.MIN_BRIGHTNESS) / settings.CAM_MODE_INCREMENTS
    exposure_incr = (settings.MAX_EXPOSURE - settings.MIN_EXPOSURE) / settings.CAM_MODE_INCREMENTS
    return True
    
# -------------------------------------------------------------------
# SetCameraParams: Using openCV, set any camera params
# -------------------------------------------------------------------
def SetCameraParams(value):
    value = value >= 0 if 1 else -1

    newGain = camera.get(cv2.CAP_PROP_GAIN) + (value * gain_incr)
    if (newGain < settings.MIN_GAIN):
        newGain = settings.MIN_GAIN
    elif (newGain > settings.MAX_GAIN):
        newGain = settings.MAX_GAIN

    newBri = camera.get(cv2.CAP_PROP_BRIGHTNESS) + (value * brightness_incr)
    if (newBri < settings.MIN_BRIGHTNESS):
        newBri = settings.MIN_BRIGHTNESS
    elif (newBri > settings.MAX_BRIGHTNESS):
        newBri = settings.MAX_BRIGHTNESS

    newExpo = camera.get(cv2.CAP_PROP_EXPOSURE) + (value * exposure_incr)
    if (newExpo < settings.MIN_EXPOSURE):
        newExpo = settings.MIN_EXPOSURE
    elif (newExpo > settings.MAX_EXPOSURE):
        newExpo = settings.MAX_EXPOSURE

    print(f"Setting camera params...\nGAIN = {newGain}\nBRIGHTNESS = {newBri}\nEXPOSURE = {newExpo}\n")

    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_GAIN, newGain)
    camera.set(cv2.CAP_PROP_BRIGHTNESS, newBri)
    camera.set(cv2.CAP_PROP_EXPOSURE, newExpo)

# -------------------------------------------------------------------
# RecordFrame: Saves the current frame to the video that is recording
# -------------------------------------------------------------------
def RecordFrame():
    # Get the current image in the camera
    _, frame = camera.read()

    # Write the frame to the output file
    video.write(frame)

# -------------------------------------------------------------------
# RecordStart: Setup a new video to record to
# -------------------------------------------------------------------
def RecordStart():
    global video, audio, cam_lock

    # Don't do anything if already recording
    if settings.RECORD_VIDEO:
        return
    settings.RECORD_VIDEO = True

    # Read current number
    with open("videos/index.txt", "r") as f:
        count = int(f.read().strip())

    # Name of the photo
    filename = f"{settings.VIDEO_NAME}_{count}.avi"
    audio_filename = f"{settings.AUDIO_NAME}_{count}.wav"

    # Directory to save in
    abspath = os.path.abspath(".")
    v_dir_path = os.path.join(abspath, f"videos/{settings.DEEPSAVE_DIR}")
    if not os.path.exists(v_dir_path):
        os.mkdir(v_dir_path)

    # Directory to save in
    abspath = os.path.abspath(".")
    a_dir_path = os.path.join(abspath, f"audio/{settings.DEEPSAVE_DIR}")
    if not os.path.exists(a_dir_path):
        os.mkdir(a_dir_path)

    # Final path
    filepath = os.path.join(v_dir_path, filename)
    audio_filepath = os.path.join(a_dir_path, audio_filename)

    # Increment and save
    count += 1
    with open("videos/index.txt", "w") as f:
        f.write(str(count))

    # Define the codec and create VideoWriter object
    # Get the default frame width and height
    frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    video = VideoRecorder(camera, cam_lock, filepath, (frame_width, frame_height))
    video.start()
    audio = AudioRecorder(audio_filepath)
    audio.start()

# -------------------------------------------------------------------
# RecordStop: Stop recording the current video 
# -------------------------------------------------------------------
def RecordStop():
    # Nothing to stop
    if not settings.RECORD_VIDEO:
        return
    settings.RECORD_VIDEO = False
    
    stop_AVrecording(video.save_path)

# -------------------------------------------------------------------
# Capture: Saves the image in the camera's current frame
# -------------------------------------------------------------------
def Capture():
    global cam_lock

    try:
        filepath = f"{settings.FILENAME}.png"
        if settings.DEEPSAVE_PHOTO:
            # Read current number
            with open("saved_photos/index.txt", "r") as f:
                count = int(f.read().strip())

            # Name of the photo
            filename = f"{settings.FILENAME}_{count}.png"

            # Directory to save in
            abspath = os.path.abspath(".")
            dir_path = os.path.join(abspath, f"saved_photos/{settings.DEEPSAVE_DIR}")
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            # Final path
            filepath = os.path.join(dir_path, filename)

            # Increment and save
            count += 1
            with open("saved_photos/index.txt", "w") as f:
                f.write(str(count))
        
        if settings.USE_WEBCAM:
            with cam_lock:
                for _ in range(5):
                    camera.read()
                ret, frame = camera.read()
            if not ret:
                print("Failed to capture image.")
                return
            print(filepath)
            cv2.imwrite(filepath, frame)
            print("Photo saved.")

        elif settings.USE_PICAM:
            camera.capture_file(filepath)
            print("Photo saved.")

        return filepath
    
    except Exception as e:
        print(f"Camera Error: {e}")
        return

# -------------------------------------------------------------------
# ConfigureMemomartFormat: Open the image at filepath and paste it
# onto one of the memomart frames
# -------------------------------------------------------------------
def ConfigureMemomartFormat(filepath):
    try:
        # Open the image saved by the webcam and do necessary adjustments
        img = Image.open(filepath).rotate(settings.ROTATION, expand=True).resize((settings.PICTURE_SIZE_X, settings.PICTURE_SIZE_Y))

        # Open the frame
        abspath = os.path.abspath(".")
        dir_path = os.path.join(abspath, f"frames/{settings.FRAME}")
        memomartFrame = Image.open(dir_path)

        # Combine the two images
        memomartFrame.paste(img, (settings.PICTURE_OFFSET_X, settings.PICTURE_OFFSET_Y))
        memomartFrame.convert('L').save("memomart_photo.png")
        
        return memomartFrame
    
    except Exception as e:
        print("Photo error:", e)
        return

# -------------------------------------------------------------------
# stop_AVrecording: Stop the recording and mux it
# -------------------------------------------------------------------
def stop_AVrecording(filepath):
    
    filename = filepath
    audio.stop() 
    frame_counts = video.frame_counts
    elapsed_time = time.time() - video.start_time
    recorded_fps = frame_counts / elapsed_time
    print("total frames " + str(frame_counts))
    print("elapsed time " + str(elapsed_time))
    print("recorded fps " + str(recorded_fps))
    video.stop() 
    print("Video stopped")

    # # Makes sure the threads have finished
    # if hasattr(video, 'video_thread') and video.video_thread:
    #     video.video_thread.join()
    # if hasattr(audio, 'audio_thread') and audio.audio_thread:
    #     audio.audio_thread.join()

    print("No Threads")
#    Merging audio and video signal

    # if abs(recorded_fps - 6) >= 0.01:    # If the fps rate was higher/lower than expected, re-encode it to the expected

    #     print("Re-encoding")
    #     cmd = "ffmpeg -r " + str(recorded_fps) + " -i temp_video.avi -pix_fmt yuv420p -r 6 temp_video2.avi"
    #     subprocess.call(cmd, shell=True)

    #     print("Muxing")
    #     cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video2.avi -pix_fmt yuv420p " + filename + ".avi"
    #     subprocess.call(cmd, shell=True)

    # else:

    # print("Normal recording\nMuxing")
    # cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.avi -pix_fmt yuv420p " + filename + ".avi"
    # subprocess.call(cmd, shell=True)

    print("..")

# -------------------------------------------------------------------
# VideoRecorder: Class for asynchronous video recording
# -------------------------------------------------------------------
class VideoRecorder():
    def __init__(self, camera, cam_lock, save_path="output.avi", resolution=(640, 480)):
        super().__init__()
        self.save_path = save_path
        self.resolution = resolution
        self.running = False
        self.queue = queue.Queue()
        self.cap = camera
        self.cam_lock = cam_lock
        self.start_time = 0
        self.frame_counts = 0
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(save_path, fourcc, 15, resolution)
        self.video_thread = None

    def start(self):
        self.video_thread = threading.Thread(target=self.run)
        self.video_thread.start()

    def run(self):
        self.running = True
        self.start_time = time.time()

        while self.running:
            with self.cam_lock:
                ret, frame = self.cap.read()
            if ret:
                self.writer.write(frame)
                self.frame_counts+=1
            time.sleep(0.05)

    def stop(self):
        self.running = False
        self.video_thread.join()
        self.writer.release()

# -------------------------------------------------------------------
# AudioRecorder: Class for asynchronous audio recording
# -------------------------------------------------------------------
class AudioRecorder():
    # Audio class based on pyAudio and Wave
    def __init__(self, filepath):
        self.rate = 16000
        self.frames_per_buffer = 1024
        self.channels = 1
        self.running = False
        self.format = pyaudio.paInt16
        self.audio_filename = filepath
        self.audio = pyaudio.PyAudio()
        self.input_device_index = 1

        # Optional: Automatically find webcam mic by name
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if "C270" in info["name"] and info["maxInputChannels"] > 0:
                self.input_device_index = i
                break

        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      input_device_index=self.input_device_index,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []
        self.audio_thread = None

    # Audio starts being recorded
    def run(self):
        self.stream.start_stream()
        self.running = True
        while(self.running):
            try:
                data = self.stream.read(self.frames_per_buffer, exception_on_overflow=False)
                self.audio_frames.append(data)
            except Exception as e:
                print(f"[Audio Read Error] {e}")
                break

    # Finishes the audio recording therefore the thread too    
    def stop(self):
        if self.running:
            self.running = False
            self.audio_thread.join()

            try:
                self.stream.stop_stream()
                self.stream.close()
                self.audio.terminate()
            except Exception as e:
                print(f"[Audio Cleanup Error] {e}")

            try:
                waveFile = wave.open(self.audio_filename, 'wb')
                waveFile.setnchannels(self.channels)
                waveFile.setsampwidth(self.audio.get_sample_size(self.format))
                waveFile.setframerate(self.rate)
                waveFile.writeframes(b''.join(self.audio_frames))
                waveFile.close()
            except Exception as e:
                print(f"[Wave File Error] {e}")
        pass

    # Launches the audio recording function using a thread
    def start(self):
        self.audio_thread = threading.Thread(target=self.run)
        self.audio_thread.start()
