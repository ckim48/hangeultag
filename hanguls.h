// hanguls.h
#ifndef HANGULS_H
#define HANGULS_H

#include <MFRC522.h>
#include <Arduino.h>

// UID와 한글 자음을 매칭하는 구조체 정의
struct CardHangul {
  const char* uidString;   // 카드 UID 문자열 
  const char* hangulChar;  // 대응되는 한글 문자
};

// 카드 UID와 한글 자음 매칭 테이블
const CardHangul cardHangulMap[] = {

  { "73 73 B3 28", "ㄱ" },
  { "3B 24 AD 19", "ㄱ" },
  { "3D 9A 59 6B", "ㄱ" },
 //{ "9B 1C 98 19", "ㄱ" },

  { "3D E5 C3 3C", "ㄴ" },
  { "AB 83 C4 19", "ㄴ" },
 // { "C3 46 6A 1D", "ㄴ" },

  { "0D FD D7 6B", "ㄷ" },
  { "E0 31 36 3B", "ㄷ" },
//  { "94 0C B0 A9", "ㄷ" },

  { "DD 1C 67 6B", "ㄹ" },
  { "C4 07 2B FF", "ㄹ" },
//  { "2B 9F DC 19", "ㄹ" },

  { "0D F6 59 6B", "ㅁ" },
  { "C4 A7 D9 B6", "ㅁ" },
 // { "9B 97 02 1A", "ㅁ" },

  { "10 53 05 3C", "ㅂ" },
  { "10 53 05 3C", "ㅂ" },
  { "DB 88 20 1A", "ㅂ" },
  { "C5 1C 4E FC", "ㅂ" },
 // { "35 04 75 FC", "ㅂ" },

  { "05 DC 77 FC", "ㅅ" },
  { "0B F8 D7 19", "ㅅ" },
//  { "10 13 7E 3B", "ㅅ" },

  { "10 82 2D 3B", "ㅇ" },
  { "83 FF 05 29", "ㅇ" },
  { "E3 E1 78 29", "ㅇ" },
 // { "AD 7B CE 3C", "ㅇ" },

  { "53 12 88 1D", "ㅈ" },
  { "44 9C 6E FE", "ㅈ" },
 // { "40 71 41 3B", "ㅈ" },

  { "13 FF CA 1D", "ㅊ" },
 // { "23 1B 25 1D", "ㅊ" },

  { "14 52 B6 A9", "ㅋ" },
  { "14 73 F0 FE", "ㅋ" },
//  { "2D E6 8D 3C", "ㅋ" },

  { "B7 BB 5E B5", "ㅌ" },
  { "90 B4 31 3B", "ㅌ" },
//  { "0D BC 96 6B", "ㅌ" },

  { "14 41 65 A9", "ㅍ" },
  { "3D 4C 48 6B", "ㅍ" },
//  { "0D 08 4F 6B", "ㅍ" },

  { "A3 90 CF 1D", "ㅎ" },
 // { "1B 24 9D 19", "ㅎ" },

  { "2B 9B BF 19", "ㄲ" },
//  { "14 4D 6B CE", "ㄲ" },

  { "D0 D2 B4 3B", "ㄸ" },
//  { "AB E2 17 1A", "ㄸ" },

  { "B0 7F 9A 3B", "ㅃ" },
//  { "DD 92 55 6B", "ㅃ" },

  { "13 08 DE 1C", "ㅆ" },
//  { "07 94 93 B5", "ㅆ" },
  
  { "C4 CF 86 FA", "ㅉ" },
//  { "C4 CF 71 FA", "ㅉ" },

  { "44 6B 95 A9", "ㄺ" },
//  { "CD C6 A0 6B", "ㄺ" },

  { "47 11 22 19", "ㄼ" },
//  { "C4 B4 D9 FF", "ㄼ" },

  { "90 9F 94 3B", "ㅏ" },
  { "50 4D C7 3B", "ㅏ" },
 // { "B7 8B 96 B5", "ㅏ" },

  { "0B 18 02 1A", "ㅐ" },
  { "C4 5E 7C A9", "ㅔ" },
//  { "0D A4 CD 3C", "ㅐ" },

  { "24 3C 92 FA", "ㅒ" },
//  { "04 9A BB FA", "ㅒ" },

  { "CB D2 00 1A", "ㅑ" },
  { "33 F0 C3 1D", "ㅑ" },

  { "B7 B5 D8 B4", "ㅓ" },
  { "1D 4D F6 3C", "ㅓ" },
//  { "AB 79 1D 1A", "ㅓ" },

  { "C0 31 C6 3B", "ㅔ" },
 // { "44 36 12 A9", "ㅔ" },

  { "E4 49 68 CE", "ㅕ" },
 // { "34 25 B3 A9", "ㅕ" },

  { "BD A4 D2 3C", "ㅖ" },
//  { "D3 AA 2B 1D", "ㅖ" },

  { "0B A6 E5 19", "ㅗ" },
  { "4D 0E 4A 6B", "ㅗ" },
 // { "1D 94 80 6B", "ㅗ" },

  { "9D 55 64 6B", "ㅘ" },
  { "24 CB 7F FA", "ㅘ" },
 // { "8A B6 B6 CE", "ㅘ" },

  { "24 35 DF B6", "ㅙ" },
//  { "14 88 41 A9", "ㅙ" },

  { "24 71 82 FA", "ㅚ" },
//  { "13 5A 8D 1D", "ㅚ" },

  { "D4 2C 4D FE", "ㅛ" },
 // { "D4 C3 DF FA", "ㅛ" },

  { "B4 59 E0 FA", "ㅜ" },
  { "94 D0 9F FE", "ㅜ" },
 // { "F4 BA 62 FA", "ㅜ" },

  { "13 30 C3 1C", "ㅝ" },
//  { "B4 54 6E FA", "ㅝ" },

  { "1D 97 F0 6B", "ㅟ" },
 // { "B4 8B 85 FA", "ㅟ" },

  { "14 7D 6F FA", "ㅠ" },
 // { "B4 51 FB 7F", "ㅠ" },

  { "64 1A BD FA", "ㅡ" },
 // { "34 1C B7 FA", "ㅡ" },

  { "74 A5 89 FA", "ㅢ" },
 // { "B4 BD B9 FA", "ㅢ" },

  { "04 7D 79 FA", "ㅣ" },
  { "74 EE 69 FA", "ㅣ" },
//  { "E4 35 B1 FA", "ㅣ" },









  // 더 많은 UID와 한글 자음을 추가할 수 있습니다
};

// UID를 문자열로 변환하여 비교하는 함수
String uidToString(const MFRC522::Uid& uid) {
  String uidStr = "";
  
  for (byte i = 0; i < uid.size; i++) {
    if (uid.uidByte[i] < 0x10) uidStr += "0";
    uidStr += String(uid.uidByte[i], HEX);
    if (i < uid.size - 1) uidStr += " ";
  }
  return uidStr;
}

// UID에 해당하는 한글 자음을 찾는 함수
const char* getHangulForCard(const MFRC522::Uid& uid) {
  String uidStr = uidToString(uid);
  for (int i = 0; i < sizeof(cardHangulMap) / sizeof(cardHangulMap[0]); i++) {
    if (uidStr.equalsIgnoreCase(cardHangulMap[i].uidString)) {
      return cardHangulMap[i].hangulChar;
    }
  }
  return "?";  // UID가 매칭되지 않을 경우
}

#endif