# from gtts import gTTS
# from io import BytesIO
#
# tts = gTTS("颊侧袋深", lang='zh-CN')
# with open("test.wav", "wb") as f:
#     tts.write_to_fp(f)
import asyncio
import os.path

import edge_tts
from trim_audios import trim_audios


async def amain(multiple, output_dir) -> None:
    rate = f"+{int(multiple * 100)}%"
    tts_words_file = "script/tts_words.txt"
    VOICE = "zh-CN-XiaoxiaoNeural"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(tts_words_file, "r", encoding="utf-8") as f:
        texts = f.readlines()
    for text in texts:
        text = text.strip()
        prefix = "".join(text.split(" "))
        print(text)
        output = f"{output_dir}/{prefix}.mp3"
        if os.path.exists(output):
            continue
        communicate = edge_tts.Communicate(text, VOICE, rate=rate)
        await communicate.save(output)


if __name__ == "__main__":
    multiple = 1.5
    tts_audios_dir = f"script/audios{multiple}"
    trim_audios_dir = "pyttsx3/drivers/audios"
    asyncio.run(amain(multiple, tts_audios_dir))
    trim_audios(tts_audios_dir, trim_audios_dir)
