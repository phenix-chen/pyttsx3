import os
import re
import subprocess
import sys
from tkinter import N
from typing import Optional


def check_ffmpeg_installed():
    """检查是否安装了ffmpeg"""
    result = subprocess.run(
        ["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        print("ffmpeg could not be found. Please install it and try again.")
        sys.exit(1)
    else:
        print("ffmpeg is installed.")


def get_audio_files(input_dir):
    """获取目录中的所有音频文件"""
    audio_files = []
    for ext in ("mp3", "wav"):
        audio_files.extend(
            [
                os.path.join(input_dir, f)
                for f in os.listdir(input_dir)
                if f.endswith(ext)
            ]
        )
    return audio_files


def get_end_time(temp_log):
    """获取最后一个非静音段的时间戳"""
    silence_starts = [
        float(match.group(1))
        for match in re.finditer(r"silence_start: (\d+\.\d+)", temp_log)
    ]
    silence_ends = [
        float(match.group(1))
        for match in re.finditer(r"silence_end: (\d+\.\d+)", temp_log)
    ]
    if silence_starts:
        end_time = silence_starts[-1]
        first_end_time = silence_ends[-2] if len(silence_ends) > 1 else 0
        slience_time = end_time - first_end_time
        return first_end_time, end_time, slience_time
    return None, None, None


def process_audio_file(input_file, output_dir):
    """处理单个音频文件"""
    filename = os.path.basename(input_file)
    filename_no_ext = os.path.splitext(filename)[0]
    output_file = os.path.join(output_dir, f"{filename_no_ext}.wav")

    temp_log = subprocess.run(
        [
            "ffmpeg",
            "-i",
            input_file,
            "-af",
            "silencedetect=noise=-30dB:d=0.1",
            "-f",
            "null",
            "-",
        ],
        stderr=subprocess.PIPE,
        text=True,
    ).stderr

    # print(temp_log)
    first_end_time, end_time, slience_time = get_end_time(temp_log)

    if end_time is None:
        print(f"No silence detected in {input_file}")
        return

    print(f"Trimming {input_file} to {output_file}")
    if os.path.exists(output_file):
        print(f"File {output_file} already exists. Skipping.")
        return
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            input_file,
            "-ss",
            str(first_end_time),
            "-t",
            str(end_time),
            output_file,
        ]
    )


def trim_audios(input_dir: str, output_dir: Optional[str] = None):
    check_ffmpeg_installed()

    if not os.path.isdir(input_dir):
        print(f"Directory {input_dir} does not exist.")
        sys.exit(1)

    if output_dir is None:
        output_dir = os.path.join(input_dir, "trimmed_files")

    os.makedirs(output_dir, exist_ok=True)

    audio_files = get_audio_files(input_dir)

    for input_file in audio_files:
        if not os.path.isfile(input_file):
            continue
        process_audio_file(input_file, output_dir)

    print("All audio files have been processed.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py directory")
        sys.exit(1)

    input_dir = sys.argv[1]
    trim_audios(input_dir)
