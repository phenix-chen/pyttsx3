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
output_dir="${input_dir}/wav_files"
mkdir -p "$output_dir"

# 遍历目录中的所有mp3文件
for input_file in "$input_dir"/*.mp3; do
    # 检查是否存在mp3文件
    if [ ! -e "$input_file" ]; then
        echo "No mp3 files found in the directory."
        exit 1
    fi

    # 获取文件名（不含扩展名）
    filename=$(basename -- "$input_file")
    filename="${filename%.*}"

    # 设置输出文件路径
    output_file="$output_dir/${filename}.wav"

    # 使用ffmpeg进行转换
    ffmpeg -i "$input_file" "$output_file"

    echo "Converted $input_file to $output_file"
done

echo "All mp3 files have been converted to wav files."

