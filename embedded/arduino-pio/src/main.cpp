#include "serialcmd/StreamBinarySerializer.hpp"
#include <Arduino.h>

serialcmd::StreamBinarySerializer serializer(Serial);

void setup() {
    Serial.begin(115200);

    struct Foo {
        uint32_t a;
        uint16_t b;
        uint8_t c;
    } foo{
        .a = 0xA1A2A3A4,
        .b = 0xB1B2,
        .c = 0x69
    };

    serializer.write(foo);
}

void loop() {}