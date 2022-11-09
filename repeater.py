import digitalio
import board
import busio
import adafruit_rfm9x

RADIO_FREQ_MHZ = 925.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio with a more conservative baudrate
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

rfm9x.tx_power = 23




while True:
    packet = None
    # draw a box to clear the image

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        print("Waiting...")
    else:
        # Display the packet text and rssi
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        if packet_text == "TESTUW":
            data = bytes("UAV", "utf-8")
            rfm9x.send(data)
            print("Received Key")
        
