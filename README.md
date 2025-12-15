# portorisbang

📊 Indonesian Stock Screener (Hybrid Value–Momentum)

Sebuah Python-based stock screener untuk saham Indonesia (IDX) yang mengombinasikan fundamental sederhana, momentum, trend, likuiditas, dan volatilitas guna menghasilkan kandidat saham trading terbaik.

Project ini ditujukan untuk retail trader / mahasiswa yang ingin membangun systematic trading approach, bukan sekadar indikator manual.

Fitur Utama : Mengambil data saham otomatis menggunakan Yahoo Finance (yfinance), Screening keras (hard filter) untuk mengeliminasi saham berisiko, Scoring & ranking saham berdasarkan multi-faktor, Mengukur likuiditas berbasis nilai transaksi, bukan volume semata, Kontrol volatilitas menggunakan ATR (Average True Range), Output hasil screening ke file CSV, Visualisasi harga dengan Moving Average

Metodologi Screening
1. Fundamental (Value Check) : Trailing P/E Ratio, Price to Book Value, Dividend Yield (sebagai validasi data)
2. Momentum : Return 3 bulan, Return 6 bulan, Return 12 bulan
3. Trend : Harga vs MA20, Konfirmasi trend dengan MA50
4. Likuiditas : Rata-rata nilai transaksi 20 hari terakhir (Close × Volume)
5. Volatilitas : ATR (14), ATR dalam persentase harga

Kriteria Screening (Hard Filter)

Saham harus memenuhi seluruh syarat berikut:
1. P/E > 0 dan < 40
2. Price to Book < 6
3. Data fundamental & harga tersedia
4. Harga di atas MA20
5. Return 6 bulan > -3%
6. Dividend Yield tersedia (indikasi data valid)
7. Jika satu syarat gagal → saham langsung dieliminasi.

Sistem Scoring
Setelah lolos screening, saham akan diberi skor berdasarkan: Faktor	Keterangan, Momentum	Return 6 bulan (maks. 50%), Trend	Bonus jika Price > MA20 > MA50, Likuiditas	Bonus berdasarkan nilai transaksi, Volatilitas	Bonus jika ATR% berada di rentang sehat (2–8%), Saham kemudian diurutkan dari skor tertinggi.

Output

Terminal

Menampilkan Top 5 saham dengan skor tertinggi, screening_result.csv (hasil lengkap screening & scoring)
Contoh output:

=== TOP TRADING CANDIDATES ===
ticker     score   ret_6m   avg_value_20   atr_pct
BBCA.JK    92.4    18.5     3.2e10         3.1
BMRI.JK    88.7    21.2     2.8e10         4.0

Instalasi 

1. Pastikan Python ≥ 3.9
2. pip install yfinance pandas matplotlib
Cara Menjalankan : python screener.py

Hasil akan otomatis: Ditampilkan di terminal

Disimpan ke screening_result.csv

Catatan Penting :

1. Data fundamental Yahoo Finance tidak selalu lengkap untuk saham Indonesia
2. Project ini BELUM termasuk backtesting
3. Tidak ada manajemen risiko (position sizing, stop loss, exit rule)
4. Cocok untuk candidate selection, bukan auto-trading

Pengembangan Selanjutnya (Roadmap) 
1. Refactor data fetch (single API call per saham)
2. Backtesting historis (PnL, drawdown)
3. Entry & exit rules berbasis ATR
4. Position sizing otomatis
5. Universe seluruh saham IDX (tanpa survivorship bias)
 Daily auto screener

Target Pengguna 
1. Mahasiswa saham enthusiast
2. Retail trader yang ingin naik level
3. Quant-minded investor
4. Personal research & portfolio project

Disclaimer : Project ini bukan rekomendasi investasi.
Segala keputusan trading sepenuhnya menjadi tanggung jawab pengguna.
