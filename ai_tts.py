
import asyncio
import edge_tts
import os

text = open("/storage/emulated/0/christina_dialogue.txt", encoding="utf-8").read()


voices = [
    "en-US-JennyNeural",
    "en-US-AvaNeural",
    "en-US-EmmaNeural",
    "en-US-AriaNeural",
    "en-US-MichelleNeural"
]


voice = voices[0]

async def generate_audio():
    speech = edge_tts.Communicate(text, voice)
    await speech.save("dialogue.mp3")

    location = os.path.abspath("dialogue.mp3")

    print("Audio generated successfully!")
    print("File location:", location)

asyncio.run(generate_audio())

