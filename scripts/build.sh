#!/bin/bash
# usage: build.sh sNN '{post json}'
cd /home/claude/udhaar
id=$1; pj=${2:-'{"grade":"dawn"}'}
python3 scripts/shots/$id.py art/svg/$id.svg && python3 scripts/render.py art/raw art/svg/$id.svg >/dev/null && python3 scripts/post.py art/raw/$id.png art/final/$id.png "$pj" && python3 -c "
import cv2; im=cv2.imread('art/final/$id.png'); cv2.imwrite('/tmp/claude-0/$id.jpg', cv2.resize(im,(540,960)))" && echo built $id
