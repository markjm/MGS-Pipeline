import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import label
import os

class Root(tk.Tk):
    """Container for all frames within the application"""
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Machine Learning Image Classifier")
        #initialize menu
        self.config(menu=MenuBar(self))

        self.status = StatusBar(self)
        self.status.pack(side='bottom', fill='x')
        
        self.appFrame = Application(self)
        self.appFrame.pack(side='top', fill='both', expand='True')
    
        
class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        filemenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=filemenu)
        filemenu.add_command(label="New", command=self.callback)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=1, command=self.quit)

        helpmenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.callback)

    def quit(self):
        sys.exit(0)
    
    def callback(self):
        print("called the callback!")

class StatusBar(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.label = ttk.Label(self, relief='sunken', anchor='w')
        self.label.pack(fill='x')

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

            
class Application(ttk.Notebook):
    def __init__(self, root):
        ttk.Notebook.__init__(self, root)
        self.root = root
        
        tab1 = ClassifyFrame(self)
        tab2 = ttk.Frame(self)
        tab3 = ttk.Frame(self)
        
        self.add(tab1, text = "Classify")
        self.add(tab2, text = "Train")
        #self.add(tab3, text = "Tab 3")

class ClassifyFrame(ttk.Frame):

    about = """
    This tool allows users to quickly evaluate bulk images from a .pb Tensorflow graph.
    
    >Tensorflow and its dependencies are required for this program to function (see www.tensorflow.org for more information).
    >Click on 'Image Directory' to navigate to the folder containing the images (.jpg or .png) to be classified.
    >Click on 'Model Path' to navigate to the the desired graph (.pb) file.
        The labels (.txt) file must be of the same name and in the same directory.
    >Click on the 'Review Directory' to choose where reviewed images are copied to (if 'Copy Images' is toggled
        on and the image is classified with a confidence below the threshold)
    >Click on 'Log Path' to choose where the log should be saved. The log appends to previous entries.
    >If 'Copy Images' is on, images will be copied into the review directory as they are classified.
    """




    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.status = master.root.status

        self.imageFilePath = label.imageFilePath
        self.modelFullPath = label.modelFullPath
        self.labelsFullPath = label.labelsFullPath
        self.logFilePath = label.logFilePath
        self.reviewFilePath = label.reviewFilePath


        self.copyImages = label.copyImages


        self.info = ttk.Label(self, text = self.about)
        self.info.pack(fill='x')
        
        self.button1 = ttk.Button(
            self, text = "Images Directory: " + label.imageFilePath, command = self.chooseImageDirectory)
        self.button1.pack(fill = 'x')

        self.button2 = ttk.Button(
            self, text = "Model Path: " + label.modelFullPath, command = self.chooseModelPath)
        self.button2.pack(fill = 'x')

        self.button3 = ttk.Button(
            self, text = "Log Path: " + label.logFilePath, command = self.chooseLogPath)
        self.button3.pack(fill = 'x')
        
        self.button4 = ttk.Button(
            self, text = "Review Directory: " + label.reviewFilePath, command = self.chooseReviewDirectory)
        self.button4.pack(fill = 'x')
    
        self.checkbutton1 = ttk.Checkbutton(
            self, text="Copy Images", variable=label.copyImages, onvalue = True, offvalue = False)
        self.checkbutton1.pack(side = tk.RIGHT)
    
        self.button4 = ttk.Button(
            self, text = "Run", command = self.run)
        self.button4.pack(fill = 'x')
    
    
    
    

    def set(self, widget, format, *args):
        widget.config(text=format % args)
        widget.update_idletasks()

    def chooseImageDirectory(self):
        base = "Images Directory: "
        chosen = fd.askdirectory(initialdir = label.imageFilePath, title = "Select Images Folder")
        if chosen:
            path = chosen
            label.imageFilePath = chosen
        else:
            path = label.imageFilePath
        self.set(self.button1, base + path)

    def chooseModelPath(self):
        base = "Model Path: "
        chosen = fd.askopenfilename(initialdir = "/",title = "Select Model",
                                    filetypes = [('model files', '.pb')], mustexist = True)
        if chosen:
            path = chosen
            label.modelFullPath = chosen
            filename, _ = os.path.splitext(chosen)
            label.labelsFullPath = filename + '.txt'
        else:
            path = label.modelFullPath
        self.set(self.button2, base + path)

    def chooseLogPath(self):
        base = "Log Path: "
        chosen = fd.askopenfilename(initialdir = "/",title = "Select Log",
                                    filetypes = [('log files', '.csv')])
        if chosen:
            path = chosen
            label.logFilePath = chosen
        else:
            path = label.logFilePath
        self.set(self.button3, base + path)

    def chooseReviewDirectory(self):
        base = "Review Directory: "
        chosen = fd.askdirectory(initialdir = label.reviewFilePath, title = "Select Review Folder")
        if chosen:
            path = chosen
            label.reviewFilePath = chosen
        else:
            path = label.reviewFilePath
            self.set(self.button4, base + path)

    def run(self):
        self.status.set('Running classification...')
        label.run()
        self.status.set('Done Classifying.')

root = Root()
root.mainloop()














