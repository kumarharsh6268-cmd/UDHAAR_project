# UDHAAR: 47 Names, Episode 0 (Pilot) production project

Final: edit/UDHAAR_Ep0_Pilot.mp4 (1080x1920, 30 fps, 92 s, -14 LUFS)

## Narration (Kabir only; Roman Hindi as captioned, Devanagari used for synthesis)
See vo/script.tsv (id, pause-after, speed, Roman, Devanagari). Selected takes: vo/selected.json.

## Rebuild
- Shots:  scripts/build.sh sNN '{"grade":"dawn|day|tungsten|night|memory"}'   (SVG -> Chromium -> painterly post)
- VO:     python3 scripts/build_vo.py        -> edit/vo.wav + edit/vo_lines.json
- Mix:    python3 sound/mix.py edit/timeline.json edit/vo.wav edit/mix.wav
- Video:  python3 edit/render.py edit/video_noaudio.mp4   (EDL + overlays in edit/edl.py)
- Mux:    ffmpeg -i edit/video_noaudio.mp4 -i edit/mix.wav -c:v libx264 -crf 20 -maxrate 12M -bufsize 24M -c:a aac -b:a 192k -shortest out.mp4

## Character / prop lock for later episodes
Kabir: profile in scripts/shapes.py (KABIR_PROFILE/HAIR), white kurta at funeral, faded blue shirt (#6f8aa0) from the notice onward.
Ma (Sudha): MA_L profile, white widow's saree pallu over head, no bindi.
Papa (Mohan): scripts/papa_face.py (sepia portrait, khaki uniform, full moustache).
Shankar: old man silhouette with stick + shawl; LEFT hand has three fingers (shapes.HAND_L3), shown in s06.
Red ledger = the only saturated red (art.RED_DEF). Brass dome bell = art.bell().
Planted for rewatch: wheelchair figure faint at the back of the funeral (s01), Shankar's three-fingered hand (s06),
"Ma didn't ask anyone" (L03), 46 mourners vs 47 names.
