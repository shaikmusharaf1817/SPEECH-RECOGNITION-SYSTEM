import speech_recognition as sr
import datetime

def transcribe_audio_from_mic():
    """
    Captures audio from the microphone and transcribes it into text
    using Google's Web Speech API.
    """
    recognizer = sr.Recognizer()

    # Optional: list microphones (uncomment if needed)
    # print("Available microphones:", sr.Microphone.list_microphone_names())

    try:
        with sr.Microphone() as source:
            input("\nPress Enter to start recording...")
            print("\nAdjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            # Set pause threshold to wait longer between pauses
            recognizer.pause_threshold = 1.5 # seconds of silence before it stops

            print("Listening... Please speak now.")
            audio = recognizer.listen(source)

        print("\nTranscribing your speech...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"\nYou said: \"{text}\"")
        return text

    except sr.WaitTimeoutError:
        print("Timeout: You didn’t speak in time.")
    except sr.UnknownValueError:
        print("Speech not clear or no input detected.")
    except sr.RequestError as e:
        print(f"API connection error: {e}")
    except Exception as e:
        print(f"! Unexpected error: {e}")

    return None

def save_transcription(text, filename="transcription_output.txt"):
    """
    Saves the transcribed text to a file with a timestamp.
    """
    with open(filename, "a", encoding="utf-8") as file:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        file.write(f"{timestamp} {text}\n")
    print(f"\nTranscription saved to '{filename}'.")

if __name__ == "__main__":
    print("AI Internship Speech-to-Text Tool")
    print("--------------------------------------")

    while True:
        transcribed_text = transcribe_audio_from_mic()

        if transcribed_text:
            print("\nTranscription complete.")
            save_transcription(transcribed_text)
            break  # Exit after success
        else:
            retry = input("\n Do you want to try again? (yes/no): ").strip().lower()
            if retry not in ['yes', 'y']:
                print("\nExiting. No transcription recorded.")
                break
