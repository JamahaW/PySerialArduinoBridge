enum Commands : byte {
  PIN_MODE = 0x10,
  DIGITAL_WRITE = 0x11,
  DIGITAL_READ = 0x12,
  DELAY_MS = 0x13,
};



void setup() {
  Serial.begin(9600);
}

void loop() {

}
