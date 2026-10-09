"""Transcreve um áudio com faster-whisper na GPU local, com timestamps por palavra.

Uso: python transcribe.py <audio.wav> <saida.json> [--model large-v3] [--language pt]
                          [--prompt "contexto..."] [--prompt-file vocabulario.txt] [--cpu] [--no-vad]
Saída: JSON {duration, segments:[{start, end, text, words:[{start,end,word,prob}]}]}

O --prompt/--prompt-file vira o initial_prompt do Whisper: descreva o tipo de vídeo, o sotaque
e liste gírias e nomes próprios (marcas, modelos, ruas, pessoas). Isso melhora muito a grafia.
--no-vad desliga o filtro de voz: necessário para pegar trechos CANTADOS (o VAD trata canto como ruído).
"""
import argparse
import json
import sys

from faster_whisper import WhisperModel

DEFAULT_PROMPT = "Vídeo em português do Brasil, fala informal: pra, tá, tô, né, cê, a gente."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("out")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--language", default="pt")
    ap.add_argument("--prompt", default="")
    ap.add_argument("--prompt-file")
    ap.add_argument("--cpu", action="store_true", help="sem GPU NVIDIA (bem mais lento)")
    ap.add_argument("--no-vad", action="store_true", help="não filtrar por voz (pega canto)")
    args = ap.parse_args()

    prompt = args.prompt
    if args.prompt_file:
        prompt = (prompt + " " + open(args.prompt_file, encoding="utf-8").read()).strip()
    prompt = prompt or DEFAULT_PROMPT

    if args.cpu:
        model = WhisperModel(args.model, device="cpu", compute_type="int8")
    else:
        model = WhisperModel(args.model, device="cuda", compute_type="float16")
    segments, info = model.transcribe(
        args.audio,
        language=args.language,
        beam_size=5,
        word_timestamps=True,
        vad_filter=not args.no_vad,
        vad_parameters={"min_silence_duration_ms": 500},
        initial_prompt=prompt[-900:],  # o Whisper só aproveita ~224 tokens do prompt
        condition_on_previous_text=False,
    )
    out = []
    for s in segments:
        out.append({
            "start": round(s.start, 2),
            "end": round(s.end, 2),
            "text": s.text.strip(),
            "words": [
                {"start": round(w.start, 2), "end": round(w.end, 2),
                 "word": w.word, "prob": round(w.probability, 2)}
                for w in (s.words or [])
            ],
        })
        print(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}", flush=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"duration": info.duration, "segments": out}, f, ensure_ascii=False, indent=1)
    print(f"OK {len(out)} segmentos -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
