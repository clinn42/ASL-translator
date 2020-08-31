import numpy as np
import cv2
from keras import models
#import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import time


#IMPORT MODEL
p1model = models.load_model('kagg_aslmod2_gray.h5')

#labels
labels_dict = { x:chr(x + 65) for x in range(29)}
labels_dict[26] ='space'
labels_dict[27] = 'del'
labels_dict[28] = 'nothing'

showgray = False
showhsv = False
prevans = ['nothing',time.time]


root = Tk()
root.title("Translator")
vidwidg = Label(root)
vidwidg.pack()

txtframe = Frame(root)
txtframe.pack(fill=X)

lablab = Label(txtframe,text='Message:',font =('Courier',16),anchor=W)
lablab.pack(side=LEFT)

msg = Label(txtframe,text=" ",font =('Courier',16),bg='snow',anchor=W)
msg.pack(side=LEFT,fill=BOTH,expand=1)

butframe = Frame(root,bg='green')
butframe.pack(fill=X,expand=1)

ans = Label(butframe,text=" ",font =('Courier',14),fg='red',relief='ridge',bg='yellow',width=8)
ans.pack(side=LEFT,fill=Y)

clrtxt = Button(butframe,text='clear',font =('Courier',12))
clrtxt.pack(side=LEFT,fill=X,expand=1)
clrtxt.bind('<Button-1>', lambda event: msg.configure(text=' '))

def gay(event):
    global showgray
    if showgray:
        cv2.destroyWindow('Grayscale')
    showgray = not showgray

def hue(event):
    global showhsv
    if showhsv:
        cv2.destroyWindow('HSV')
    showhsv = not showhsv

gbut = Button(butframe,text='Grayscale',font =('Courier',12))
gbut.pack(side=LEFT,fill=X,expand=1)
gbut.bind('<Button-1>',gay)

hbut = Button(butframe,text='HSV',font =('Courier',12))
hbut.pack(side=LEFT,fill=X,expand=1)
hbut.bind('<Button-1>',hue)


cap = cv2.VideoCapture(0)

def makemsg(s):
    
    if s == 'nothing':
        pass
    elif s == 'del':
        m = msg.cget("text")
        if m == ' ' :
            pass
        else:
            msg.configure(text=m[:-1])
    elif s == 'space':
        msg.configure(text=msg.cget("text")+" ")
    else:
        msg.configure(text=msg.cget("text")+s)

def show_video():
    global prevans
    
    #VIDEO FEED
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    
    #RECT CO-ODS
    x1 = 375
    y1 = 125
    
    #EXTRACT SQUARE AREA
    part = frame[y1:y1+200,x1:x1+200]
    part = cv2.flip(part,1)
    forfilt = part
    part = cv2.cvtColor(part, cv2.COLOR_BGR2GRAY)
    #part = cv2.adaptiveThreshold(part,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,3)
    
    #PREDICTION
    temp = cv2.resize(part,(64,64))
    temp = np.reshape(temp,(64,64,1))
    temp = temp.astype('float32')/255.0
    tans = p1model.predict_classes(temp.reshape(1,64,64,1))[0]
    ans.configure(text=labels_dict[tans])
    
    if prevans[0] == tans :
        if time.time() - prevans[1] >=2.5 :
            print(labels_dict[prevans[0]])
            makemsg(labels_dict[prevans[0]])
            prevans[1] =time.time()
    else:
        prevans = [tans,time.time()]
    
    if showgray:
        cv2.imshow('Grayscale',part)

    if showhsv:
        forfilt = cv2.cvtColor(forfilt, cv2.COLOR_BGR2HSV)
        cv2.imshow('HSV',forfilt)
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.rectangle(frame, (x1-1,y1-1),(x1+200,y1+200),(0,255,0),1)
    
    tkimg = ImageTk.PhotoImage(Image.fromarray(frame))
    vidwidg.configure(image=tkimg)
    vidwidg.image = tkimg
    vidwidg.after(10, show_video)

show_video()
root.mainloop()
cap.release()
cv2.destroyAllWindows()

