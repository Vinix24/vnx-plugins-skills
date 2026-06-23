#!/usr/bin/env bash
# Lokale spraaktranscriptie — mlx-whisper (Apple Silicon native), optioneel met
# spreker-diarization (pyannote) en/of PII-strip. Volledig lokaal, geen cloud.
#
# Gebruik: transcribe.sh [-e cpp|mlx] [-l taal|auto] [-p] [-d] [-n aantal] [-o uitvoerbestand] audiobestand
#
# PII (-p) en diarization (-d) zijn ONAFHANKELIJK aan/uit te zetten. Combinaties:
#   (geen)    vol transcript, namen erin            -> <out>.txt
#   -d        + sprekerlabels, namen erin           -> <out>.txt, <out>_diarized.txt
#   -p        + PII-stripped, geen sprekers          -> <out>_anon.txt, <out>.map.json
#   -p -d     + PII-stripped MET sprekerlabels       -> ook <out>_diarized_anon.txt
#
# Taal: -l nl (standaard), -l en, -l fr, of -l auto (laat whisper detecteren;
# handig bij meertalige opnames). Standaard engine: mlx. Diarization vereist mlx.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WHISPER_CLI="/opt/homebrew/bin/whisper-cli"
WHISPER_MODEL="$HOME/whisper/models/ggml-large-v3-turbo.bin"
MLX_WHISPER="$HOME/whisper/venv/bin/mlx_whisper"
MLX_MODEL="mlx-community/whisper-large-v3-turbo"
PII_SCRIPT="$SCRIPT_DIR/pii_strip.py"
DIARIZE_SCRIPT="$SCRIPT_DIR/diarize_merge.py"
PII_PYTHON="$HOME/whisper/venv/bin/python3"
LANGUAGE="nl"
ENGINE="mlx"
OUTPUT=""
DO_PII=0
DO_DIAR=0
NUM_SPK=""

usage() {
    echo "Gebruik: $(basename "$0") [-e cpp|mlx] [-l taal|auto] [-p] [-d] [-n aantal] [-o uitvoerbestand.txt] audiobestand"
    echo ""
    echo "  -e cpp   whisper.cpp"
    echo "  -e mlx   mlx-whisper, Apple Silicon native (standaard)"
    echo "  -l       taal: nl (standaard), en, fr, ... of 'auto' voor autodetectie (meertalig)"
    echo "  -p       PII-strip: pseudonimiseer na transcriptie en sla sleuteltabel op"
    echo "  -d       diariseer: voeg spreker-labels toe (pyannote, lokaal; alleen mlx)"
    echo "  -n       aantal sprekers (hint voor diarization; bv. 2 voor een 1-op-1 interview)"
    echo "  -o       uitvoerbestand (optioneel; standaard: <invoer>_<engine>.txt)"
    echo ""
    echo "  -p en -d zijn onafhankelijk; combineer ze vrij. Met -p -d komt er ook"
    echo "  een <out>_diarized_anon.txt (sprekers in, klantdata eruit)."
    exit 1
}

while getopts ":e:l:o:n:pdh" opt; do
    case $opt in
        e) ENGINE="$OPTARG" ;;
        l) LANGUAGE="$OPTARG" ;;
        o) OUTPUT="$OPTARG" ;;
        n) NUM_SPK="$OPTARG" ;;
        p) DO_PII=1 ;;
        d) DO_DIAR=1 ;;
        h) usage ;;
        *) usage ;;
    esac
done
shift $((OPTIND - 1))

