"""
This script illustatrates the Model-View-Controller design pattern.
The canvas is triggered by user input to make a model (a square),
and then a controller is made.
"""

import tkinter as tk

class SquareController(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """
        SquareController is a tk.Frame that provides the GUI interface to control squares drawn in App
        """
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        ##Objects
        self.child = tk.Frame(self.parent, height=2, bd=1, relief='groove', borderwidth=4)
        self.label = tk.Label(self.child, text="Delete?")
        self.button = tk.Button(self.child, text = "Delete")
        self.colorLabel = tk.Label(self.child, text="Color:")
        self.colorInput = tk.Entry( self.child)
        
        ##Packing
        self.child.pack(side='top')
        self.label.pack(side='top')
        self.button.pack(side='top')
        self.colorLabel.pack(side='top')
        self.colorInput.pack(side='top')

        ##Bindings
        self.button.bind("<Button-1>", self.deleteClicked)
 
    def deleteClicked(self, event=None):
        """
        deleteClicked is a callback that deletes the rectangle in the App canvas
        """
        self.child.pack_forget()
        self.child.destroy()
        self.destroy()

    def setLabel(self, text, event=None):
        self.label.config(text=text)
            
        

class App:
    def __init__(self, root):
        self.root = root

        ##Set Canvas
        self.canvas =  tk.Canvas(self.root, bg="pale turquoise", height=700, width=700)
        self.canvas.grid(row=0, column=4)

        ##Add parent frame
        self.mainFrame = tk.Frame(self.root, relief='flat', borderwidth=4)
        self.mainFrame.grid(row=0,column=0,columnspan=3,sticky="n")

        ##Add explanatory labels to the parent frame
        self.label = tk.Label(self.mainFrame, text="Squares")
        self.label1 = tk.Label(self.mainFrame, text="Click on canvas to\ncreate squares!")

        ##Pack Labels
        self.label.pack(side="top")
        self.label1.pack(side="top")

        ##Make the canvas a button
        self.canvas.bind("<Button-1>", self.clickedCanvas)

        ##Store all the rectangles in a list
        self.rectangles = []



    def clickedCanvas(self, event=None):
        x,y = event.x, event.y
        
        tag = str(len(self.rectangles)+1)

        ##Generate the rectangle
        self.rectangles.append(self.canvas.create_rectangle(x+55, y+55, x-55, y-55, fill="sienna", width=0, tags=tag))

        ##Generate the GUI elements
        frame = SquareController(self.mainFrame, relief='flat', borderwidth=9)
        frame.setLabel(tag+" -Cube")
        frame.pack(side="top",  pady=5)

        ##Bindings
        frame.button.bind("<Button-1>", lambda a = frame, b=tag: self.buttonClicked(frame, tag))
        frame.colorInput.bind("<Key>", lambda a =tag, b=frame: self.randColor(tag, frame))

    def buttonClicked(self, frame, tag,  event=None):
        frame.deleteClicked()
        self.canvas.delete(tag)

    def randColor(self, a, frame,event=None):
        try:
            self.canvas.itemconfigure(self.rectangles[int(a)-1], fill=frame.colorInput.get())
        except:
            None

if __name__=="__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

