
# coding: utf-8

# In[157]:


import cv2
import numpy as np
import os


# In[158]:


height = 480
width = 640

scale = 1.0


# In[159]:


filename = 'pig_01'
category = 'pothole'


# In[160]:


category_list = ['line', 'marker', 'outside', 'pothole', 'shadow', 'vehicle']


# In[161]:


for i in range(6):
    directory = filename + '/' + category_list[i] + '/original'
    try:
        if not(os.path.isdir(directory)):
            os.makedirs(os.path.join(directory))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise


# In[162]:


for i in range(6):
    directory = filename + '/' + category_list[i] + '/labeled'
    if category_list[i] == 'pothole':
        continue
    try:
        if not(os.path.isdir(directory)):
            os.makedirs(os.path.join(directory))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise


# In[163]:


x_start, y_start, x_end, y_end = 0, 0, 0, 0
cnt, cnt_l, cnt_m, cnt_t, cnt_p, cnt_s, cnt_v = 0, 0, 0, 0, 0, 0, 0

label_pic = np.zeros([height, width])
cropping = False
def Mouse_Crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, filename, cropping
    global cnt, cnt_l, cnt_m, cnt_t, cnt_p, cnt_s, cnt_v, category
    
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        cropping = True
        
        #w1, h1 = int(x/scale), int(y/scale)
        #w2, h2 = w1 + width, h1 + height
        w1, h1 = 0, int(y/scale)
        w2, h2 = width, h1 + height
                
        refPoint = [(w1, h1), (w2, h2)]
 
        if len(refPoint) == 2: #when two points were found
            roi = frame[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]            
            
            if category == 'line':
                cnt = cnt_l
                cnt_l += 1
            elif category == 'marker':
                cnt = cnt_m
                cnt_m += 1
            elif category == 'outside':
                cnt = cnt_t
                cnt_t += 1
            elif category == 'pothole':
                cnt = cnt_p
                cnt_p += 1
            elif category == 'shadow':
                cnt = cnt_s
                cnt_s += 1
            elif category == 'vehicle':
                cnt = cnt_v
                cnt_v += 1
    
            if cnt < 10:
                cv2.imwrite(filename + '/' + category + '/original' + '/' + filename + '_' + category + '_0000' + str(cnt) + '.png', roi) 
                if category != 'pothole':
                    cv2.imwrite(filename + '/' + category + '/labeled' + '/' + filename + '_' + category + '_0000' + str(cnt) + '.png', label_pic) 
            elif cnt < 100:
                cv2.imwrite(filename + '/' + category + '/original' + '/' + filename + '_' + category + '_000' + str(cnt) + '.png', roi) 
                if category != 'pothole':
                    cv2.imwrite(filename + '/' + category + '/labeled' + '/' + filename + '_' + category + '_000' + str(cnt) + '.png', label_pic) 
            elif cnt < 1000:
                cv2.imwrite(filename + '/' + category + '/original' + '/' + filename + '_' + category + '_00' + str(cnt) + '.png', roi) 
                if category != 'pothole':
                    cv2.imwrite(filename + '/' + category + '/labeled' + '/' + filename + '_' + category + '_00' + str(cnt) + '.png', label_pic) 
            elif cnt < 10000:
                cv2.imwrite(filename + '/' + category + '/original' + '/' + filename + '_' + category + '_0' + str(cnt) + '.png', roi) 
                if category != 'pothole':
                    cv2.imwrite(filename + '/' + category + '/labeled' + '/' + filename + '_' + category + '_0' + str(cnt) + '.png', label_pic) 
            else:
                cv2.imwrite(filename + '/' + category + '/original' + '/' + filename + '_' + category + '_' + str(cnt) + '.png', roi)          
                if category != 'pothole':
                    cv2.imwrite(filename + '/' + category + '/labeled' + '/' + filename + '_' + category + '_' + str(cnt) + '.png', label_pic) 
 
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        x_start, y_start = x, y
        x_end, y_end = x + int(width*scale), y + int(height*scale)       
        
        cropping = False


# In[164]:


cap = cv2.VideoCapture('./' + filename + '/' + filename + '.mp4')

if (cap.isOpened()== False): 
  print("Error opening video stream or file")


# In[165]:


fps = cap.get(cv2.CAP_PROP_FPS)
n_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)

print(fps, n_frame)


# In[166]:


font                   = cv2.FONT_HERSHEY_COMPLEX  
bottomLeftCornerOfText = (30, 40)
bottomLeftCornerOfText2 = (30, 70)
fontScale              = 0.7
fontColor              = (0, 255, 255)
lineType               = 1


# In[167]:


idx, flag = 0, 0
crop_img = []
# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret == True:        
        # Crop images (height x width)   
        img = np.copy(frame)
           
        imgS = cv2.resize(img, (0,0), fx=scale, fy=scale)
        if cropping == False:
            #cv2.rectangle(imgS, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
            cv2.rectangle(imgS, (0, y_start), (width, y_end), (255, 0, 0), 2)
        else:
            #cv2.rectangle(imgS, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)
            cv2.rectangle(imgS, (0, y_start), (width, y_end), (0, 0, 255), 2)
            
        cv2.imshow('Frame', imgS)
        cv2.setMouseCallback("Frame", Mouse_Crop)
            
        while 1:
            # Crop images (height x width)   
            img = np.copy(frame)
    
            imgS = cv2.resize(img, (0,0), fx=scale, fy=scale)
            if cropping == False:
                #cv2.rectangle(imgS, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
                cv2.rectangle(imgS, (0, y_start), (width, y_end), (255, 0, 0), 2)
            else:
                #cv2.rectangle(imgS, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)
                cv2.rectangle(imgS, (0, y_start), (width, y_end), (0, 0, 255), 2)
            
            cv2.putText(imgS, 'line[l] marker[m] outside[t] pothole[p] shadow[s] vehicle[v]', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            cv2.putText(imgS, category, bottomLeftCornerOfText2, font, fontScale, fontColor, lineType)
        
            cv2.imshow('Frame', imgS)
            # Press Q on keyboard to exit                
            key = cv2.waitKey(25)
            if key == ord('4'): 
                idx -= 5
                break
            elif key == ord('6'):
                idx += 5
                break
            elif key == ord('7'):
                idx -= 50
                break
            elif key == ord('9'):
                idx += 50
                break
            elif key == ord('8'):
                idx -= 1
                break
            elif key == ord('2'):
                idx += 1
                break
            elif key == ord('q'):
                flag = 1
                break  
            elif key == ord('l'):
                category = 'line'
                break    
            elif key == ord('m'):
                category = 'marker'
                break  
            elif key == ord('t'):
                category = 'outside'
                break    
            elif key == ord('p'):
                category = 'pothole'
                break    
            elif key == ord('s'):
                category = 'shadow'
                break   
            elif key == ord('v'):
                category = 'vehicle'
                break    
        
        if idx < 0:
            idx = 0        
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        
        if flag == 1:
            break
  
    # Break the loop
    else: 
        break


# In[168]:


# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()

