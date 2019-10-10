#include <Wire.h>
#include <bluefruit.h>

//analog in
int adcin    = A0;
float mv_per_lsb = 3600.0F/1024.0F; // 10-bit ADC with 3.6V input range

// BLE Service
BLEDis  bledis;
BLEUart bleuart;
BLEBas  blebas;
BLEService flex0s = BLEService(0xABCD);
BLECharacteristic flex0c = BLECharacteristic(0xBEEB);

void setup() {
  analogReference(AR_INTERNAL_3_0);
  analogReadResolution(12);
    Serial.begin(115200);
  while ( !Serial ) delay(10);
   bleSetup();
}

void bleSetup() {
    Bluefruit.begin();
    Bluefruit.setTxPower(4);
    Bluefruit.setName("flex0");
    Bluefruit.setConnectCallback(connect_callback);
    Bluefruit.setDisconnectCallback(disconnect_callback);
    bledis.setManufacturer("agnes cameron");
    bledis.setModel("V2.0");
    bledis.begin();
  // Configure and Start BLE Uart Service
//    setupUUID();
    bleuart.begin();
    Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
    Bluefruit.Advertising.addTxPower();
    Bluefruit.Advertising.addService(bleuart);
//    Serial.print(bleuart);
    Bluefruit.ScanResponse.addName();
    Bluefruit.Advertising.restartOnDisconnect(true);
    Bluefruit.Advertising.setInterval(32, 244);   
    Bluefruit.Advertising.setFastTimeout(30);     
    Bluefruit.Advertising.start(0); 
}

void connect_callback(uint16_t conn_handle) {
  char central_name[32] = { 0 };
  Bluefruit.Gap.getPeerName(conn_handle, central_name, sizeof(central_name));
  Serial.print("Connected to ");
  Serial.println(central_name);
}

int adcvalue;
int id = 0;

void disconnect_callback(uint16_t conn_handle, uint8_t reason) {
  (void) conn_handle;
  (void) reason;
  Serial.println();
  Serial.println("Disconnected");
}

void sendData(){
  int numVals = 2;
  int vals[numVals];
  vals[0] = adcvalue;
  vals[1] = id;  
  int cnt = numVals * sizeof(int) ;
  uint8_t buf[cnt];
  for (int _i=0; _i<numVals; _i++)
    memcpy(&buf[_i*sizeof(int)], &vals[_i], sizeof(int));
  bleuart.write( buf, cnt );
}

void loop() {
  adcvalue = analogRead(adcin);
  sendData();
  delay(100);
}
