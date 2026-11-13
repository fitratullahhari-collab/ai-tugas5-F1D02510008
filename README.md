# Tugas 5 — Sistem Pakar Sederhana: Kesiapsiagaan Banjir dan Banjir Bandang

**Nama:** Hari Fitratullah
**NIM:** F1D02510008

## 1. Topik dan cara menjalankan

Topik: penilaian awal tanda bahaya banjir bandang dan tindakan yang disarankan saat banjir.

- Bahasa: Python 3.x (library bawaan saja: `json`, `argparse`, `sys`)
- Mode tanya-jawab: `python sistem_pakar.py`
- Mode langsung (fakta "ya" lewat argumen, boleh diulang):
  `python sistem_pakar.py --fakta "air sungai keruh" --fakta "muka air sungai tiba-tiba surut"`

## 2. Sumber dan tabel aturan

| Kode | Judul | Penerbit | URL | Diakses |
| ---- | ----- | -------- | --- | ------- |
| S1 | Siaga Bencana Banjir (buku *Tanggap Tangkas Tangguh Menghadapi Bencana*) | BNPB, diunggah di PPID KKP | https://ppid.kkp.go.id/media/uploads/document_information_public/4._Siaga_Bencana_Banjir.pdf | 13 Nov 2026 |
| S2 | Karakterisasi Bencana Banjir Bandang di Indonesia (Seno Adi) | Jurnal Sains dan Teknologi Indonesia Vol. 15 No. 1, 2013, BPPT | https://media.neliti.com/media/publications/130039-ID-karakterisasi-bencana-banjir-bandang-di.pdf | 13 Nov 2026 |

| Aturan | IF | THEN | Sumber |
| ------ | -- | ---- | ------ |
| R1 | air sungai keruh **AND** muka air sungai tiba-tiba surut | aliran sungai di hulu terbendung | S2 |
| R2 | aliran sungai di hulu terbendung **OR** suara gemuruh dari arah hulu | tanda bahaya banjir bandang | S2 |
| R3 | tanda bahaya banjir bandang **OR** air banjir mulai naik di sekitar saya | **evakuasi segera ke tempat yang lebih tinggi** | S1 |
| R4 | sedang mengemudi di jalan tergenang **AND** air banjir mulai naik | **tinggalkan mobil, menuju tempat lebih tinggi** | S1 |
| R5 | berdiri di dalam air banjir **AND** peralatan listrik masih tersambung | **bahaya tersengat listrik, jangan sentuh peralatan listrik** | S1 |

Tiga kesimpulan akhir (tebal). Program menanyakan 7 fakta. Rantai terpanjang: R1 → R2 → R3.

## 3. Metode: Forward Chaining

Dipilih karena user mengamati tanda di lapangan (fakta) lalu perlu tahu tindakan yang disarankan, jadi penalaran bergerak dari fakta ke kesimpulan.

Langkah: (1) memori diisi fakta yang dijawab "ya"; (2) cari aturan yang syaratnya terpenuhi dan hasilnya belum ada di memori; (3) jalankan aturan pertama yang cocok, tambahkan hasilnya ke memori, catat asalnya; (4) ulangi sampai tidak ada aturan baru; (5) kesimpulan = hasil yang tidak dipakai sebagai syarat aturan lain; alasan ditelusuri mundur dari catatan asal.

## 4. Kasus uji

| # | Jawaban "ya" | Kesimpulan | Screenshot |
| - | ------------ | ---------- | ---------- |
| 1 | air sungai keruh, muka air sungai tiba-tiba surut | evakuasi segera ke tempat yang lebih tinggi | ![kasus 1](screenshot/kasus1.png) |
| 2 | sedang mengemudi di jalan tergenang, air banjir mulai naik | evakuasi segera + tinggalkan mobil | ![kasus 2](screenshot/kasus2.png) |
| 3 | air sungai keruh saja | **tidak ada** (kasus negatif) | ![kasus 3](screenshot/kasus3.png) |

## 5. Batas keberlakuan

Pengetahuan dalam program ini berasal dari dua sumber: buku panduan BNPB dan satu artikel jurnal BPPT (2013) yang merangkum tanda banjir bandang di Jember. Aturan hanya mencakup beberapa tanda banjir bandang dan tindakan dasar saat banjir, serta tidak mewakili semua kondisi daerah; tanda di lapangan sangat bergantung pada kondisi lokal. Hasilnya adalah saran awal, bukan keputusan akhir. Selalu ikuti informasi resmi BPBD, BNPB, atau BMKG dan perintah petugas. Catatan ini juga ditampilkan oleh program.

## 6. Penggunaan alat bantu AI

Saya memakai Claude untuk mencari sumber dan membuat kerangka kode. Saya sudah membaca kedua sumber, memeriksa tiap aturan, dan menjalankan serta memahami kodenya."
