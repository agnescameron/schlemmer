#include <Wire.h>
#include <Adafruit_ADT7410.h>
#include <bluefruit.h>

// BLE Service
BLEDis  bledis;
BLEUart bleuart;
BLEBas  blebas;
BLEService tempS = BLEService(0xABCD);
BLECharacteristic tempC = BLECharacteristic(0xBEEB);
Adafruit_ADT7410 tempsensor = Adafruit_ADT7410();

void setup(void) {
  Serial.begin(115200);
  delay(2000);
  Serial.println("Hello!");
  Serial.println(sizeof(float));
  bleSetup();

  if (! tempsensor.begin()) {
    Serial.println("Couldnt find sensor");
    return;
  }
  else {
    Serial.print("temp:  "); Serial.print(tempsensor.readTempC()); 
  }

}

int id = 2;

void bleSetup() {
    Bluefruit.begin();
    Bluefruit.setTxPower(4);
    Bluefruit.setName("temp2");
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

int temp;

void sendData(){
  int numVals = 2;
  int vals[numVals];
  vals[0] = temp;
  vals[1] = id;
  Serial.println(temp);
  Serial.println(id);  
  int cnt = numVals * sizeof(int) ;
  uint8_t buf[cnt];
  for (int _i=0; _i<numVals; _i++)
    memcpy(&buf[_i*sizeof(int)], &vals[_i], sizeof(int));
  bleuart.write( buf, cnt );
}

void loop(void) {
  float tempFloat = tempsensor.readTempC();
  temp = round(tempFloat*100.00);
  sendData();
  delay(100);
}
