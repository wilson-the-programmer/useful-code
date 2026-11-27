
import asyncio
import edge_tts

with open("/storage/emulated/0/christina_dialogue.txt", encoding="utf-8") as file:
    text = file.read()

voices = [
    "en-US-AvaNeural",
    "en-US-EmmaNeural",
    "en-US-AriaNeural",
    "en-US-MichelleNeural"
]

async def generate_voices():
    for voice in voices:
        print("Generating:", voice)

        speech = edge_tts.Communicate(
            text,
            voice,
            rate="-5%",
            pitch="+0Hz"
        )

        filename = voice + ".mp3"
        await speech.save("/storage/emulated/0/" + filename)

        print("Saved:", filename)

    print("All four voices generated!")

asyncio.run(generate_voices())

