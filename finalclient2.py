from socket import *
import threading
import json, time, sys, os
import selectors2 as selectors
import logging, serial
import RPi.GPIO as GPIO

TRIG = 20
ECHO = 21
BUZZER = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

def sen_data():
    while True:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            startTime = time.time()

        while GPIO.input(ECHO) == 1:
            stopTime = time.time()

        travel = stopTime - startTime

        distance = float((travel * 34300) / 2)

        dist = float(distance)
        if dist<20:
            serialFromArduino2.write('1')
        else:
            serialFromArduino2.write('0')


        rfid = serialFromArduino.readline()
        rfid = float(rfid)
        if rfid < 5:
            GPIO.output(BUZZER,True)
            time.sleep(0.2)
            GPIO.output(BUZZER,False)
            if rfid == 1:
                sended = 'Apple'
                yield sended
            elif rfid == 2:
                sended = 'Banana'
                yield sended
            elif rfid == 3:
                sended = 'Onion'
                yield sended
            elif rfid == 4:
                sended = 'Garlic'
                yield sended
            elif rfid ==5:
                pass

class IoTClient:
    def __init__(self, server_addr):
        """IoT client with persistent connection
        Each message separated by b'\n'
        """
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(server_addr)  # connect to server process
        rfile = sock.makefile('rb')  # file-like obj
        sel = selectors.DefaultSelector()
        sel.register(sock, selectors.EVENT_READ)

        self.sock = sock
        self.rfile = rfile
        self.sel = sel
        self.requests = {}      # messages sent but not yet received their responses
        self.time_to_expire = None

    def select_periodic(self, interval):
        """Wait for ready events or time interval.
        Timeout event([]) occurs every interval, periodically.
        """
        now = time.time()
        if self.time_to_expire is None:
            self.time_to_expire = now + interval
        timeout_left = self.time_to_expire - now
        if timeout_left > 0:
            events = self.sel.select(timeout=timeout_left)
            if events:
                return events
        # time to expire elapsed or timeout event occurs
        self.time_to_expire += interval # set next time to expire
        return []

    def run(self):
        # Report sensors' data forever
        my_data = sen_data()
        while True:
            try:
                events = self.select_periodic(interval=0.1)
                if not events: # timeout occurs
                    try: # keep receiving data by while loop
                        data = next(my_data)
                    except StopIteration:
                        logging.info('No more sensor data to send')
                        break
                    request = dict(data=data) # make a dictionary with request data
                    logging.debug(request) # display the request data(rfid, distance) on terminal
                    request_bytes = json.dumps(request).encode('utf-8') + b'\n' # encode the request data to UTF-8
                    self.sock.sendall(request_bytes) # send the encoded data to server
                else:               # EVENT_READ
                    response_bytes = self.rfile.readline()      # receive response
                    if not response_bytes: # if the server doesn't send responses
                        self.sock.close()
                        raise OSError('Server abnormally terminated')
                    response = json.loads(response_bytes.decode('utf-8')) # decode the response data came from server
                    # logging.debug(response) # display the response data on terminal

            except Exception as e:
                logging.error(e)
                break

        logging.info('client terminated')
        self.sock.close()

# settings for arduino-rasp serial connection
serial_port = "/dev/ttyACM0"
serial_port2 ="/dev/ttyUSB0"
serialFromArduino = serial.Serial(serial_port,9600)
serialFromArduino2 = serial.Serial(serial_port2, 9600)
serialFromArduino.flushInput()
serialFromArduino2.flushInput()
if __name__ == '__main__':
    if len(sys.argv) == 2:
        host, port = sys.argv[1].split(':')
        port = int(port)
    else:
        print('Usage: {} host:port'.format(sys.argv[0]))
        sys.exit(1)

    # setting the logging which is displayed on terminal
    logging.basicConfig(level=logging.DEBUG,
                        format = '%(asctime)s:%(levelname)s:%(message)s')

    # making objects with host address & port number
    client = IoTClient((host, port))
    client.run()
GPIO.cleanup()
