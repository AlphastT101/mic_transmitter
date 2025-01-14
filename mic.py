import pyaudio
import socket

def main():
    addr = input("Enter the receiver's LAN IP: ")
    port = 9678

    # Socket setup
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))
    print("Connected to the receiver, streaming audio...")

    # PyAudio setup
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=48000,
                        input=True,
                        frames_per_buffer=1024)

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            sock.sendall(data)
    except KeyboardInterrupt:
        print("Streaming stopped.")
    finally:
        # Clean up resources
        stream.stop_stream()
        stream.close()
        audio.terminate()
        sock.close()

if __name__ == "__main__":
    main()
