#include "serialcmd/Types.hpp"
#include "serialcmd/StreamSerializer.hpp"
#include "serialcmd/Protocol.hpp"

#include <Arduino.h>


namespace cmd {
    using serialcmd::StreamSerializer;

    enum Error : char {
        ok = 0x00,
        fail = 0x01
    };

    /// pinMode<00>({u8, u8}) -> (None, ArduinoError<u8>)
    void pin_mode(StreamSerializer &serializer) {
        struct { serialcmd::u8 pin, mode; } data{};
        serializer.read(data);

        pinMode(data.pin, data.mode);

        serializer.write(Error::ok);
    }

    /// digitalWrite<01>({u8, u8}) -> (None, ArduinoError<u8>)
    void digital_write(StreamSerializer &serializer) {
        struct { serialcmd::u8 pin, state; } data{};
        serializer.read(data);

        digitalWrite(data.pin, data.state);

        serializer.write(Error::ok);
    }

    /// digitalRead<02>(u8) -> (u8, ArduinoError<u8>)
    void digital_read(StreamSerializer &serializer) {
        serialcmd::u8 pin;
        serializer.read(pin);

        serializer.write(Error::ok);

        serialcmd::u8 ret = digitalRead(pin);
        serializer.write(ret);
    }

    /// millis<03>(None) -> (u32, ArduinoError<u8>)
    void millis(StreamSerializer &serializer) {
        serialcmd::u32 ret = ::millis();

        serializer.write(Error::ok);
        serializer.write(ret);
    }

    /// delay<04>(u32) -> (None, ArduinoError<u8>)
    void delay(StreamSerializer &serializer) {
        serialcmd::u32 v;
        serializer.read(v);

        ::delay(v);

        serializer.write(Error::ok);
    }

    typedef void(*Cmd)(StreamSerializer &);

    Cmd commands[] = {
        pin_mode,
        digital_write,
        digital_read,
        millis,
        delay
    };
}


serialcmd::Protocol<uint8_t, uint8_t> protocol(cmd::commands, 5, Serial);

void setup() {
    Serial.begin(115200);
    protocol.begin(0x01);
}

void loop() {
    protocol.pull();
}
