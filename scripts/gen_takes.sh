#!/bin/bash
cd /home/claude/udhaar/vo; mkdir -p takes
while IFS=$'\t' read id p sp r d; do for k in 1 2 3 4; do echo "$id	$k	$sp	$d"; done; done < script.tsv | \
  xargs -P 2 -d '\n' -I{} bash -c 'IFS=$'"'"'\t'"'"' read id k sp d <<< "{}"; [ -f takes/${id}_$k.wav ] || /home/claude/udhaar/scripts/tts_take.sh takes/${id}_$k.wav $sp 8 "$d"'
echo GEN_DONE
