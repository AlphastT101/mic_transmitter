import subprocess
import socket

def main():
    addr = input("Enter the receiver's LAN IP: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, 9678))
    print("Connected to the receiver, streaming audio...")

    ffmpeg_command = [
        "ffmpeg",
        "-f", "alsa",  # Use ALSA for audio capture
        "-i", "default",
        "-ar", "48000",  # Sampling rate
        "-ac", "1",      # Mono audio
        "-f", "s16le",   # Raw PCM data format
        "-"
    ]

    ffmpeg = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE)

    try:
        while True:
            data = ffmpeg.stdout.read(1024)
            if not data:
                break
            sock.sendall(data)
    except KeyboardInterrupt:
        print("Streaming stopped.")
    finally:
        sock.close()
        ffmpeg.terminate()

if __name__ == "__main__":
    main()