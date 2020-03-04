#include <SPI.h>

void setup() {
  // initialise serial

  Serial.begin(115200);
  while (!Serial) { delay(1); } // wait until serial console is open, remove if not tethered to computer


}

int id = 0;
int xval, yval, zval;

void randTemp(){
  xval=1000;
  yval=1000;
  zval=1000;
}


void loop() {
  delay(50);  // Wait 0.05 second between transmits, could also 'sleep' here!
  randTemp();

  // put your main code here, to run repeatedly:
  char radiopacket[20];
  snprintf ( radiopacket, 20, "%d %d %d %d", id, xval, yval, zval );
  Serial.println(radiopacket);
}
