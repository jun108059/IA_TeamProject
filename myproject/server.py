import socketserver, json
import logging
import os
import django
from django.utils import timezone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from searches.models import Search
import time


class IoTRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = self.request.getpeername() # request의 ip address(host, port) return
        logging.info("Client connecting: {}".format(client)) # 받아온 client의 ip address를 출력

        for line in self.rfile:
            # get a request message in JSON and converts into dict
            try:
                request = json.loads(line.decode('utf-8')) # decode the request data from client
            except ValueError as e:
                # reply ERROR response message
                error_msg = '{}: json decoding error'.format(e)
                status = 'ERROR {}'.format(error_msg)
                response = dict(status=status)
                response = json.dumps(response)
                self.wfile.write(response.encode('utf-8') + b'\n')
                self.wfile.flush()
                logging.error(error_msg)
                break
            else:
                status = 'OK'
                logging.debug("{}:{}".format(client, request)) # display request data(produect, distance) on terminal

            # Insert sensor data into DB tables, 데이터를 DB table에 넣는다
            # and retrieve information to control the actuators, 그리고 actuator를 제어하기 위해 정보를 검색
            data = request.get('data')
            if data:  # data exists
                # Search(timedata=timezone.now(), distance=distance).save()
                Search(name='data', state=data).save()

        # reply response message
            response = dict(status=status) # make a dictionary with response data
            #logging.debug(response)  # display response data(status) on terminal
            response_bytes = json.dumps(response) # json 내용 공부해야함
            self.wfile.write(response_bytes.encode('utf-8') + b'\n') # encode the response data to UTF-8
            self.wfile.flush() # empty buffer

        logging.info('Client closing: {}'.format(client))


logging.basicConfig(filename='', level=logging.DEBUG,
                    format = '%(asctime)s:%(levelname)s:%(message)s')

serv_addr = ("", 12003)
with socketserver.ThreadingTCPServer(serv_addr, IoTRequestHandler) as server:
    logging.info('Server starts: {}'.format(serv_addr)) # port 번호가 12003인 서버를 연다고 말해준다
    server.serve_forever()
