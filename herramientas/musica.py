# Música original e calma (30 s), feita por código. Uso: python3 -I musica.py saida.wav
import sys, wave
import numpy as np
SR, DUR = 44100, 30.0
t = np.arange(int(SR * DUR)) / SR
nota = lambda m: 440 * 2 ** ((m - 69) / 12)
# progressão: Dó maior com 7ª, Lá menor, Fá maior com 7ª, Sol (cada acorde 2,5 s)
acordes = [[48, 55, 60, 64, 71], [45, 52, 57, 60, 64], [41, 53, 57, 60, 64], [43, 50, 55, 59, 62]]
mix = np.zeros_like(t)
dur_ac = 2.5
for i in range(int(DUR / dur_ac)):
    ac = acordes[i % 4]; t0 = i * dur_ac
    seg = (t >= t0) & (t < t0 + dur_ac + 1.0)
    tt = t[seg] - t0
    env = np.minimum(1, tt / 0.6) * np.exp(-np.maximum(0, tt - dur_ac) * 4)
    for m in ac[1:]:  # pad suave
        f = nota(m)
        mix[seg] += 0.05 * env * (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt))
    mix[seg] += 0.09 * env * np.sin(2 * np.pi * nota(ac[0]) * tt)  # baixo
    # arpejo em colcheias
    for k in range(8):
        tk = t0 + k * dur_ac / 8
        s2 = (t >= tk) & (t < tk + 1.2)
        ta = t[s2] - tk
        m = ac[1:][k % 4] + 12
        mix[s2] += 0.035 * np.exp(-ta * 5) * np.sin(2 * np.pi * nota(m) * ta) * np.minimum(1, ta / 0.005)
fade_in = np.minimum(1, t / 1.5); fade_out = np.minimum(1, (DUR - t) / 2.5)
mix *= fade_in * fade_out
mix = mix / np.max(np.abs(mix)) * 0.45
estereo = np.stack([mix, np.roll(mix, 220)], axis=1)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((estereo * 32767).astype(np.int16).tobytes())
print("ok")
