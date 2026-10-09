"""Sugere onde cortar um vídeo a partir do transcript.json do transcrever-video.

Uso: python speech_bounds.py <transcript.json> [--pre 0.4] [--post 1.3] [--gap 20]
Imprime: transcript compacto, pausas longas, a primeira fala e a despedida detectada,
e uma sugestão de START/END. A decisão final é de quem lê o transcript inteiro:
o Whisper costuma "alucinar" frases depois do tchau (ruído de trânsito/vento).
"""
import argparse
import json
import re

FAREWELL = re.compile(
    r"\b(tchau|falou|valeu|fui|até a próxima|até mais|até logo|abraço|beijo|"
    r"se inscreve|inscreva|deixa (o|seu) like|dá um like|bom dia de trabalho|boa noite|"
    r"boa viagem|vamo pra cima|vamos pra cima|vamos para cima|fiquem com deus)\b", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("--pre", type=float, default=0.4, help="folga antes da 1ª palavra")
    ap.add_argument("--post", type=float, default=1.3, help="folga depois da última palavra")
    ap.add_argument("--gap", type=float, default=20, help="pausa (s) considerada longa")
    a = ap.parse_args()

    d = json.load(open(a.transcript, encoding="utf-8"))
    segs = [s for s in d["segments"] if s["words"]]
    print(f"Duração do áudio: {d['duration']:.1f}s, {len(segs)} segmentos\n")
    for s in segs:
        mark = "  <- despedida?" if FAREWELL.search(s["text"]) else ""
        print(f"{s['start']:7.2f}-{s['end']:7.2f} {s['text']}{mark}")

    print("\nPausas longas (fala ausente):")
    for p, n in zip(segs, segs[1:]):
        if n["start"] - p["end"] >= a.gap:
            print(f"  {p['end']:.1f}s -> {n['start']:.1f}s ({n['start'] - p['end']:.0f}s)")

    first = segs[0]["words"][0]
    # despedida = último segmento com palavra de despedida que não esteja isolado no fim
    farewells = [i for i, s in enumerate(segs) if FAREWELL.search(s["text"])]
    if farewells:
        last = segs[farewells[-1]]
        # se a despedida continua no(s) segmento(s) seguinte(s) colados (< 1,5 s), inclui
        j = farewells[-1]
        while j + 1 < len(segs) and segs[j + 1]["start"] - segs[j]["end"] < 1.5 and \
                len(segs[j + 1]["text"]) < 80 and FAREWELL.search(segs[j]["text"]):
            j += 1
            last = segs[j]
        end_word = last["words"][-1]["end"]
        print(f"\nDespedida detectada: [{last['start']:.2f}] {last['text']}")
        after = [s for s in segs if s["start"] > end_word]
        if after:
            print(f"Depois dela ainda há {len(after)} segmento(s) — confira se é alucinação/ruído:")
            for s in after[:5]:
                print(f"   {s['start']:.2f} {s['text']}")
    else:
        end_word = segs[-1]["words"][-1]["end"]
        print("\nNenhuma despedida reconhecida; usando a última fala.")

    start = max(0.0, first["start"] - a.pre)
    end = min(d["duration"], end_word + a.post)
    print(f"\nSUGESTÃO: START={start:.2f} END={end:.2f} DUR={end - start:.2f} "
          f"(1ª palavra '{first['word'].strip()}' em {first['start']:.2f}s)")


if __name__ == "__main__":
    main()
