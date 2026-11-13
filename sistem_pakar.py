"""Sistem pakar sederhana: masalah kualitas air kolam lele (Forward Chaining).

Cara pakai:
  python sistem_pakar.py                       -> mode tanya-jawab (y/t)
  python sistem_pakar.py --fakta "ikan lemas"  -> mode langsung (bisa diulang)
"""
import argparse
import json
import sys


def muat_kb(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def terpenuhi(aturan, memori):
    """mode 'dan' = semua syarat ada di memori; 'atau' = salah satu cukup."""
    ada = [s in memori for s in aturan["jika"]]
    return all(ada) if aturan["mode"] == "dan" else any(ada)


def fakta_dasar(kb):
    """Fakta yang tidak pernah menjadi hasil aturan -> ditanyakan ke user."""
    hasil = {r["maka"] for r in kb["aturan"]}
    urut = []
    for r in kb["aturan"]:
        for s in r["jika"]:
            if s not in hasil and s not in urut:
                urut.append(s)
    return urut


def tanya_user(daftar):
    print("Jawab y/t.")
    ya = []
    for i, f in enumerate(daftar, 1):
        while True:
            j = input(f"{i}. Apakah {f}? (y/t) > ").strip().lower()
            if j in ("y", "t"):
                break
            print("   Ketik y atau t saja.")
        if j == "y":
            ya.append(f)
    return ya


def forward_chaining(kb, fakta_awal):
    memori = set(fakta_awal)
    asal = {}   # hasil -> aturan yang menghasilkannya
    log = []
    siklus = 0
    while True:
        cocok = [r for r in kb["aturan"]
                 if r["maka"] not in memori and terpenuhi(r, memori)]
        if not cocok:
            log.append(f"Siklus {siklus + 1}: tidak ada aturan baru, berhenti")
            break
        r = cocok[0]
        siklus += 1
        memori.add(r["maka"])
        asal[r["maka"]] = r
        log.append(f"Siklus {siklus}: {r['id']} -> {r['maka']}")
    return memori, asal, log


def kesimpulan_akhir(kb, asal):
    """Hasil aturan yang tidak dipakai sebagai syarat aturan lain."""
    dipakai = {s for r in kb["aturan"] for s in r["jika"]}
    return [h for h in asal if h not in dipakai]


def alasan(h, asal, memori, indent=0, tampil=None):
    tampil = set() if tampil is None else tampil
    if h in tampil or h not in asal:
        return []
    tampil.add(h)
    r = asal[h]
    syarat = [s for s in r["jika"] if s in memori]
    baris = [f"{'    ' * indent}{h}  <- {r['id']} ({', '.join(syarat)}) [{r['sumber']}]"]
    for s in syarat:
        baris += alasan(s, asal, memori, indent + 1, tampil)
    return baris


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kb", default="kb_banjir.json")
    p.add_argument("--fakta", action="append",
                   help="fakta 'ya' (boleh diulang); bila ada, program tidak bertanya")
    a = p.parse_args()

    kb = muat_kb(a.kb)
    dasar = fakta_dasar(kb)
    print(kb["judul"])

    if a.fakta:
        salah = [f for f in a.fakta if f not in dasar]
        if salah:
            sys.exit(f"Fakta tidak dikenal: {salah}\nFakta yang ada: {dasar}")
        fakta = a.fakta
    else:
        fakta = tanya_user(dasar)

    print("\nFakta awal:", ", ".join(fakta) if fakta else "(tidak ada)")
    print()
    memori, asal, log = forward_chaining(kb, fakta)
    print("\n".join(log))
    print()

    hasil = kesimpulan_akhir(kb, asal)
    if not hasil:
        print("Kesimpulan: tidak ada kesimpulan dari fakta yang diberikan")
    else:
        print("Kesimpulan:", ", ".join(hasil))
        print("Alasan:")
        tampil = set()
        for h in hasil:
            print("\n".join("  " + b for b in alasan(h, asal, memori, 0, tampil)))
    print(f"\nCatatan: {kb['batas']}")
    print("\nSumber:")
    for k, v in kb["sumber"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
