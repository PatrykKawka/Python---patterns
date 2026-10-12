from sklearn.feature_extraction.text import CountVectorizer

# --- PARAMETRY ---
df = transakcje                # ramka z danymi
kolumna = "tytuł_transakcji"   # kolumna tekstowa
ngram_range = (1, 5)           # zakres długości fraz w słowach
min_wierszy = 10               # min. liczba wierszy z frazą

# 1) Unikalne teksty + krotność jako waga
teksty = df[kolumna].dropna().value_counts()
w = teksty.to_numpy()

# 2) Wektoryzacja unikalnych tekstów
vec = CountVectorizer(
    ngram_range=ngram_range,       # opcjonalny, domyślnie (1, 1)
    token_pattern=r"(?u)\b\w+\b",  # opcjonalny, zachowuje słowa 1-znakowe
    dtype=np.int32,                # opcjonalny, mniej RAM
)
X = vec.fit_transform(teksty.index)  # wymagane: iterowalny zbiór tekstów

# 3) Liczności ważone krotnością (X.T @ w = suma X[i, j] * w[i])
Xb = X.copy()
Xb.data[:] = 1                       # binaryzacja: fraza jest / nie ma

ngrams = pd.DataFrame({
    "fraza": vec.get_feature_names_out(),
    "liczba": X.T @ w,               # łączna liczba wystąpień
    "liczba_wierszy": Xb.T @ w,      # w ilu wierszach występuje
})
ngrams = ngrams[ngrams["liczba_wierszy"] >= min_wierszy].copy()
ngrams["n_slow"] = ngrams["fraza"].str.count(" ") + 1

# 4) Pochłanianie: krótsza fraza jest usuwana, jeśli jej rozszerzenie o 1 słowo (z lewej lub prawej) ma tyle samo wierszy
cnt = ngrams.set_index("fraza")["liczba_wierszy"]
dluzsze = ngrams.loc[ngrams["n_slow"] >= 2, ["fraza", "liczba_wierszy"]].copy()
dluzsze["prefiks"] = dluzsze["fraza"].str.rsplit(" ", n=1).str[0]  # bez ostatniego słowa
dluzsze["sufiks"] = dluzsze["fraza"].str.split(" ", n=1).str[1]    # bez pierwszego słowa

pochloniete = set()
for kol in ("prefiks", "sufiks"):
    rowne = cnt.reindex(dluzsze[kol]).to_numpy() == dluzsze["liczba_wierszy"].to_numpy()
    pochloniete.update(dluzsze.loc[rowne, kol])

ngrams_final = (
    ngrams[~ngrams["fraza"].isin(pochloniete)]
    .sort_values("liczba_wierszy", ascending=False)
    .reset_index(drop=True)
)
ngrams_final
