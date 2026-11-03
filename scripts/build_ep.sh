#!/bin/bash
# usage: build_ep.sh EPDIR sNN '{post json}'
EP=$1; id=$2; pj=${3:-'{"grade":"dawn"}'}
cd /home/claude/udhaar
python3 $EP/shots/$id.py $EP/art/svg/$id.svg && python3 scripts/render.py $EP/art/raw $EP/art/svg/$id.svg >/dev/null && python3 scripts/post.py $EP/art/raw/$id.png $EP/art/final/$id.png "$pj" && python3 -c "
import cv2; im=cv2.imread('$EP/art/final/$id.png'); cv2.imwrite('/tmp/claude-0/$id.jpg', cv2.resize(im,(540,960)))" && echo built $id
