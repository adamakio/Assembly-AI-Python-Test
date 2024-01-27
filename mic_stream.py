import assemblyai as aai
import time
import threading

aai.settings.api_key = f"fb401df1f67247c9a8aaf02d4dd785ee"


def on_open(session_opened: aai.RealtimeSessionOpened):
    print("Session ID:", session_opened.session_id)


def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        print(transcript.text)
    else:
        print(transcript.text, end="\r")
        


def on_error(error: aai.RealtimeError):
    print(type(error))
    print(error.__dict__)
    print("An error occured:", error)


def on_close():
    print("Closing Session")



transcriber = aai.RealtimeTranscriber(
    sample_rate=16_000,
    on_data=on_data,
    on_error=on_error,
    on_open=on_open,
    on_close=on_close,
)
transcriber.connect()
microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)
# Define a function to stream audio from the microphone
# def stream_audio():
#     transcriber.stream(microphone_stream)

# Create a thread for audio streaming
stream_thread = threading.Thread(target=transcriber.stream, args=(microphone_stream,))


# Start the thread
stream_thread.start()


# Optionally, you can perform other tasks here
time.sleep(10)

# Close the microphone:
microphone_stream.close()

# Close the connection when done
transcriber.close()

# Wait for the streaming thread to finish
stream_thread.join(timeout=0.0)

print(stream_thread.is_alive())