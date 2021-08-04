import numpy as np
import cv2
from skimage import img_as_ubyte		
from skimage.color import rgb2gray
from keras.models import load_model

width = 640
height = 640

 
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
 
model = load_model('trained_model.h5')
#model = load_model(r"C:\Users\SHREYASI\OneDrive\Desktop\new\train.py")
 
while True:
	success, img_original = cap.read()
	img_gray = rgb2gray(img_original)


	img_gray_u8 = img_as_ubyte(img_gray)
	#cv2.imshow("Window", img_gray_u8)
	
	#Convert grayscale image to binary
	(thresh, im_binary) = cv2.threshold(img_gray_u8, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	

	img_resized = cv2.resize(im_binary,(28,28))

	#invert image
	im_gray_invert = 255 - img_resized
	#cv2.imshow("invert image", im_gray_invert)

	im_final = im_gray_invert.reshape(1,28,28,1)



	ans = model.predict(im_final)
	ans = np.argmax(ans,axis=1)[0]
	print("THE PREDICTED ANSWER CAN BE",ans)


	cv2.putText(img_original,'Predicted Digit : '+str(ans),
                    (50,50),cv2.FONT_HERSHEY_COMPLEX,
                    1,(0,0,255),1)

	cv2.imshow("Original Image",img_original)
	if cv2.waitKey(1) and 0xFF == ord('q'):
		break
        
cap.release()
cv2.destroyAllWindows()




