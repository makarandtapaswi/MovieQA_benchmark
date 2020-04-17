#!/bin/bash
counter=0
for movie in video_clips/tt*; do
    ((counter++))
    imdb_key="${movie##*/}"
    echo "================= ${counter}/140. $imdb_key ================="

    clip_counter=0
    num_files=$(ls video_clips/${imdb_key}/*.mp4 | wc -l)
    for clip in video_clips/${imdb_key}/*.mp4; do
        ((clip_counter++))
        #echo $clip
        clip_fname="${clip##*/}"
        #echo $clip_fname
        clip_name="${clip_fname%.*}"
        echo "${clip_counter}/${num_files}. $clip_name"

        # create output directory, delete if exists from previous runs
        output_dir="video_0.5fps/${imdb_key}/${clip_name}"
        rm -rf ${output_dir}
        mkdir -p ${output_dir}

        # write ffprobe information of the video to a file
        echo ${clip} > ${output_dir}/info.txt
        ffprobe_info ${clip} >> ${output_dir}/info.txt

        # burst frames
        ffmpeg -hide_banner -loglevel panic -i ${clip} -qscale:v 2 -r 1/2 ${output_dir}/%03d.jpg

    done
done


