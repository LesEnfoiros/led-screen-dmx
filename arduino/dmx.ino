#include <Conceptinetics.h>
#include <Wire.h>

//
// The slave device will use a block of 10 channels counting from
// its start address.
//
// If the start address is for example 56, then the channels kept
// by the dmx_slave object is channel 56-66
//
#define DMX_SLAVE_CHANNELS   6

//
// The address of the first channel of the
// device in the DMX network.
//
#define DMX_SLAVE_ADDRESS 490

//
// This is the I2C address to communicate with
// the Raspberry pi card.
//
#define WIRE_SLAVE_ADDRESS 0x08

// Configure a DMX slave controller
DMX_Slave dmx_slave(DMX_SLAVE_CHANNELS) ;

//const int ledPin = 13;

// This is the order received by the Arduino card
// coming from the I2C channel from the Raspberry card.
byte order_received_from_raspberry = 0 ;

// the setup routine runs once when you press reset:
void setup() {
  // Enable DMX slave interface and start recording
  // DMX data.
  dmx_slave.enable() ;

  // Set start address to 1, this is also the default setting
  // You can change this address at any time during the program.
  dmx_slave.setStartAddress(DMX_SLAVE_ADDRESS) ;

  // Initialize the I2C wire sending the data to the
  // Raspberry pi card.
  Wire.begin(WIRE_SLAVE_ADDRESS) ;
  Wire.onReceive(receiveOrderFromRaspberry) ;
  Wire.onRequest(sendDataToRaspberry) ;

  // Set led pin as output pin
  //pinMode(ledPin, OUTPUT) ;
}

// the loop routine runs over and over again forever:
void loop() {
  // getChannelValue is relative to the configured startaddress
  /*if(dmx_slave.getChannelValue(2) > 127) {
    digitalWrite(ledPin, HIGH) ;
    } else {
    digitalWrite(ledPin, LOW) ;
    }*/
}

void receiveOrderFromRaspberry(int bytecount) {
  for (int i = 0; i < bytecount; i++) {
    order_received_from_raspberry = Wire.read() ;
  }
}

void sendDataToRaspberry() {
  //Wire.write(order_received_from_raspberry) ;
  Wire.write(dmx_slave.getChannelValue(order_received_from_raspberry + 1)) ;
}
