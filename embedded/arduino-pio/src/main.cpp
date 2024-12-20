#include "serialcmd/Types.hpp"
#include "serialcmd/StreamSerializer.hpp"
#include "serialcmd/Protocol.hpp"

#include <Arduino.h>


namespace cmd {
    using serialcmd::Error;
    using serialcmd::StreamSerializer;

    struct Device;


    /// pinMode<00>({u8, u8}) -> (None, ArduinoError<u8>)
    Error pin_mode(Device &, StreamSerializer &serializer) {
        struct { serialcmd::u8 pin, mode; } data{};
        serializer.read(data);

        pinMode(data.pin, data.mode);

        return Error::ok;
    }

    /// digitalWrite<01>({u8, u8}) -> (None, ArduinoError<u8>)
    Error digital_write(Device &, StreamSerializer &serializer) {
        struct { serialcmd::u8 pin, state; } data{};
        serializer.read(data);

        digitalWrite(data.pin, data.state);

        return Error::ok;
    }

    /// digitalRead<02>(u8) -> (u8, ArduinoError<u8>)
    Error digital_read(Device &, StreamSerializer &serializer) {
        serialcmd::u8 pin;
        serializer.read(pin);

        serialcmd::u8 ret;
        ret = digitalRead(pin);

        serializer.write(ret);

        return Error::ok;
    }

    /// millis<03>(None) -> (u32, ArduinoError<u8>)
    Error millis(Device &, StreamSerializer &serializer) {
        serialcmd::u32 ret = ::millis();
        serializer.write(ret);

        return Error::ok;
    }

    /// delay<04>(u32) -> (None, ArduinoError<u8>)
    Error delay(Device &, StreamSerializer &serializer) {
        serialcmd::u32 v;
        serializer.read(v);

        ::delay(v);

        return Error::ok;
    }

    typedef Error(*Cmd)(Device &, StreamSerializer &);

    Cmd commands[] = {
        pin_mode,
        digital_write,
        digital_read,
        millis,
        delay
    };
}


serialcmd::Protocol<cmd::Device, uint8_t, uint8_t> protocol(
    cmd::commands,
    4,
    Serial
);

void setup() {
    Serial.begin(115200);
    protocol.begin(0x01);
}

void loop() {
    protocol.pull();
}
