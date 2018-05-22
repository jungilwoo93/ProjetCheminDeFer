import math
trace = 0 
     
class CanvasEventsDemo: 
    startX=0
    startY=0
    isDraw=False
    finalX=0
    finalY=0
    objectId=None
    #list=[]
    def __init__(self, parent,shape=None):
        ##canvas = tk.Canvas(width=300, height=300, bg='white') 
        #canvas.pack()
        #canvas.bind('<ButtonPress-1>', self.onStart)  
        #canvas.bind('<B1-Motion>',     self.onGrow)   
        #canvas.bind('<Double-1>',      self.onClear)  
        #canvas.bind('<ButtonPress-3>', self.onMove)   
        self.canvas = parent
        self.isDraw=False
        if shape is not None:
            print("shape is not none")
            #可能没什么用
            self.drawn=shape
        else:
            print("shape is none")
            self.drawn  = None

    def onStart(self, event):
        global objectId
        self.start = event
        canvas = self.start.widget
        if self.isDraw is True:
            canvas.delete(objectId)
        self.drawn = None
        self.startX=self.start.x
        self.startY=self.start.y
        self.isDraw=False
        #self.isDraw=False

    def onGrow(self, event): 
        global objectId,isDraw                      
        canvas = event.widget
        if self.isDraw is False:
            #print("is draw")
            if self.drawn: 
                canvas.delete(self.drawn)
            objectId = canvas.create_rectangle(self.start.x, self.start.y, event.x, event.y)
            if trace: 
                print("trace")
                print(objectId)
            self.drawn = objectId
        

    def onClear(self, event):
        global objectId
        canvas = event.widget
        canvas.delete(objectId)
        self.drawn=None

    def onMove(self, event):
        canvas = event.widget
        if self.drawn: 
            canvas.delete(self.drawn)
        diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
        objectId = canvas.create_rectangle(self.start.x+diffX, self.start.y+diffY, self.finalX+diffX, self.finalY+diffY)
        if trace: 
            print("trace")
            print(objectId)
        self.drawn = objectId
        """if self.drawn:            
            if trace: print(self.drawn)
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y) 
            canvas.move(self.drawn, diffX, diffY)
            self.start = event"""
            
    def onFinal(self,event):
        global isDraw
        self.final=event
        self.finalX=event.x
        self.finalY=event.y
        self.isDraw=True
	
    """def returnStartX(self):
        x=self.startX
        print("return"+str(self.startX))
        return x
		
    def returnFinal(self):
        return self.finalX,self.finalY
    
    def hasDrawn(self):
        return self.isDraw"""
        
    def getCoordonnes(self):
        listCoord=[]
        width=abs(self.finalX-self.startX)
        height=abs(self.finalY-self.startY)
        listCoord.append(self.startX)
        listCoord.append(self.startY)
        listCoord.append(width)
        listCoord.append(height)
        return listCoord
    
    def deleteRect(self):
        print("delete rect")
        self.canvas.delete(objectId)

        
"""import tkinter.filedialog as tf
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
        panelA.bind("<Button-1>", down)
        panelA.bind("<B1-Motion>",move)
        #panelA.bind("<ButtonRelease-1>",up)
        #panelA.bind('<ButtonPress-1>', move) 
        panelA.pack()
    #img=np.zeros((500,500,3),np.uint8)
    
    
btn = tk.Button(root, text="Select an image", command=select_image)
btn.grid(row=0, column=0,padx="10", pady="10")

def down(event):
    global startX,startY,drawing,canvas,a
    startX=event.x
    startY=event.y
    canvas=tk.Canvas(panelA)
    canvas.pack()
    drawing=True
    a=canvas.create_rectangle(startX,startY,startX+1,startY+1,fill='red')
    print("down")
    
def grow(event):
    global canvas,startX,startY,drawing
    canvas=tk.Canvas(root)
    startX=event.x
    startY=event.y
    #if drawing is True:
    print("grow")
    drawing=True
    canvas.create_rectangle(startX,startY,startX+1,startY+1,fill='red')
    
def move(event):
    global currentX,currentY
    currentX=event.x
    currentY=event.y
    print("move?")
    if drawing is True:
        #canvas=tk.Canvas(f1)
        print("move")
        diffX,diffY=(event.x-startX),(event.y-startY)
        #canvas.pack(expand=tk.YES,fill=tk.BOTH)
        canvas.move(a,diffX,diffY)#,outline="red", fill="red", width=2)
       # cv.rectangle(img,(currentX,currentY),(startX,startY),(0,0,255),-1)
        
    
def up(event):
    global finalX,finalY,labelRect
    finalX=event.x
    finalY=event.y
#fonction pour le souris
def draw(event,x,y,flags,param):
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
cv.destroyAllWindows()
#img = cv.imread("C:\\Users\\panpa\\Downloads\\gou.jpg",cv.IMREAD_COLOR)
#cv.imshow('projet',img)
#cv.waitKey(0)
#cv.destroyAllWindows()




img = np.zeros((512,512,3), np.uint8)
cv.namedWindow('image')
draw=cv.setMouseCallback('image',draw_circle)

while True:
    cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break
cv.destroyAllWindows()


root.mainloop()"""