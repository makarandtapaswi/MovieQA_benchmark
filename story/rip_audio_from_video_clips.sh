#!/bin/bash

for dir in video_clips/*; do
    # check valid movie directories
    if [ -d ${dir} ]; then
        echo $dir;
        # get imdb-key
        movie="${dir##*/}"
        echo $movie
        # make output directory
        mkdir -p audio_clips/${movie}

        # check mp4 files in this movie
        for vid in ${dir}/*.mp4; do
            # create output audio filename
            filename=$(basename -- "$vid")
            filename="${filename%.*}"
            out_fname="audio_clips/${movie}/${filename}.aac"

            # run ffmpeg 
            echo "${vid} --> ${out_fname}"
            ffmpeg -hide_banner -loglevel panic -y -i ${vid} ${out_fname}
        done
    fi
done    

#echo ffmpeg -i $vid $audio.mp3

