import pyaudio
import wave
import tkinter as tk

# Initialize global variables
audio = None
stream = None
filename = ""
channels = 2
sample_format = pyaudio.paInt16
frames_per_second = 44100
frames = []
duration = 0
timer_running = False

def start_timer():
    global duration, timer_running
    try:
        duration = int(duration_entry.get())
        if duration <= 0:
            raise ValueError("Please enter a valid duration greater than 0.")
        
        timer_running = True
        countdown()
    except ValueError as e:
        tk.messagebox.showerror("Error", str(e))

# Function to update the timer
def countdown():
    global duration, timer_running
    
    if timer_running and duration > 0:
        timer_label.config(text=f"Time Left: {duration} seconds")
        length_entry.config(state="disabled")
        duration_entry.configure(state="disabled")
        duration -= 1
        timer_label.after(1000, countdown)  # Call countdown again after 1 second
    elif timer_running and duration == 0:
        timer_label.config(text="Time's up!")
        timer_running = False
        
        record_audio()

def record_audio():
    global audio, stream, filename, channels, sample_format, frames_per_second, frames, duration

    if audio is not None:
        return  # Recording is already in progress

    file = length_entry.get()
    if not file:
        return  # No filename provided

    filename = file + ".wav"
    chunk = 1024

    audio = pyaudio.PyAudio()

    stream = audio.open(format=sample_format,
                        channels=channels,
                        rate=frames_per_second,
                        frames_per_buffer=chunk,
                        input=True)

    print("Recording audio...")

    frames = []
    for i in range(int(frames_per_second / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(sample_format))
    wf.setframerate(frames_per_second)
    wf.writeframes(b"".join(frames))
    length_entry.config(state="normal")
    duration_entry.configure(state="normal")
    duration_entry.config("")
    length_entry.config("")

    wf.close()

def start_recording():
    global frames
    frames = []  # Clear previous frames
    start_timer()

# Create the main Tkinter window
root = tk.Tk()
root.title("Audio Recorder")
root.geometry("700x370")
root.maxsize(700, 370)  # Set maximum dimensions
root.minsize(700, 370)  # Set minimumburlywood1
root.config(bg="indianred4")
# Labels
length_label = tk.Label(root, text="Welcome Audio Recorder", font=("Times New Roman", 20, "bold"),bg="indianred4")
length_label.pack(pady=5)

duration_label = tk.Label(root, text="Recording Duration (seconds):", font=("Times New Roman", 16),bg="indianred4")
duration_label.pack()

# Entry for recording duration
duration_entry = tk.Entry(root, font=("Times New Roman", 16), width=10,bg="indianred4")
duration_entry.pack(pady=2)
filename_lable = tk.Label(root, text="File Name", font=("Times New Roman", 16),bg="indianred4")
filename_lable.place(x=100, y=118)
# Entry for filename
length_entry = tk.Entry(root, font=("Times New Roman", 20, "bold"),bg="indianred4")
length_entry.pack(pady=8)

# Buttons
start_button = tk.Button(root, text="Start Recording", height=2, width=20, font=("Times New Roman", 20, "bold"),bg="indianred4", command=start_recording)
start_button.pack(pady=10)

timer_label = tk.Label(root, text=f"Time Left: {duration} seconds", font=("Times New Roman", 16),bg="indianred4")
timer_label.place(x=250, y=260)

# Start the Tkinter event loop
root.mainloop()
