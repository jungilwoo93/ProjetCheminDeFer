import numpy as np
import cv2 as cv
import tkinter as tk
import tkinter.filedialog as tf
from PIL import Image, ImageFont, ImageDraw, ImageTk
root = tk.Tk()

drawing = False #si le souris click, devient true
positionCurrent=None
ix,iy = -1,-1
#panelA=None
root.title("Projet")
#récupérer la taille d'écran d'ordi
ecran_width = root.winfo_screenwidth()-500
ecran_height = root.winfo_screenheight()-100
#définir la taille d'écran d'or comme la fenêtre d'application
root.geometry(str(ecran_width)+'x'+str(ecran_height))
f1=tk.Frame(root)
f1.grid(row=0,column=1)
def select_image():
    global path,panelA,img
    path = tf.askopenfilename()
    if len(path) > 0:
        image=cv.imread(path)
        image=Image.fromarray(image)
        image=ImageTk.PhotoImage(image)
        panelA=tk.Label(f1,image=image)
        panelA.image=image
        #panelA.bind("<Button-1>", down)
        panelA.bind("<B1-Motion>",grow)
        panelA.bind("<ButtonRelease-1>",up)
        panelA.bind('<ButtonPress-1>', move) 
        panelA.pack()
    #img=np.zeros((500,500,3),np.uint8)
    
    
btn = tk.Button(root, text="Select an image", command=select_image)
btn.grid(row=0, column=0,padx="10", pady="10")

def down(event):
    global startX,startY,drawing,mode
    startX=event.x
    startY=event.y
    drawing=True
     
def grow(event):
    global canvas
    canvas=event.widget
    #if drawing is True:
    print("grow")
    canvas.create_rectangle(startX,startY,event.x,event.y)
    
def move(event):
    global currentX,currentY
    currentX=event.x
    currentY=event.y
    if drawing is True:
        #canvas=tk.Canvas(f1)
        canvas=event.widget
        diffX,diffY=(event.x-startX),(event.y-startY)
        #canvas.pack(expand=tk.YES,fill=tk.BOTH)
        canvas.move(drawing,diffX,diffY)#,outline="red", fill="red", width=2)
       # cv.rectangle(img,(currentX,currentY),(startX,startY),(0,0,255),-1)
        
    
def up(event):
    global finalX,finalY,labelRect
    finalX=event.x
    finalY=event.y
#fonction pour le souris
"""def draw(event,x,y,flags,param):
    global ix,iy,drawing,mode

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing is True:
            #if mode is True:
                #cv.rectangle(panelA,(ix,iy),(x,y),(0,255,0),-1)
            #else:
            cv.rectangle(panelA,(x,y),5,(0,0,255),-1)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        #if mode is True:
        #    cv.rectangle(panelA,(ix,iy),(x,y),(0,255,0),-1)
        #else:
        cv.rectangle(panelA,(x,y),5,(0,0,255),-1)

cv.setMouseCallback(draw)
cv.destroyAllWindows()"""
#img = cv.imread("C:\\Users\\panpa\\Downloads\\gou.jpg",cv.IMREAD_COLOR)
#cv.imshow('projet',img)
#cv.waitKey(0)
#cv.destroyAllWindows()




"""img = np.zeros((512,512,3), np.uint8)
cv.namedWindow('image')
draw=cv.setMouseCallback('image',draw_circle)"""
"""
while True:
    cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break
cv.destroyAllWindows()"""


root.mainloop()