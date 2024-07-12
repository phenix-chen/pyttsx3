#!/bin/bash

# 检查是否安装了ffmpeg
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg could not be found. Please install it and try again."
    exit
fi

# 检查是否提供了目录参数
if [ $# -eq 0 ]; then
    echo "Usage: $0 directory"
    exit 1
fi

# 获取目录参数
input_dir=$1

# 检查目录是否存在
if [ ! -d "$input_dir" ]; then
    echo "Directory $input_dir does not exist."
    exit 1
fi

# 创建输出目录
output_dir="${input_dir}/trimmed_files"
mkdir -p "$output_dir"

# 遍历目录中的所有音频文件
for input_file in "$input_dir"/*.{mp3,wav}; do
    # 检查文件是否存在
    if [ ! -e "$input_file" ]; then
        continue
    fi

    # 获取文件名（不含扩展名）
    filename=$(basename -- "$input_file")
    filename="${filename%.*}"

    # 使用ffmpeg检测静音部分
    ffmpeg -i "$input_file" -af silencedetect=noise=-30dB:d=0.1 -f null - 2> temp_log.txt

    # 获取最后一个非静音段的时间戳
    end_time=$(grep 'silence_start' temp_log.txt | tail -1 | awk '{print $5}')
    first_end_time=$(grep 'silence_end' temp_log.txt | tail -2 | awk '{print $5}')
    echo AAAAAAAAAA $end_time
    echo BBBBBBBBBB $first_end_time
    first_end_time=$(echo $first_end_time | awk '{print$ 1}')
    echo BBBBBBBBBB $first_end_time
    slience_time=$(echo "$end_time" - "$first_end_time"| bc)
    echo BBBBBBBBBB $slience_time

    if [ -z "$end_time" ]; then
        # 如果没有检测到静音部分，则跳过该文件
        echo "No silence detected in $input_file"
        cp "$input_file" "$output_dir/${filename}_trimmed.${input_file##*.}"
        continue
    fi

    # 设置输出文件路径
    # output_file="$output_dir/${filename}.${input_file##*.}"
    # 获取文件名（不含扩展名）
    filename=$(basename -- "$input_file")
    filename="${filename%.*}"

    # 设置输出文件路径
    output_file="$output_dir/${filename}.wav"

    # 获取音频文件总时长
    duration=$(ffmpeg -i "$input_file" 2>&1 | grep "Duration" | awk '{print $2}' | tr -d ,)

    # 计算新时长（减去 0.5 秒）
    new_duration=$(echo $duration | awk -F: '{print $1":"$2":"$3-0.60b}')

    echo duration $duration
    echo new_duration $new_duration
    echo input_file $input_file
    echo output_file $output_file
    # 裁剪音频文件
    # ffmpeg -i "$input_file" -t $new_duration -c copy "$output_file"
    # ffmpeg -i "$input_file" -ss 0.1 -t $new_duration "$output_file"
    # ffmpeg -i "$input_file" -t $end_time "$output_file"
    ffmpeg -i "$input_file" -ss $first_end_time -t $end_time "$output_file"

    # 使用ffmpeg进行剪切
    # ffmpeg -i "$input_file" -to "$end_time" "$output_file"

    echo "Trimmed $input_file to $output_file"
    echo "$input_file"  $new_duration $output_file
done

# 删除临时日志文件
rm temp_log.txt

echo "All audio files have been processed."

