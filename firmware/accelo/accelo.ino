#include <Wire.h>
#include <Adafruit_LIS3DH.h>
#include <bluefruit.h>

// BLE Service
BLEDis  bledis;
BLEUart bleuart;
BLEBas  blebas;
BLEService acceloS = BLEService(0xABCD);
BLECharacteristic acceloC = BLECharacteristic(0xBEEB);

Adafruit_LIS3DH lis = Adafruit_LIS3DH();


void setup(void) {
  Serial.begin(115200);
  delay(2000);
  Serial.println(sizeof(int));
  Serial.println("Hello!");
  bleSetup();
  
  if (! lis.begin()) {
    Serial.println("Couldnt find sensor");
    return;
  }
  else {
    lis.read();
    Serial.print("X:  "); Serial.print(lis.x); 
    Serial.print("  \tY:  "); Serial.print(lis.y); 
    Serial.print("  \tZ:  "); Serial.print(lis.z); 
  }
}

int id = 5;

void bleSetup() {
    Bluefruit.begin();
    Bluefruit.setTxPower(4);
    Bluefruit.setName("accelo5");
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

int xval, yval, zval;

void sendData(){
  int numVals = 4;
  int vals[numVals];
  vals[0] = abs(xval);
  vals[1] = abs(yval);
  vals[2] = abs(zval);
  vals[3] = id;  
  int cnt = numVals * sizeof(int) ;
  uint8_t buf[cnt];
  for (int _i=0; _i<numVals; _i++)
    memcpy(&buf[_i*sizeof(int)], &vals[_i], sizeof(int));
  bleuart.write( buf, cnt );
}

void loop(void) {
  lis.read();
  Serial.print("X:  "); Serial.print(lis.x); 
  Serial.print("  \tY:  "); Serial.print(lis.y); 
  Serial.print("  \tZ:  "); Serial.print(lis.z); 
  Serial.print("  \tid:  "); Serial.print(id);   
  Serial.println("");
  // get X Y and Z data at once
  xval = lis.x;
  yval = lis.y;
  zval = lis.z;
  sendData();
  delay(100);
}
