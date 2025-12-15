# ===============================
# BOARD ESP32 + COMUNICAZIONE UART
# ===============================
from machine import Pin, PWM, UART # type: ignore
from config import uartTxPin, uartRxPin, uartBaudrate

class Board:
    def __init__(self):
        # ===== MOTORI =====
        self.motorLeftPin = 5                         # pin motore sinistro
        self.motorRightPin = 6                        # pin motore destro
        self.motorLeftPwm = PWM(Pin(self.motorLeftPin))   # oggetto PWM sinistro
        self.motorRightPwm = PWM(Pin(self.motorRightPin)) # oggetto PWM destro
        self.motorLeftPwm.freq(1000)                  # frequenza PWM sinistro
        self.motorRightPwm.freq(1000)                 # frequenza PWM destro
        self.motorLeftSpeed = 0                        # velocità iniziale sinistro
        self.motorRightSpeed = 0                       # velocità iniziale destro

        # ===== SERVO =====
        self.servoPin = 9                               # pin servo braccio
        self.servoPwm = PWM(Pin(self.servoPin))        # oggetto PWM servo
        self.servoPwm.freq(50)                         # frequenza standard servo
        self.servoAngle = 0                             # angolo iniziale

        # ===== SENSORI =====
        self.lineSensorPins = [2, 3, 4]               # pin sensori linea

        # ===== UART verso Raspberry Pi =====
        self.uart = UART(1, baudrate=uartBaudrate, tx=Pin(uartTxPin), rx=Pin(uartRxPin))  # oggetto UART

    # ===== FUNZIONI BASE =====
    def initBoard(self):
        self.stopMotors()                             # motori fermi
        self.setServoAngle(0)                         # servo a riposo
        print("Board inizializzata, motori fermi, servo a riposo") # messaggio debug

    def stopMotors(self):
        self.motorLeftPwm.duty(0)                     # ferma motore sinistro
        self.motorRightPwm.duty(0)                    # ferma motore destro
        self.motorLeftSpeed = 0                        # aggiorna stato interno
        self.motorRightSpeed = 0                       # aggiorna stato interno

    def setServoAngle(self, angle):
        duty = int((angle / 180) * 1023)             # mappa 0-180° a PWM 0-1023
        self.servoPwm.duty(duty)                      # aggiorna PWM servo
        self.servoAngle = angle                        # aggiorna stato interno

    # ===== COMUNICAZIONE =====
    def sendToPi(self, message):
        self.uart.write(message + "\n")              # invia stringa al Pi

    def receiveFromPi(self):
        if self.uart.any():                           # se ci sono dati disponibili
            return self.uart.readline().decode('utf-8').strip()  # decodifica e rimuove spazi
        return None                                   # nessun dato
