import serial

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
    self.sampling_freq = 'S2'
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
    print(descrStr, commandStr)
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
                # print(data_rx_str)
                ser_write_verify = True
                
  def getSpeed(self) -> float:
    data = self.ser.readline()
    # print(len(data))
    data = data.decode('utf-8')
    if "-" in data:
      neg = data.replace("-", "")
      print(print('-', float(neg)))
    elif data.isnumeric():
      print(float(data))
                
while __name__ == '__main__':
  doppler = Doppler()
  while True:
    doppler.getSpeed()
  