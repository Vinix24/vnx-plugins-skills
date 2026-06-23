#!/usr/bin/env python3
"""Diariseer een WAV met pyannote en plak spreker-labels op een Whisper-JSON-transcript.

Lokaal: de inference draait op deze machine. Het pyannote-model wordt eenmalig
gedownload (gated, vereist een HuggingFace-login + accepteren van de modelvoorwaarden).

Gebruik:
  diarize_merge.py <wav> <whisper_json> <out_txt> [--num-speakers N] [--hf-token TOKEN]

Output: transcript met "SPREKER_00:" / "SPREKER_01:" per aaneengesloten spreker-blok.
Daarna nog een handmatige spreker-map (SPREKER_xx -> Vincent / stakeholder).
"""
import argparse
import json
import os
from collections import defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("whisper_json")
    ap.add_argument("out_txt")
    ap.add_argument("--num-speakers", type=int, default=None)
    ap.add_argument("--hf-token", default=os.environ.get("HF_TOKEN"))
    args = ap.parse_args()

    import torch
    from pyannote.audio import Pipeline

    tok = args.hf_token  # None -> gebruik de gecachte huggingface-login
    try:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-community-1", token=tok)
    except TypeError:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-community-1",
            use_auth_token=(tok if tok else True),
        )
    if torch.backends.mps.is_available():
        pipeline.to(torch.device("mps"))

    kwargs = {}
    if args.num_speakers:
        kwargs["num_speakers"] = args.num_speakers
    diarization = pipeline(args.wav, **kwargs)
    # pyannote 4.x levert DiarizeOutput (.speaker_diarization = Annotation); 3.x levert direct Annotation
    annotation = getattr(diarization, "speaker_diarization", diarization)

    turns = [(t.start, t.end, spk) for t, _, spk in annotation.itertracks(yield_label=True)]

    with open(args.whisper_json) as f:
        segments = json.load(f).get("segments", [])

    def speaker_for(seg):
        s, e = seg["start"], seg["end"]
        overlap = defaultdict(float)
        for ts, te, spk in turns:
            ov = min(e, te) - max(s, ts)
            if ov > 0:
                overlap[spk] += ov
        if not overlap:
            return "SPREKER_?"
        best = max(overlap, key=overlap.get)
        return "SPREKER_" + best.split("_")[-1]

    lines, cur, buf = [], None, []
    for seg in segments:
        spk = speaker_for(seg)
        text = seg["text"].strip()
        if not text:
            continue
        if spk != cur:
            if buf:
                lines.append(f"{cur}: " + " ".join(buf))
            cur, buf = spk, [text]
        else:
            buf.append(text)
    if buf:
        lines.append(f"{cur}: " + " ".join(buf))

    with open(args.out_txt, "w") as f:
        f.write("\n".join(lines) + "\n")

    speakers = sorted({"SPREKER_" + s.split("_")[-1] for _, _, s in turns})
    print(f"[diarize] {len(turns)} beurten, {len(segments)} segmenten, sprekers: {', '.join(speakers)}")
    print(f"[diarize] -> {args.out_txt}")


if __name__ == "__main__":
    main()
