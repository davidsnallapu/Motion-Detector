import cv2, time

first_frame=None

video=cv2.VideoCapture(0)
print("Click 'q' to close application.")
while True:
	check,frame = video.read()
	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	gray=cv2.GaussianBlur(gray,(21,21),0)#blurs for accuracy
	if first_frame is None:
		first_frame=gray
		continue

	delta_frame=cv2.absdiff(first_frame,gray)
	thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]#CHecks difference bw first frame and the rest
	thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)#Used to accentuate featues(helps with the white areas)

	(_,cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in cnts:
		if cv2.contourArea(contour) < 10000:
			continue

		(x,y,w,h)=cv2.boundingRect(contour)#Contuor bounded with rectangle if ther's motion
		cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),3)


	#cv2.imshow("Gray frame",gray) #Gray frame better for noisy backgrounds
	#cv2.imshow("Delta Frame", delta_frame) #Compares the first frame to Gray frame
	#cv2.imshow("Threshold Frame", thresh_frame)#Threshold kept to detect volume
	cv2.imshow("Color Frame (Click 'q' to close application)",frame)#COlor frame with rectangle detects motion
	key=cv2.waitKey(1)

	if key==ord('q'):
		break


video.release()
cv2.destroyAllWindows
