#include <SPI.h>
#include <MFRC522.h>
#include "hanguls.h"  // hanguls.h 파일 포함

#define RST_PIN 2

const int SS_PINS[] = { 3, 5, 4, 6, 8, 7, A0, A1, A2 };
MFRC522 rfidReaders[sizeof(SS_PINS) / sizeof(SS_PINS[0])];

String hanguls[sizeof(SS_PINS) / sizeof(SS_PINS[0])];  // 한글 자음을 저장할 배열

void setup() {
  Serial.begin(115200);
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV128);


  for (int i = 0; i < sizeof(SS_PINS) / sizeof(SS_PINS[0]); i++) {
    pinMode(SS_PINS[i], OUTPUT);
    digitalWrite(SS_PINS[i], LOW);

    rfidReaders[i].PCD_Init(SS_PINS[i], RST_PIN);
    delay(50);
    digitalWrite(SS_PINS[i], HIGH);


    delay(50);
  }

  Serial.println("Scan an RFID card on any reader");
}


void readCard(MFRC522& rfid, int ssPin, int readerNum) {
  digitalWrite(ssPin, LOW);
  delay(20);
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    // Serial.print("Reader ");
    // Serial.print(readerNum);
    // Serial.print(" UID tag: ");
    for (byte i = 0; i < rfid.uid.size; i++) {
      // Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
      // Serial.print(rfid.uid.uidByte[i], HEX);
    }

    // 카드에 대응되는 한글 자음 출력
    const char* hangul = getHangulForCard(rfid.uid);
    // Serial.print(" -> ");
    // Serial.println(hangul);

    if (hangul[0] != '\0') {  // 매칭된 한글 자음이 있을 경우
      hanguls[readerNum - 1] = hangul;
    }

    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }
  digitalWrite(ssPin, HIGH);
  delay(20);
}

unsigned long previousMillis = 0;
const long interval = 1000;  // 1초(1000밀리초) 간격


void loop() {

  unsigned long currentMillis = millis();

  // 1초(1000ms) 경과했는지 확인
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    Serial.print("Current Hangul States: ");
    for (int i = 0; i < sizeof(hanguls) / sizeof(hanguls[0]); i++) {
      Serial.print(hanguls[i]);
      //Serial.print(" ");
      Serial.print(",");
    }
    Serial.println();
    // 모든 RFID 리더기 재초기화
    for (int i = 0; i < 9; i++) {
      rfidReaders[i].PCD_Init(SS_PINS[i], RST_PIN);
    }



    for (int i = 0; i < sizeof(hanguls) / sizeof(hanguls[0]); i++) {
      hanguls[i] = " ";  // 공백 문자열로 초기화
    }
  }



  for (int i = 0; i < sizeof(rfidReaders) / sizeof(rfidReaders[0]); i++) {

    //rfidReaders[i].PCD_Init(SS_PINS[i], RST_PIN);
    readCard(rfidReaders[i], SS_PINS[i], i + 1);
    delay(10);  // 리더 간 간섭을 줄이기 위해 딜레이를 추가
  }
}