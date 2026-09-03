'''
File:
devices.py

Purpose:
Dedicated file that maintains the objects that define the behavior of various
components of the box

Author:
Dean Badr - 06/2025
'''
# IMPORTS
from gpiozero import Button, PWMLED
from escpos.printer import Usb
from PIL import Image, ImageFont, ImageDraw
import cv2
import threading
import os
import time
# import pyaudio
# import wave

class FM_LED:
    # -------------------------------------------------------------------
    # __init__: Setup the led
    # -------------------------------------------------------------------
    def __init__(self, gpioNum):
        self.__led = PWMLED(gpioNum, initial_value=True)
        self.__led.value = 0.75

    # -------------------------------------------------------------------
    # Off: Turn off the led
    # -------------------------------------------------------------------
    def Off(self, ):
        self.__led.off()

    # -------------------------------------------------------------------
    # On: Turn on the led
    # -------------------------------------------------------------------
    def On(self, ):
        self.__led.on()

    # -------------------------------------------------------------------
    # Blink: Turn off and on a designated amoutn of times
    # -------------------------------------------------------------------
    def Blink(self, amount, spacing):
        self.__led.off()
        time.sleep(0.2)

        for _ in range(amount):
            self.__led.on()
            time.sleep(spacing)
            self.__led.off()
            time.sleep(spacing)
        self.__led.on()

    # -------------------------------------------------------------------
    # Pulse: Turns on and off by fading
    # -------------------------------------------------------------------
    def Pulse(self, n):
        # Delay a little for people to get in position
        self.led.pulse(0.5, 0.5, n)

class FM_Button:
    cooldownTime = 3
    holdTime = 2
    quickAction = None
    holdAction = None
    onReady = None

    __readyToPress = False
    # -------------------------------------------------------------------
    # __init__: Create the button associated with the gpio pin
    # -------------------------------------------------------------------
    def __init__(self, gpio):
        self.__button = Button(gpio, pull_up=True, bounce_time = 0.05)
        self.__button.when_pressed = self.OnPress
        self.__button.when_released = self.OnRelease
        self.__pressTime = time.time()
        self.__releaseTime = time.time()

    # -------------------------------------------------------------------
    # IsReady: Returns the button status
    # -------------------------------------------------------------------
    def IsReady(self):
        return self.__readyToPress

    # -------------------------------------------------------------------
    # OnPress: Track when the button is pressed and what to do
    # -------------------------------------------------------------------
    def OnPress(self):
        if (self.__readyToPress):
            self.__pressTime = time.time()

    # -------------------------------------------------------------------
    # OnRelease: Determine if its a quick press or long press
    # -------------------------------------------------------------------
    def OnRelease(self):
        if not self.__readyToPress:
            return
        self.__readyToPress = False

        self.__releaseTime = time.time()
        print(f"Release Time: {self.__releaseTime}, Press Time: {self.__pressTime}")
        if (self.__releaseTime - self.__pressTime < self.holdTime):
            if self.quickAction is not None:
                self.quickAction()
        elif self.holdAction is not None:
            self.holdAction()

    # -------------------------------------------------------------------
    # UpdateState: Check if the button is ready to be pressed
    # -------------------------------------------------------------------
    def UpdateState(self):
        if not self.__readyToPress:
            if time.time() - self.__releaseTime >= self.cooldownTime:
                self.__readyToPress = True
                if self.onReady is not None:
                    self.onReady()

