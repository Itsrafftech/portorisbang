import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# 1. FUNGSI AMBIL DATA
# =====================================================

def get_fundamental(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    info = t.info

    return {
        "ticker": ticker,
        "name": info.get("shortName"),
        "sector": info.get("sector"),
        "trailingPE": info.get("trailingPE"),
        "priceToBook": info.get("priceToBook"),
        "dividendYield": info.get("dividendYield"),
        "marketCap": info.get("marketCap"),
    }


def get_returns(ticker: str, period: str = "1y") -> dict:
    t = yf.Ticker(ticker)
    hist = t.history(period=period)

    if hist.empty:
        return {"ret_3m": None, "ret_6m": None, "ret_12m": None}

    close = hist["Close"]

    def calc_return(days: int):
        if len(close) < days:
            return None
        start_price = close.iloc[-days]
        end_price = close.iloc[-1]
        if start_price == 0:
            return None
        return (end_price - start_price) / start_price * 100

    return {
        "ret_3m": calc_return(63),
        "ret_6m": calc_return(126),
        "ret_12m": calc_return(252),
    }


def get_trend(ticker: str, period: str = "6mo") -> dict:
    t = yf.Ticker(ticker)
    hist = t.history(period=period)

    if hist.empty:
        return {"last_price": None, "ma20": None, "ma50": None}

    close = hist["Close"]

    return {
        "last_price": close.iloc[-1],
        "ma20": close.rolling(20).mean().iloc[-1],
        "ma50": close.rolling(50).mean().iloc[-1],
    }


def get_liquidity(ticker: str, period: str = "3mo") -> dict:
    t = yf.Ticker(ticker)
    hist = t.history(period=period)

    if hist.empty:
        return {"avg_volume_20": None, "avg_value_20": None}

    hist["value"] = hist["Close"] * hist["Volume"]

    return {
        "avg_volume_20": hist["Volume"].tail(20).mean(),
        "avg_value_20": hist["value"].tail(20).mean(),
    }


def get_atr(ticker: str, period: str = "6mo", window: int = 14) -> dict:
    t = yf.Ticker(ticker)
    hist = t.history(period=period)

    if hist.empty:
        return {"atr": None, "atr_pct": None}

    high, low, close = hist["High"], hist["Low"], hist["Close"]

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(window).mean().iloc[-1]
    atr_pct = atr / close.iloc[-1] * 100

    return {"atr": atr, "atr_pct": atr_pct}


# =====================================================
# 2. SCREENING (FILTER KERAS)
# =====================================================

def safe_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def screen_stock(row: pd.Series,
                 max_pe: float = 40,
                 max_pb: float = 6,
                 min_ret_6m: float = -3) -> bool:

    pe = safe_float(row.get("trailingPE"))
    pb = safe_float(row.get("priceToBook"))
    dy = safe_float(row.get("dividendYield"))
    last_price = safe_float(row.get("last_price"))
    ma20 = safe_float(row.get("ma20"))
    ret_6m = safe_float(row.get("ret_6m"))

    # data wajib ada
    if None in (pe, pb, last_price, ma20, ret_6m):
        return False

    if not (0 < pe < max_pe):
        return False

    if pb > max_pb:
        return False

    if dy is None:
        return False

    if last_price < ma20:
        return False

    if ret_6m <= min_ret_6m:
        return False

    return True



# =====================================================
# 3. SCORING (RANKING)
# =====================================================

def scoring(row: pd.Series) -> float:
    score = 0

    # Momentum
    score += min(row["ret_6m"], 50) * 0.4

    # Trend
    if row["last_price"] > row["ma20"] > row["ma50"]:
        score += 30

    # Liquidity
    if row["avg_value_20"] > 20e9:
        score += 20
    elif row["avg_value_20"] > 10e9:
        score += 10

    # Volatility
    if 2 <= row["atr_pct"] <= 8:
        score += 10

    return score


# =====================================================
# 4. VISUALISASI
# =====================================================

def plot_price_with_ma(ticker: str):
    hist = yf.Ticker(ticker).history(period="6mo")
    if hist.empty:
        return

    close = hist["Close"]
    plt.figure()
    plt.plot(close, label="Close")
    plt.plot(close.rolling(20).mean(), label="MA20")
    plt.plot(close.rolling(50).mean(), label="MA50")
    plt.legend()
    plt.title(ticker)
    plt.show()


# =====================================================
# 5. MAIN
# =====================================================

def main():
    tickers = [
    "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "TLKM.JK", "ASII.JK", "UNVR.JK",
    "ICBP.JK", "INDF.JK", "HMSP.JK", "GGRM.JK", "KLBF.JK", "SIDO.JK", "TSPC.JK",
    "INCO.JK", "ANTM.JK", "MDKA.JK", "ADRO.JK", "PTBA.JK", "ITMG.JK", "BUMI.JK",
    "HRUM.JK", "PGAS.JK", "AKRA.JK", "BRPT.JK", "SMGR.JK", "INTP.JK",
    "CPIN.JK", "JPFA.JK", "MAIN.JK",
    "ERAA.JK", "MAPI.JK", "AMRT.JK", "MIDI.JK", "ACES.JK", "RALS.JK",
    "LPPF.JK", "MAPA.JK",
    "PWON.JK", "CTRA.JK", "BSDE.JK", "SMRA.JK", "PANI.JK", "APLN.JK", "DILD.JK",
    "GOTO.JK", "BUKA.JK",
    "TOWR.JK", "TBIG.JK", "EXCL.JK", "ISAT.JK", "MTEL.JK", "FREN.JK",
    "MEDC.JK", "ELSA.JK", "RAJA.JK",
    "WIKA.JK", "PTPP.JK", "ADHI.JK", "JSMR.JK", "WSKT.JK",
    "BBTN.JK", "BDMN.JK", "MEGA.JK", "PNBN.JK", "BNGA.JK", "NISP.JK",
    "BJBR.JK", "BJTM.JK", "AGRO.JK", "ARTO.JK", "BANK.JK",
    "SRTG.JK", "MPMX.JK", "SMDR.JK", "ASSA.JK", "GIAA.JK", "CMPP.JK",
    "MARK.JK", "WTON.JK",
    "AALI.JK", "LSIP.JK", "SIMP.JK", "TBLA.JK", "SSMS.JK", "DSNG.JK",
    "BWPT.JK", "TAPG.JK",
    "ULTJ.JK", "MYOR.JK", "ROTI.JK", "SKBM.JK", "SKLT.JK",
    "DVLA.JK", "KAEF.JK", "INAF.JK",
    "MIKA.JK", "SILO.JK", "HEAL.JK", "SAME.JK",
    "AUTO.JK", "IMAS.JK", "BIRD.JK",
    "KIJA.JK", "BEST.JK", "DMAS.JK",
    "DOID.JK", "DEWA.JK", "BSSR.JK",
    "CLEO.JK", "CAMP.JK", "GOOD.JK",
    "RICY.JK", "MLBI.JK",
    "WOOD.JK", "INDS.JK",
    "WEGE.JK", "TOTL.JK",
    "PZZA.JK", "FAST.JK",
    "MNCN.JK", "SCMA.JK", "EMTK.JK", "FILM.JK", "VIVA.JK",
    "IPTV.JK", "LINK.JK",
    "KINO.JK", "MBTO.JK",
    "DIGI.JK", "WIFI.JK",
    "TRIM.JK", "YULE.JK",
    "ZONE.JK", "CASH.JK"
]


    rows = []
    for t in tickers:
        data = {}
        data.update(get_fundamental(t))
        data.update(get_returns(t))
        data.update(get_trend(t))
        data.update(get_liquidity(t))
        data.update(get_atr(t))
        if data.get("last_price") is None:
            print(f"Lewati {t} (data harga tidak tersedia)")
            continue

        rows.append(data)

    df = pd.DataFrame(rows)

    df["lulus_screen"] = df.apply(screen_stock, axis=1)
    df = df[df["lulus_screen"]]

    if df.empty:
        print("Tidak ada saham lolos filter.")
        return

    df["score"] = df.apply(scoring, axis=1)
    df = df.sort_values("score", ascending=False)

    print("\n=== TOP TRADING CANDIDATES ===")
    print(df[[
        "ticker", "score", "ret_6m",
        "avg_value_20", "atr_pct"
    ]].head(5))

    df.to_csv("screening_result.csv", index=False)
    print("\nDisimpan ke screening_result.csv")


if __name__ == "__main__":
    main()
