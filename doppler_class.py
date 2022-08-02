import serial
import csv
from datetime import datetime

class Doppler:
  def __init__(self) -> None:
    self.ser = serial.Serial(
      port = '/dev/ttyACM0',
      baudrate = 9600,
      parity = serial.PARITY_NONE,
      stopbits = serial.STOPBITS_ONE,
      bytesize = serial.EIGHTBITS,
      timeout = 1,
      writeTimeout = 2
    )
    self.speed_units = 'US'
    self.direction_control = 'Od'
    self.sampling_freq = 'SC'
    self.tx_power = 'PX'
    self.threshold = 'QI'
    self.module_info = '??'
    self.data_accuracy = 'F1'
    self.display_max_speed_time = 1
    self.reset_speed_time = 5
    self.sendSerCmd("\nSet Speed Output Units: ", self.speed_units)
    self.sendSerCmd("\nSet Direction Control: ", self.direction_control)
    self.sendSerCmd("\nSet Sampling Frequency: ", self.sampling_freq)
    self.sendSerCmd("\nSet Transmit Power: ", self.tx_power)
    self.sendSerCmd("\nSet Threshold Control: ", self.threshold)
    self.sendSerCmd("\nSet Data Accuracy: ", self.data_accuracy)
    self.sendSerCmd("\nModule Information: ", self.module_info)
    
  def sendSerCmd(self, descrStr, commandStr) :
    data_for_send_str = commandStr
    data_for_send_bytes = str.encode(data_for_send_str)
    # print(descrStr, commandStr)
    self.ser.write(data_for_send_bytes)
    # Initialize message verify checking
    ser_message_start = '{'
    ser_write_verify = False
    # Print out module response to command string
    while not ser_write_verify :
        data_rx_bytes = self.ser.readline()
        data_rx_length = len(data_rx_bytes)
        if (data_rx_length != 0) :
            data_rx_str = str(data_rx_bytes)
            if data_rx_str.find(ser_message_start) :
                print(data_rx_str)
                ser_write_verify = True
                
  def write_speed_to_file(self, speed):
    with open('/home/pi/doppler/speed.csv', 'a+') as f:
      writer = csv.writer(f)
      writer.writerow([speed, datetime.now()])
      # f.write(str(speed) + ', ')
      
  def create_speed_file(self):
    with open('/home/pi/doppler/speed.csv', 'w') as f:
      writer = csv.writer(f)
      writer.writerow(['speed', 'datetime'])
      # f.write('speed, timestamp')
                
  def getSpeed(self) -> float:
    data = self.ser.readline()
    # print(len(data))
    decoded_data = data.decode('utf-8')
    # print('original', decoded_data)
    try:
      negative = decoded_data.split('-')
      # print(negative)
      if len(negative) > 1:
        speed = float(negative[1])
        print(speed * -1)
        self.write_speed_to_file(speed * -1)
      else:
        speed = float(decoded_data)
        print(speed)
        self.write_speed_to_file(speed)
    except Exception as e:
      # print(e)
      pass
                
while __name__ == '__main__':
  doppler = Doppler()
  doppler.create_speed_file()
  while True:
    doppler.getSpeed()
  