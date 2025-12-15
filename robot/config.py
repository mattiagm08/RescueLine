
# ===============================
# CONFIGURAZIONE ROBOT (ESP32)
# ===============================

# ===== LINE FOLLOW =====
lineThreshold = 500          # soglia sensore linea
lineLostTimeoutMs = 300     # tempo massimo linea persa in ms

# ===== PID MOTORI =====
pidKp = 1.3                 # guadagno proporzionale
pidKi = 0.0                 # guadagno integrale
pidKd = 0.08                # guadagno derivativo
pidMax = 255                # massimo valore PID

# ===== MOTORI =====
baseSpeed = 120             # velocità normale motori
turnSpeed = 90              # velocità curve o aggiustamenti

# ===== OSTACOLI =====
obstacleDistanceMm = 80     # distanza minima per considerare ostacolo
obstacleClearTimeMs = 400   # tempo per confermare ostacolo passato

# ===== INTERSEZIONI =====
intersectionBlackCount = 5  # numero sensori neri per confermare incrocio
intersectionConfirmMs = 100 # tempo conferma incrocio

# ===== RESCUE ZONE =====
whiteAreaThreshold = 900     # soglia zona bianca
rescueSearchTimeMs = 3000   # tempo massimo ricerca oggetto
servoDropAngle = 120        # angolo servo per rilascio
servoRestAngle = 30         # angolo servo a riposo

# ===== LOOP =====
loopFrequencyHz = 500        # frequenza loop principale robot

# ===== UART (verso Raspberry Pi) =====
uartTxPin = 17               # pin TX ESP32
uartRxPin = 16               # pin RX ESP32
uartBaudrate = 115200        # velocità comunicazione UART