class FM_Printer:
    pixelWidth = 576
    
    # -------------------------------------------------------------------
    # __init__: Connect to the printer and configure the width of
    # images to print
    # -------------------------------------------------------------------
    def __init__(self, VID, PID, OUT_EP, IN_EP):
        try:
            self.__printer = Usb(
                VID, 
                PID, 
                0, 
                out_ep=OUT_EP, 
                in_ep=IN_EP)
            self.__printer.profile.media['width']['pixels'] = self.pixelWidth
            print("Successfully connect to thermal printer.")
            print("OUT_EP:", hex(self.__printer.out_ep))
            print("IN_EP:", hex(self.__printer.in_ep))
        except Exception as e:
            print(f"Printer setup error: {e}")
            exit()

    # -------------------------------------------------------------------
    # PrintStartMessage: Prints a short welcome note to tell the
    # users when the device is ready to use
    # -------------------------------------------------------------------
    def PrintStartMessage(self):
        if self.__printer == None:
            print("Cannot access a printer.")
            return
        
        print("Printing activation message.")
        self.__printer.ln(5)
        self.__printer.set(align='center', font='b', custom_size=True, width=2, height=2)
        self.__printer.text("WELCOME TO MEM-O-MART!\n")
        self.__printer.ln(2)
        self.__printer.set(align='center', font='a', custom_size=True, width=1, height=1)
        self.__printer.text("Please press the button to receive a \ncopy of your memory! ")
        self.__printer.ln(5)
        self.__printer.cut()  

    # -------------------------------------------------------------------
    # PrintPhoto: Prints the passed in photo
    # -------------------------------------------------------------------
    def PrintPhoto(self, photo, lines=0):
        if self.__printer == None:
            print("Cannot access printer.")
            return

        # photo = photo.convert("L")
        self.__printer.image(photo, center=True)
        self.__printer.ln(lines)
        self.__printer.cut(mode='FULL', feed=True) 

    # -------------------------------------------------------------------
    # PrintBusinessCard: Prints the passed in photo
    # -------------------------------------------------------------------
    def PrintBusinessCard(self, cardPath):
        print("Printing business card")
        abspath = os.path.abspath(".")
        path = os.path.join(abspath, cardPath)
        bc = Image.open(path)
        self.PrintPhoto(bc)

    # -------------------------------------------------------------------
    # Debug: Allows the user to define a custom package to print as
    # a debug statement
    # -------------------------------------------------------------------
    def Debug(self, *, text="Debug line.", beginning_line=1, end_line=1):
        self.__printer.set(align='left', font='a', custom_size=True, width=1, height=1)
        self.__printer.text("DEBUG")
        self.__printer.ln(beginning_line)
        self.__printer.set(align='center', font='b', custom_size=True, width=2, height=2)
        self.__printer.text(text)
        self.__printer.ln(end_line)
        self.__printer.cut()

