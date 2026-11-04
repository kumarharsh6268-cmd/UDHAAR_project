#!/bin/bash
# usage: build6.sh [ids...]   -> art/svg, art/raw, art/final, previews in art/prev
cd /home/claude/udhaar/ep06
mkdir -p art/svg art/raw art/final art/prev
GR=$(python3 shots6.py art/svg "$@") || exit 1
ids=$(echo $GR | tr ' ' '\n' | cut -d: -f1)
python3 /home/claude/udhaar/scripts/render.py art/raw $(for i in $ids; do echo art/svg/$i.svg; done) >/dev/null || exit 1
for kv in $GR; do echo $kv; done | xargs -P 3 -I{} bash -c 'kv={}; i=${kv%%:*}; gr=${kv##*:}; python3 /home/claude/udhaar/scripts/post.py art/raw/$i.png art/final/$i.png "{\"grade\":\"$gr\"}"' 
python3 -c "
import cv2,sys
for i in sys.argv[1:]:
    im=cv2.imread(f'art/final/{i}.png'); cv2.imwrite(f'art/prev/{i}.jpg',cv2.resize(im,(396,704)),[cv2.IMWRITE_JPEG_QUALITY,85])
" $ids
echo built $ids
