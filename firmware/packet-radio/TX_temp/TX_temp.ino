// rf69 demo tx rx.pde
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messageing client
// with the RH_RF69 class. RH_RF69 class does not provide for addressing or
// reliability, so you should only use RH_RF69  if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example rf69_server.
// Demonstrates the use of AES encryption, setting the frequency and modem 
// configuration

#include <Wire.h>
#include <SPI.h>
#include <RH_RF69.h>
#include <Adafruit_ADT7410.h>

/************ Radio Setup ***************/

// Change to 434.0 or other frequency, must match RX's freq!
#define RF69_FREQ 915.0
#define RFM69_CS      8
#define RFM69_INT     7
#define RFM69_RST     4
#define LED           13

// accelerometer setup
Adafruit_ADT7410 tempsensor = Adafruit_ADT7410();

// Singleton instance of the radio driver
RH_RF69 rf69(RFM69_CS, RFM69_INT);

int16_t packetnum = 0;  // packet counter, we increment per xmission
int id = 5;

void setup() 
{
  Serial.begin(115200);
  pinMode(LED, OUTPUT); 
  pinMode(RFM69_RST, OUTPUT);
  digitalWrite(RFM69_RST, LOW);

  Serial.println("RFM69 TX temperature");
  Serial.println();
  
  //set up temp sensor
    if (! tempsensor.begin()) {
      Serial.println("Couldnt find sensor");
      return;
    }
    else {
      Serial.print("in setup temp is:  "); Serial.print(tempsensor.readTempC()); 
    }
  
  if (!rf69.init()) {
    Serial.println("RFM69 radio init failed");
    while (1);
  }
  Serial.println("RFM69 radio init OK!");
  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM (for low power module)
  // No encryption
  if (!rf69.setFrequency(RF69_FREQ)) {
    Serial.println("setFrequency failed");
  
  }

  // If you are using a high power RF69 eg RFM69HW, you *must* set a Tx power with the
  // ishighpowermodule flag set like this:
  rf69.setTxPower(20, true);  // range from 14-20 for power, 2nd arg must be true for 69HCW

  // The encryption key has to be the same as the one in the server
  uint8_t key[] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
  rf69.setEncryptionKey(key);
  
  pinMode(LED, OUTPUT);

  Serial.print("RFM69 radio @");  Serial.print((int)RF69_FREQ);  Serial.println(" MHz");
}

int temp;

void loop() {
  delay(10);  // Wait 0.01 second between transmits, could also 'sleep' here!
  readTemp();

  char radiopacket[10];
  snprintf ( radiopacket, 10, "%d %d", id, temp );
  Serial.print("Sending "); 
  Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
}


void readTemp() {
  float tempFloat = tempsensor.readTempC();
  temp = round(tempFloat*100.00); 
}
