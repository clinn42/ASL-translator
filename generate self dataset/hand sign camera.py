import cv2
import os
import re

alpha = [chr(65 + i) for i in range(26)]
alpha += ['space','del','nothing']

train = 'self_dataset/'
lp = True


def capture(ch):
    
    highest = [int(re.findall("[0-9]+",im)[0]) for im in os.listdir(train+ch)]
    if not highest:
        no = 1
    else:
        no = max(highest)
    
    
    print("Press 'c' to capture and esc to exit")
    cap = cv2.VideoCapture(0)
    
    while True:
        ret,frame = cap.read()
        #print(ret)
        frame = cv2.flip(frame,1)
        
        x1 = 375
        y1 = 125
        cv2.rectangle(frame, (x1-1,y1-1),(x1+200,y1+200),(0,255,0),1)
        
        part = frame[y1:y1+200,x1:x1+200]
        part = cv2.flip(part,1)
        
        gaus = cv2.cvtColor(part,cv2.COLOR_BGR2GRAY)
        gaus = cv2.adaptiveThreshold(gaus,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,3)
        #cv2.imshow('filt',gaus)
        cv2.imshow('EXAMPLE',cv2.flip(cv2.imread('demo/'+ch+'.jpg'),1))
        
        cv2.imshow('Translator',frame)
        
        k = cv2.waitKey(5) & 0xFF
        if k == 99:
            cv2.imwrite(train+ch+'/'+ch+str(no)+'.jpg',part)
            print("Captured",ch+str(no)+'.jpg')
            no+=1
        elif k==27:
            break
        
    cap.release()
    cv2.destroyAllWindows()
    #endyolo


while lp:
    print("\n\n")
    i = 0
    for a in alpha:
        print(a+":",len(os.listdir(train+a)),"images","| ",end='')
        i += 1
        if i%5 == 0:
            print()
    
    
    ch = input("\n\nEnter Alphabet for taking picture\t0 to exit\n>>>")
    
    if ch == '0':
        lp = False
    elif ch in alpha:
        capture(ch)
    else:
        print("Invalid input or make sure you are enter Alphabets in uppercase")