class FM_Camera:
    # -------------------------------------------------------------------
    # __init__: Connect to the camera via USB
    # -------------------------------------------------------------------
    def __init__(self):
        self.camLock = threading.Lock()
        try:
            self.__camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
            if not self.__camera.isOpened():
                print("Could not open webcam.")
                return False

            self.__camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            print("Connected to camera!")

        except Exception as e:
            print("Failed to open the camera:", e)
            return False

    # -------------------------------------------------------------------
    # SetParameters: Update some camera settings to the passed in
    # value(s)
    # -------------------------------------------------------------------
    def SetParameters(self, *, gain=None, brightness=None, exposure=None):
        if gain is not None:
            self.__camera.set(cv2.CAP_PROP_GAIN, gain)
        if brightness is not None:
            self.__camera.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        if exposure is not None:
            self.__camera.set(cv2.CAP_PROP_EXPOSURE, exposure)

    # -------------------------------------------------------------------
    # GetFrame: Grab a frame from the camera
    # -------------------------------------------------------------------
    def GetFrame(self):
        with self.camLock:
            ret, frame = self.__camera.read()

        if not ret:
            return None

        return frame
    # -------------------------------------------------------------------
    # Capture: Save the image in the camera's current frame
    # -------------------------------------------------------------------
    def Capture(self, filepath):
        try:
            with self.camLock:
                for _ in range(5):
                    self.__camera.read()
                ret, frame = self.__camera.read()

            if not ret:
                print("Failed to capture image")
                return False

            cv2.imwrite(filepath, frame)
            print("Photo saved.")
            return True

        except Exception as e:
            print(f"Camera Error: {e}")
            return False

    # -------------------------------------------------------------------
    # # RecordFrame: Saves the current frame to the video that is recording
    # # -------------------------------------------------------------------
    # def RecordFrame():
    #     # Get the current image in the camera
    #     _, frame = camera.read()

    #     # Write the frame to the output file
    #     video.write(frame)

    # # -------------------------------------------------------------------
    # # RecordStart: Setup a new video to record to
    # # -------------------------------------------------------------------
    # def RecordStart():
    #     global video, audio, cam_lock

    #     # Don't do anything if already recording
    #     if settings.RECORD_VIDEO:
    #         return
    #     settings.RECORD_VIDEO = True

    #     # Read current number
    #     with open("media/videos/index.txt", "r") as f:
    #         count = int(f.read().strip())

    #     # Name of the photo
    #     filename = f"{settings.VIDEO_NAME}_{count}.avi"
    #     audio_filename = f"{settings.AUDIO_NAME}_{count}.wav"

    #     # Directory to save in
    #     abspath = os.path.abspath(".")
    #     v_dir_path = os.path.join(abspath, f"media/videos/{settings.DEEPSAVE_DIR}")
    #     if not os.path.exists(v_dir_path):
    #         os.mkdir(v_dir_path)

    #     # Directory to save in
    #     abspath = os.path.abspath(".")
    #     a_dir_path = os.path.join(abspath, f"media/audio/{settings.DEEPSAVE_DIR}")
    #     if not os.path.exists(a_dir_path):
    #         os.mkdir(a_dir_path)

    #     # Final path
    #     filepath = os.path.join(v_dir_path, filename)
    #     audio_filepath = os.path.join(a_dir_path, audio_filename)

    #     # Increment and save
    #     count += 1
    #     with open("media/videos/index.txt", "w") as f:
    #         f.write(str(count))

    #     # Define the codec and create VideoWriter object
    #     # Get the default frame width and height
    #     frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    #     frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #     video = VideoRecorder(camera, cam_lock, filepath, (frame_width, frame_height))
    #     video.start()
    #     audio = AudioRecorder(audio_filepath)
    #     audio.start()

    # # -------------------------------------------------------------------
    # # RecordStop: Stop recording the current video 
    # # -------------------------------------------------------------------
    # def RecordStop():
    #     # Nothing to stop
    #     if not settings.RECORD_VIDEO:
    #         return
    #     settings.RECORD_VIDEO = False
        
    #     stop_AVrecording(video.save_path)


    # # -------------------------------------------------------------------
    # # stop_AVrecording: Stop the recording and mux it
    # # -------------------------------------------------------------------
    # def stop_AVrecording(filepath):
        
    #     filename = filepath
    #     audio.stop() 
    #     frame_counts = video.frame_counts
    #     elapsed_time = time.time() - video.start_time
    #     recorded_fps = frame_counts / elapsed_time
    #     print("total frames " + str(frame_counts))
    #     print("elapsed time " + str(elapsed_time))
    #     print("recorded fps " + str(recorded_fps))
    #     video.stop() 
    #     print("Video stopped")

    #     # # Makes sure the threads have finished
    #     # if hasattr(video, 'video_thread') and video.video_thread:
    #     #     video.video_thread.join()
    #     # if hasattr(audio, 'audio_thread') and audio.audio_thread:
    #     #     audio.audio_thread.join()

    #     print("No Threads")
    # #    Merging audio and video signal

    #     # if abs(recorded_fps - 6) >= 0.01:    # If the fps rate was higher/lower than expected, re-encode it to the expected

    #     #     print("Re-encoding")
    #     #     cmd = "ffmpeg -r " + str(recorded_fps) + " -i temp_video.avi -pix_fmt yuv420p -r 6 temp_video2.avi"
    #     #     subprocess.call(cmd, shell=True)

    #     #     print("Muxing")
    #     #     cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video2.avi -pix_fmt yuv420p " + filename + ".avi"
    #     #     subprocess.call(cmd, shell=True)

    #     # else:

    #     # print("Normal recording\nMuxing")
    #     # cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.avi -pix_fmt yuv420p " + filename + ".avi"
    #     # subprocess.call(cmd, shell=True)

    #     print("..")

    # # -------------------------------------------------------------------
    # # VideoRecorder: Class for asynchronous video recording
    # # -------------------------------------------------------------------
    # class VideoRecorder():
    #     def __init__(self, camera, cam_lock, save_path="output.avi", resolution=(640, 480)):
    #         super().__init__()
    #         self.save_path = save_path
    #         self.resolution = resolution
    #         self.running = False
    #         self.queue = queue.Queue()
    #         self.cap = camera
    #         self.cam_lock = cam_lock
    #         self.start_time = 0
    #         self.frame_counts = 0
    #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #         self.writer = cv2.VideoWriter(save_path, fourcc, 15, resolution)
    #         self.video_thread = None

    #     def start(self):
    #         self.video_thread = threading.Thread(target=self.run)
    #         self.video_thread.start()

    #     def run(self):
    #         self.running = True
    #         self.start_time = time.time()

    #         while self.running:
    #             with self.cam_lock:
    #                 ret, frame = self.cap.read()
    #             if ret:
    #                 self.writer.write(frame)
    #                 self.frame_counts+=1
    #             time.sleep(0.05)

    #     def stop(self):
    #         self.running = False
    #         self.video_thread.join()
    #         self.writer.release()

    # # -------------------------------------------------------------------
    # # AudioRecorder: Class for asynchronous audio recording
    # # -------------------------------------------------------------------
    # class AudioRecorder():
    #     # Audio class based on pyAudio and Wave
    #     def __init__(self, filepath):
    #         self.rate = 16000
    #         self.frames_per_buffer = 1024
    #         self.channels = 1
    #         self.running = False
    #         self.format = pyaudio.paInt16
    #         self.audio_filename = filepath
    #         self.audio = pyaudio.PyAudio()
    #         self.input_device_index = 1

    #         # Optional: Automatically find webcam mic by name
    #         for i in range(self.audio.get_device_count()):
    #             info = self.audio.get_device_info_by_index(i)
    #             if "C270" in info["name"] and info["maxInputChannels"] > 0:
    #                 self.input_device_index = i
    #                 break

    #         self.stream = self.audio.open(format=self.format,
    #                                       channels=self.channels,
    #                                       rate=self.rate,
    #                                       input=True,
    #                                       input_device_index=self.input_device_index,
    #                                       frames_per_buffer = self.frames_per_buffer)
    #         self.audio_frames = []
    #         self.audio_thread = None

    #     # Audio starts being recorded
    #     def run(self):
    #         self.stream.start_stream()
    #         self.running = True
    #         while(self.running):
    #             try:
    #                 data = self.stream.read(self.frames_per_buffer, exception_on_overflow=False)
    #                 self.audio_frames.append(data)
    #             except Exception as e:
    #                 print(f"[Audio Read Error] {e}")
    #                 break

    #     # Finishes the audio recording therefore the thread too    
    #     def stop(self):
    #         if self.running:
    #             self.running = False
    #             self.audio_thread.join()

    #             try:
    #                 self.stream.stop_stream()
    #                 self.stream.close()
    #                 self.audio.terminate()
    #             except Exception as e:
    #                 print(f"[Audio Cleanup Error] {e}")

    #             try:
    #                 waveFile = wave.open(self.audio_filename, 'wb')
    #                 waveFile.setnchannels(self.channels)
    #                 waveFile.setsampwidth(self.audio.get_sample_size(self.format))
    #                 waveFile.setframerate(self.rate)
    #                 waveFile.writeframes(b''.join(self.audio_frames))
    #                 waveFile.close()
    #             except Exception as e:
    #                 print(f"[Wave File Error] {e}")
    #         pass

    #     # Launches the audio recording function using a thread
    #     def start(self):
    #         self.audio_thread = threading.Thread(target=self.run)
    #         self.audio_thread.start()