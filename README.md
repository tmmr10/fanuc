# Fanuc Gestensteuerung

## Beschreibung
Ziel dieses Projekts ist es einen `Fanuc M-1iA` Roboter mittels Gesten steuern zu können. Dafür wird mittels eines Python Programms die Position des Zeigefingers erkannt, in Roboterkoordinaten umgerechnet und an den Roboter über das Netzwerk (Socket) gesendet. Dieser schreibt die erhaltenen Positionen in ein Positionsregister und ließt daraus regelmäßig um seine Position dementsprechend anzupassen. Zudem wird die gesendete Position auf mögliche Positionskonflikte geprüft.

## Installation
1. Auf dem Fanuc:
    1. Kompilieren der Fanuc Programme `gesture.kl` und `gesture_mover.ls`
       > Dafür wird der Compiler von Roboguide benötigt
       >
       > Im Labor ist dies der Windows 7 Rechner (PW `cunaf`)
       >
       > Dort befindet sich auf dem Desktop `C:\Users\fanuc\Desktop\KarelCompiler` mit dem Karel-Compiler `ktrans.exe` und dem TP-Compiler `maketp.exe`
       > (`i:` ist im folgenden der verwendete USB-Stick)
       > ```sh
       > ktrans.exe i:gesture.kl i:gesture.pc
       > maketp.exe i:gesture_mover.ls i:gesture_mover.tp
    2. Kopieren der kompilierten `gesture.pc` und `gesture_mover.tp` auf einen USB-Stick
    3. Einstecken des USB-Sticks im TeachPendent des Fanucs, folgendes dann am TeachPendant
    4. Anmelden als Administrator
       > `Help` > `Login (F4)` > `Admin` auswählen > `Login (F2)` > Passwort eingeben (000) > `Enter` 
    5. Auswählen des USB-Sticks
       > `Menu` > `File (7)` > `Util (F5)` > `Set Device` > `1 USB ON TP (UT1:)`
    6. Kopieren der Programme
       > `7 *PC (all Karel p-code)` bzw. `8 *TP (all TP programs)` > Eintrag / Datei auswählen > `Next` > `Copy (F2)` > `To Device:` `Choice (F4)` > `6 Mem Device (MD:)` > `Do Copy (F1)` > (Overwrite: `Yes (F4)`)
    7. Starten der Programme
       > ...
    8. Identifizieren der Ip Adresse
2. Auf dem Rechner
   1. Kamera / Webcam verbinden
   2. `Python3 <= v11` installieren
   3. `pip install -r requirements/requirements.txt` (oder `requirements.in`)
   4. Eintragen der Roboter IP in `HOST_ADDR` (`main.py`)

## Usage
Zum Starten des Programms muss zuerst der `GESTURE_MOVER` auf dem Fanuc gestartet werden. Im Anschluss kann sich ein Client mittels des `main.py` python scripts verbinden und ein Fenster mit der verwendeten Kamera öffnet sich.

Um den Roboter zu bewegen, muss eine Hand im Bild erkannt werden und der Zeigefinger ausgestreckt werden. Die Spitze des Fingers dient dann zur Übersetzung der Position.

Um den Roboter in die definierte Home-Position fahren zu lassen, müssen beide Fäuste (Handrücken zur Kamera) ins Bild gehalten werden.

## Konfiguration
### `main.py`
Eintragung der Roboter IP: `HOST_ADDR`.

Definition der Home-Position: `HOME_POSITION`

Definition der Limits des Roboters (zur Übersetzung von Pixel- zu Roboterkoordinaten): `TARGET_(X|Z|Y)_(MIN|MAX)`

Randbereich im Bild in px: `MARGIN`

### `gesture.kl`


## Authors and acknowledgment
*Oliver Sedlbauer*

*Tom Maier*

*Janis Reinelt*

Betreuung und Beratung: *M.Sc. Thomas Franzke*

## Projekt Status
Bei dem Projekt handelt es sich um einen POC.

Derzeit ist nur die Gestenerkennung auf Bildebene implementiert. Eine dreidimensionale Erkennung ist ebenso möglich und die Basis dafür ist bereits gegeben. Allerdings wurde der z_Value auf einen fixen Wert gesetzt.

Eine Weiterentwicklung kann dennoch durch nachfolgende Projekte gegeben sein.
