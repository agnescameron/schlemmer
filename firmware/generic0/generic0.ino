#include <Wire.h>
#include <bluefruit.h>

// BLE Service
BLEDis  bledis;
BLEUart bleuart;
BLEBas  blebas;
BLEService generic3s = BLEService(0xABCD);
BLECharacteristic generic3c = BLECharacteristic(0xBEEB);


void setup(void) {
  Serial.begin(115200);
  delay(2000);
  Serial.println(sizeof(int));
  Serial.println("Hello!");
  bleSetup();
}

void bleSetup() {
    Bluefruit.begin();
    Bluefruit.setTxPower(4);
    Bluefruit.setName("generic3");
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

void disconnect_callback(uint16_t conn_handle, uint8_t reason) {
  (void) conn_handle;
  (void) reason;
  Serial.println();
  Serial.println("Disconnected");
}

int id = 3;

void sendData(){
  int numVals = 4;
  int vals[numVals];
  vals[0] = 10;
  vals[1] = 20;
  vals[2] = 30;
  vals[3] = id;  
  int cnt = numVals * sizeof(int) ;
  uint8_t buf[cnt];
  for (int _i=0; _i<numVals; _i++)
    memcpy(&buf[_i*sizeof(int)], &vals[_i], sizeof(int));
  bleuart.write( buf, cnt );
}

void loop(void) {
  sendData();
  delay(100);
}
