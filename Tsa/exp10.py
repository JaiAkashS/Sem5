# 1. Import necessary libraries
import speech_recognition as sr

# 2. Define Speech Recognition Function
def speech_recognition_function():
    """Recognize speech using the default microphone."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Speak now!")
        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        recognized_text = recognizer.recognize_google(audio)
        return recognized_text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# 3. Define Error Rate Calculation Function
def calculate_error_rate(original_text, recognized_text):
    """Calculate the error rate using Levenshtein distance."""
    original_text = original_text.lower()
    recognized_text = recognized_text.lower()

    # Initialize matrix
    len_orig = len(original_text) + 1
    len_rec = len(recognized_text) + 1
    matrix = [[0] * len_rec for _ in range(len_orig)]

    # Initialize first row and column
    for i in range(len_orig):
        matrix[i][0] = i
    for j in range(len_rec):
        matrix[0][j] = j

    # Compute Levenshtein distance
    for i in range(1, len_orig):
        for j in range(1, len_rec):
            if original_text[i - 1] == recognized_text[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost
            )

    distance = matrix[-1][-1]
    error_rate = distance / len(original_text)
    return error_rate

def main():
    original_text = "Artificial Intelligence is transforming the world rapidly."
    print("Original text:", original_text)

    recognized_text = speech_recognition_function()

    if recognized_text is not None:
        print("Recognized text:", recognized_text)
        error_rate = calculate_error_rate(original_text, recognized_text)
        print(f"Error Rate: {error_rate:.2%}")
    else:
        print("Speech recognition failed.")

main()