#!/bin/bash
# usage: tts_take.sh out.wav speed sid "text"
D=/home/claude/udhaar/tts; export LD_LIBRARY_PATH=$D/sherpa-onnx-v1.13.8-linux-x64-shared/lib; ST=$D/sherpa-onnx-supertonic-3-tts-int8-2026-05-11
$D/sherpa-onnx-v1.13.8-linux-x64-shared/bin/sherpa-onnx-offline-tts --num-threads=1 --supertonic-duration-predictor=$ST/duration_predictor.int8.onnx --supertonic-text-encoder=$ST/text_encoder.int8.onnx --supertonic-vector-estimator=$ST/vector_estimator.int8.onnx --supertonic-vocoder=$ST/vocoder.int8.onnx --supertonic-tts-json=$ST/tts.json --supertonic-unicode-indexer=$ST/unicode_indexer.bin --supertonic-voice-style=$ST/voice.bin --sid=$3 --lang=hi --num-steps=24 --speed=$2 --output-filename=$1 "$4" >/dev/null 2>&1
