import re

KEYWORDS = {
    "carbs_g": ["탄수화물", "탄수"],
    "fat_g": ["지방"],
    "protein_g": ["단백질", "단백"],
}

def normalize(text: str) -> str:
    return (
        text.lower()
        .replace("o", "0")
        .replace("i", "1")
        .replace("l", "1")
        .replace("|", "1")
        .replace("!", "1")
        .replace(",", ".")
        .replace(" ", "")
    )

def extract_number(text: str):
    m = re.search(r"(\d+(?:\.\d+)?)", text)
    return float(m.group(1)) if m else None

def looks_like_kcal(token: str) -> bool:
    return bool(re.search(r"kca[l1!]{0,2}$", token))

def has_g_percent(token: str) -> bool:
    return "g" in token and "%" in token


def extract_nutrition(lines: list[str]) -> dict:
    print("\n=== OCR RAW LINES ===")
    for i, l in enumerate(lines):
        print(i, l)

    norm = [normalize(l) for l in lines]

    print("\n=== NORMALIZED LINES ===")
    for i, l in enumerate(norm):
        print(i, l)

    result = {
        "calories_kcal": None,
        "carbs_g": None,
        "protein_g": None,
        "fat_g": None,
    }

    # 1) kcal (숫자 + kcal)
    for i in range(len(norm) - 1):
        num = extract_number(norm[i])
        if num is None:
            continue

        if looks_like_kcal(norm[i + 1]) and 10 < num < 1200:
            result["calories_kcal"] = round(num, 1)
            print(f"✔ calories_kcal = {num}")
            break

    # 2) carbs / fat / protein (키워드 + g%)
    for i, t in enumerate(norm):
        for key, kws in KEYWORDS.items():
            if result[key] is not None:
                continue

            if any(k in t for k in kws):
                print(f"\n[{key} 키워드 발견] line {i}: {t}")
                for j in range(1, 4):
                    if i + j >= len(norm):
                        break
                    cand = norm[i + j]
                    if has_g_percent(cand):
                        v = extract_number(cand)
                        if v is not None:
                            result[key] = round(v, 1)
                            print(f"✔ {key} = {v}")
                            break

    # 3) protein fallback (관계 기반)
    if result["protein_g"] is None:
        g_vals = []
        for t in norm:
            if has_g_percent(t):
                v = extract_number(t)
                if v:
                    g_vals.append(v)

        print("\n[g 후보]", g_vals)

        kcal = result["calories_kcal"]
        carbs = result["carbs_g"]
        fat = result["fat_g"]

        for v in reversed(g_vals):
            # 이미 사용된 값 제외
            if v in (carbs, fat):
                continue

            # kcal 물리 조건
            if kcal:
                if v * 4 > kcal:
                    continue

            result["protein_g"] = round(v, 1)
            print(f"✔ protein_g (fallback) = {v}")
            break

    print("\n=== FINAL RESULT ===")
    print(result)
    return result
