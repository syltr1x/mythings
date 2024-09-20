#!/usr/bin/env python
# ^ Change this if you don't use venv

from datetime import datetime, timedelta
import subprocess
import whisper

def grabar_audio(duration, output_file):
    command = [
        "ffmpeg",
        "-f", "pulse",          # Change if you don't use pulseaudio
        "-i", "alsa_output.pci-0000_30_00.6.analog-stereo.monitor",        # Change this to your output, see using this: pactl list sources short | grep RUNNING 
        "-t", str(duration),    # Meet time 
        f"{output_file}.wav"
    ]
    
    # Run ffmpeg command
    subprocess.run(command)

def voice_to_text(output_file):
    # Load whisper model
    model = whisper.load_model("base")
    
    # Transcribe voice to text
    result = model.transcribe(output_file+".wav")
    
    # write text in output file
    file = open(f"{output_file}.txt", 'w', encoding='utf8')
    file.write(result["text"])
    file.close()

# Start program
time = datetime.now()
meet_name = input("Meet name >> ")
meet_time = int(input("Meet duration (sec) >> "))
start_time = time.strftime("%d-%m %H:%M")
end_time = (time + timedelta(seconds=meet_time)).strftime("%d-%m %H:%M")
output_file = f"{start_time}_{meet_name}"

# Process meet duration
hours = meet_time // 3600
minutes = (meet_time % 3600) // 60
seconds = meet_time % 60

if hours > 0: duration = f"{hours}:{minutes}:{seconds}"
elif minutes > 0: duration = f"00:{minutes}:{seconds}"
else: duration = f"00:00:{seconds}"

print(f"Recording meet. Time start: {start_time}, meet duration: {duration}, this recording end in: {end_time}")
verf = input("Proceed?[Y/n] >> ")
if verf.lower() == "n":
    print("[!] Program stopped.")
    exit()

# Record meet
grabar_audio(meet_time, output_file)
print("[+] Meet recorded.")

# Transcribe meet
print("[*] Transcribing audio...")
voice_to_text(output_file)
print("[+] Transcript complete.")
