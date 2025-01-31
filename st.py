def korean_breakdown(word):
    result = []
    for char in word:
        unicode_val = ord(char) - 44032
        if unicode_val < 0 or unicode_val > 11171:
            result.append(char)
            continue

        cho = unicode_val // 588
        jung = (unicode_val % 588) // 28
        jong = unicode_val % 28

        # Debug: print the internal values
        print(f"Char: {char}, Unicode Value: {unicode_val}, cho: {cho}, jung: {jung}, jong: {jong}")

        cho_list = ["ㅇ", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄸ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㅁ", "ㅂ", "ㅃ", "ㅄ", "ㅅ", "ㅆ", "ㅇ",
                    "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
        jung_list = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ",
                     "ㅣ"]
        jong_list = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄸ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㅁ", "ㅂ", "ㅃ", "ㅄ", "ㅅ", "ㅆ", "ㅈ",
                     "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

        breakdown = [cho_list[cho], jung_list[jung], jong_list[jong]]
        result.extend(breakdown)

    return result


# Testing with '용'
print(korean_breakdown('용'))  # Expected output: ['ㅇ', 'ㅛ', 'ㅇ', '', '', '', '', '', '']