[[ $# -lt 1 ]] && usage
INPUT="$1"
[[ ! -f "$INPUT" ]] && { echo "Fout: bestand '$INPUT' niet gevonden."; exit 1; }
[[ "$ENGINE" != "cpp" && "$ENGINE" != "mlx" ]] && { echo "Fout: engine moet 'cpp' of 'mlx' zijn."; exit 1; }
[[ $DO_DIAR -eq 1 && "$ENGINE" != "mlx" ]] && { echo "Fout: -d (diarization) werkt alleen met de mlx-engine."; exit 1; }

# Taal-argument: bij 'auto' laten we --language weg zodat whisper zelf detecteert
LANG_ARG=()
LANG_LABEL="$LANGUAGE"
if [[ "$LANGUAGE" == "auto" ]]; then
    LANG_LABEL="auto-detect"
else
    LANG_ARG=(--language "$LANGUAGE")
fi

# Bepaal uitvoerpad
if [[ -z "$OUTPUT" ]]; then
    BASE="${INPUT%.*}"
    OUTPUT="${BASE}_${ENGINE}.txt"
fi

# Tijdelijk 16kHz mono 16-bit WAV (QuadCast neemt op in 48kHz)
TMP_WAV="$(mktemp /tmp/whisper_XXXXXX.wav)"
trap 'rm -f "$TMP_WAV"' EXIT

echo "[ffmpeg] Omzetten naar 16kHz mono 16-bit WAV..."
ffmpeg -y -i "$INPUT" -ar 16000 -ac 1 -sample_fmt s16 "$TMP_WAV" -loglevel error

START=$(date +%s)

if [[ "$ENGINE" == "cpp" ]]; then
    echo "[whisper.cpp] Transcriberen (taal: $LANG_LABEL)..."
    "$WHISPER_CLI" \
        --model "$WHISPER_MODEL" \
        ${LANG_ARG[@]+"${LANG_ARG[@]}"} \
        --output-txt \
        --output-file "${OUTPUT%.txt}" \
        "$TMP_WAV" \
        2>&1 | grep -v "^load_backend\|^ggml_metal\|^whisper_\|^system_info\|^main:"
    if [[ -f "${OUTPUT%.txt}.txt" && "${OUTPUT%.txt}.txt" != "$OUTPUT" ]]; then
        mv "${OUTPUT%.txt}.txt" "$OUTPUT"
    fi

elif [[ "$ENGINE" == "mlx" ]]; then
    echo "[mlx-whisper] Transcriberen (taal: $LANG_LABEL)..."
    OUTDIR="$(dirname "$OUTPUT")"
    OUTNAME="$(basename "${OUTPUT%.txt}")"
    MLX_FMT="txt"
    [[ $DO_DIAR -eq 1 ]] && MLX_FMT="all"
    # --condition-on-previous-text False voorkomt 'repetition collapse'
    # (lange "Ja. Ja."-hallucinatielussen over stiltes).
    "$MLX_WHISPER" \
        --model "$MLX_MODEL" \
        ${LANG_ARG[@]+"${LANG_ARG[@]}"} \
        --condition-on-previous-text False \
        --output-format "$MLX_FMT" \
        --output-dir "$OUTDIR" \
        --output-name "$OUTNAME" \
        "$TMP_WAV" \
        2>/dev/null
fi

END=$(date +%s)
ELAPSED=$((END - START))

echo ""
echo "=== Transcriptie klaar ==="
echo "Engine  : $ENGINE"
echo "Taal    : $LANG_LABEL"
echo "Tijd    : ${ELAPSED}s"
echo "Uitvoer : $OUTPUT"

# Diarization (optioneel via -d, alleen mlx): spreker-labels uit pyannote, lokaal
DIAR_OUT=""
if [[ $DO_DIAR -eq 1 ]]; then
    echo ""
    echo "[diarize] Sprekers herkennen (pyannote, lokaal)..."
    JSON_FILE="${OUTPUT%.txt}.json"
    DIAR_OUT="${OUTPUT%.txt}_diarized.txt"
    NSPK_ARG=()
    [[ -n "$NUM_SPK" ]] && NSPK_ARG=(--num-speakers "$NUM_SPK")
    "$PII_PYTHON" "$DIARIZE_SCRIPT" "$TMP_WAV" "$JSON_FILE" "$DIAR_OUT" ${NSPK_ARG[@]+"${NSPK_ARG[@]}"}
    rm -f "${OUTPUT%.txt}".vtt "${OUTPUT%.txt}".srt "${OUTPUT%.txt}".tsv
    echo "Gediariseerd : $DIAR_OUT"
    echo ""
    echo "Volgende stap: map de SPREKER_xx-labels naar namen (interviewer = Vincent)."
fi

# PII-strip (optioneel via -p)
if [[ $DO_PII -eq 1 ]]; then
    echo ""
    echo "[pii_strip] Pseudonimiseren..."
    ANON_OUTPUT="${OUTPUT%.txt}_anon.txt"
    MAP_OUTPUT="${OUTPUT%.txt}.map.json"
    "$PII_PYTHON" "$PII_SCRIPT" strip "$OUTPUT" \
        --out "$ANON_OUTPUT" \
        --map "$MAP_OUTPUT"
    echo ""
    echo "Gebruik voor analyse : $ANON_OUTPUT"
    echo "Sleuteltabel         : $MAP_OUTPUT  <- lokaal bewaren!"

    # Combinatie -p -d: ook de diarized-output anonimiseren met DEZELFDE sleuteltabel,
    # zodat sprekerlabels behouden blijven maar klantdata eruit is.
    if [[ $DO_DIAR -eq 1 && -n "$DIAR_OUT" && -f "$DIAR_OUT" ]]; then
        DIAR_ANON="${OUTPUT%.txt}_diarized_anon.txt"
        "$PII_PYTHON" "$PII_SCRIPT" strip "$DIAR_OUT" \
            --out "$DIAR_ANON" \
            --map "$MAP_OUTPUT"
        echo "Gediariseerd + anon  : $DIAR_ANON  (sprekers in, klantdata eruit)"
    fi

    echo ""
    echo "Terugzetten na analyse:"
    echo "  $(basename "$PII_PYTHON") $(basename "$PII_SCRIPT") restore $ANON_OUTPUT --map $MAP_OUTPUT"
fi
