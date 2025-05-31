import cv2
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

tracker = cv2.TrackerCSRT.create()
cam = cv2.VideoCapture(0)
ret, frame = cam.read()
bbox = (100, 100, 200, 200)
print(bbox)
tracker.init(frame, bbox)
cv2.destroyAllWindows()
while True:
    ret, frame = cam.read()
    ok, bbox = tracker.update(frame)

    if ok:
        x = bbox[0]
        y = bbox[1]
        b = bbox[2]
        d = bbox[3]
        z = int((x+(x+b-x)/2)/640*100)
        c = int((y+(y+d-y)/2)/480*100)
        
        #if z < 10:
		#	print("Гиперправее")
		#	ser.write(b'3')
        if z < 20:
            print("Правее")
            ser.write(b'7')
        #elif z > 90:
		#    ser.write(b'4')
        elif z > 80:
            print("Левее")
            ser.write(b'6')

        else:
            ser.write(b'5')
        if c < 40:
            print("Ниже")
        elif c > 60:
            print("Выше")
        else:
            pass
        print(z, c)
        
        cv2.rectangle(frame, (x, y), (x+b, y+d), (0, 0, 255), thickness=1)
    else:
        cv2.putText(frame, 'Ошибка отслеживания', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
	
    cv2.imshow("да", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        ser.write(b'5')
        break

cam.release()
cv2.destroyAllWindows()

