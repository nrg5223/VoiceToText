import tkinter as tk
import customtkinter as ctk
import soundfile as sf
import sounddevice as sd
import whisper
from whisper.tokenizer import LANGUAGES

# Constants ========================================================

app_width = 532
app_height = 632
x_main_label = 10
y_main_label = 110
y_buttons = 280
default_duration = 5

# Tools ============================================================

model = whisper.load_model("base") # options: tiny, base, small, medium, large

# App functions ====================================================

def record():
    duration = float(duration_entry.get()) if duration_entry.get() else default_duration
    fs = 48000  # standard frequency of sampling in Hz
    main_label.configure(text="Recording...")

    # Create a progress bar
    progress = ctk.CTkProgressBar(app, width=400)
    progress.place(x=66, y=200)
    progress.set(0)

    # Start recording
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    # Update progress bar
    for i in range(int(duration * 10)):
        progress.set(i / (duration * 10))
        app.update_idletasks()
        sd.sleep(100) 

    sd.wait()

    # Save as FLAC file at correct sample rate
    output_path = "my_audio.flac"
    sf.write(output_path, myrecording, fs)
    main_label.configure(text="Recording done!")
    progress.place_forget()

def transcribe():
    audio = "my_audio.flac"

    options = {
        "fp16": False,
        "language": None,     # whisper infers the language by default if transcribing
        "task": "transcribe",
    }
    results = model.transcribe(audio, **options)

    output = f"{results["text"]}\n\nDetected Language: {LANGUAGES[results["language"]]}"
    main_label.configure(text=output)

def translate():
    audio = "my_audio.flac"

    options = {
        "fp16": False,
        "language": None,   
        "task": "translate",
    }
    results = model.transcribe(audio, **options)

    output = f"{results["text"]}"
    main_label.configure(text=output)

# UI Elements ======================================================

app = tk.Tk()

main_label = ctk.CTkLabel(
    app, # parent widget
    height=512,
    width=512,
    text_color="black",
    font=("Roboto Medium", 16),
)

recordButton = ctk.CTkButton(
    app,
    height=40,
    width=120,
    font=("Roboto Medium", 20),
    text_color="white",
    fg_color=("white", "gray38"),
    command=record,
)

transcribeButton = ctk.CTkButton(
    app,
    height=40,
    width=120,
    font=("Roboto Medium", 20),
    text_color="white",
    fg_color=("white", "gray38"),
    command=transcribe,
)

translateButton = ctk.CTkButton(
    app,
    height=40,
    width=120,
    font=("Roboto Medium", 20),
    text_color="white",
    fg_color=("white", "gray38"),
    command=translate,
)

duration_label = ctk.CTkLabel(
    app,
    height=40,
    width=120,
    text="Duration (s):",
    font=("Roboto Medium", 16),
    text_color="black",
)
duration_entry = ctk.CTkEntry(
    app,
    height=40,
    width=120,
    font=("Roboto Medium", 16),
)

# UI Layout ========================================================

app.geometry(f"{app_width}x{app_height}")
app.title("Voice to text")
ctk.set_appearance_mode("dark")

main_label.configure(
    text="Welcome to Voice-to-Text!\nTranscriptions and Translations will appear here.",
    wraplength=app_width - 10,
    anchor="n",
    justify="center",
)
main_label.place(x=x_main_label, rely=0.52, relx=0.5, anchor="n")

recordButton.configure(text="Record")
recordButton.place(x=206, y=20)

duration_label.place(x=146, y=80)
duration_entry.place(x=266, y=80)
duration = tk.StringVar()
duration_entry.configure(textvariable=duration)

transcribeButton.configure(text="Transcribe")
transcribeButton.place(x=106, y=y_buttons)

translateButton.configure(text="Translate")
translateButton.place(x=306, y=y_buttons)

# main =============================================================

app.mainloop()