from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple

import unicodedata
import re

# --- Text utilities ---

_NON_ALNUM_RE = re.compile(r"[^0-9a-zA-Z]+", re.UNICODE)


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join([c for c in normalized if not unicodedata.combining(c)])


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = strip_accents(text)
    text = _NON_ALNUM_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> List[str]:
    cleaned = normalize_text(text)
    return cleaned.split() if cleaned else []


# --- Scoring & feedback ---

def similarity_ratio(expected: str, recognized: str) -> float:
    e = normalize_text(expected)
    r = normalize_text(recognized)
    if not e and not r:
        return 1.0
    return SequenceMatcher(None, e, r).ratio()


def word_diff(expected: str, recognized: str) -> List[Dict[str, str]]:
    e_tokens = tokenize(expected)
    r_tokens = tokenize(recognized)
    sm = SequenceMatcher(None, e_tokens, r_tokens)
    ops: List[Dict[str, str]] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        e_part = " ".join(e_tokens[i1:i2])
        r_part = " ".join(r_tokens[j1:j2])
        ops.append({"op": tag, "expected": e_part, "recognized": r_part})
    return ops


def compute_scores(expected: str, recognized: str) -> Dict[str, float]:
    e_tokens = tokenize(expected)
    r_tokens = tokenize(recognized)
    sm_words = SequenceMatcher(None, e_tokens, r_tokens)
    equal_words = sum((i2 - i1) for tag, i1, i2, j1, j2 in sm_words.get_opcodes() if tag == "equal")
    total_expected = max(1, len(e_tokens))
    word_accuracy = equal_words / total_expected

    char_sim = similarity_ratio(expected, recognized)
    return {
        "char_similarity": round(char_sim * 100.0, 2),
        "word_accuracy": round(word_accuracy * 100.0, 2),
    }


def generate_feedback(expected: str, recognized: str, max_items: int = 3) -> List[str]:
    ops = word_diff(expected, recognized)
    issues: List[Tuple[str, int]] = []
    for op in ops:
        if op["op"] in {"replace", "delete"}:
            words = op["expected"].split()
            for w in words:
                if w:
                    issues.append((w, len(w)))
    issues.sort(key=lambda x: (-x[1], x[0]))
    hints = []
    for w, _ in issues[:max_items]:
        hints.append(f"Try pronouncing '{w}' more clearly.")
    if not hints:
        hints.append("Great job! Your pronunciation is clear.")
    return hints


# --- Audio capture & recognition ---

try:
    import speech_recognition as sr
except Exception:
    sr = None  # type: ignore


@dataclass
class ASRResult:
    success: bool
    transcription: Optional[str]
    error: Optional[str]


def recognize_speech_from_mic(
    language: str = "en-US",
    timeout: Optional[float] = None,
    phrase_time_limit: Optional[float] = 10.0,
    ambient_duration: float = 0.5,
) -> ASRResult:
    if sr is None:
        return ASRResult(False, None, "SpeechRecognition or PyAudio not available")
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            if ambient_duration and ambient_duration > 0:
                recognizer.adjust_for_ambient_noise(source, duration=ambient_duration)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    except Exception as e:
        return ASRResult(False, None, str(e))

    try:
        transcription = recognizer.recognize_google(audio, language=language)
        return ASRResult(True, transcription, None)
    except sr.UnknownValueError:
        return ASRResult(False, None, "Could not understand audio")
    except sr.RequestError as e:
        return ASRResult(False, None, f"API unavailable or quota exceeded: {e}")


# --- CLI ---

def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Speech-to-text pronunciation evaluator (English only)")
    p.add_argument("--phrase", type=str, default=None, help="Target phrase to speak (if omitted, you will be prompted)")
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    phrase = args.phrase
    if not phrase:
        try:
            phrase = input("Enter the target sentence to practice: ").strip()
        except KeyboardInterrupt:
            print("\nAborted.")
            return 130
    if not phrase:
        print("No phrase provided.")
        return 2

    print("Target:", phrase)
    print("Please speak after the beep (if any)...")

    # English-only: use defaults (en-US, reasonable timeouts)
    res = recognize_speech_from_mic()

    if not res.success:
        print(f"Recognition failed: {res.error}")
        return 1

    recognized = res.transcription or ""
    print(f"Recognized: {recognized}")

    scores = compute_scores(phrase, recognized)
    print(f"Character similarity: {scores['char_similarity']}%")
    print(f"Word accuracy: {scores['word_accuracy']}%")

    for hint in generate_feedback(phrase, recognized):
        print("-", hint)

    return 0


if __name__ == "__main__":
    sys.exit(main())
