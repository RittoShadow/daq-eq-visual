from Tkinter import *
import plot
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import re

def refreshPlot(f0, f1, c0, c1):
    f0.clf()
    f1.clf()
    path = "/home/rba/Downloads/RBA-DAQ_multisensor/trunk"
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getctime)
    newest = files[-1]
    plot.main(path+"/"+newest, f0, f1)
    canvas0.show()
    canvas1.show()

root = Tk()
root.wm_title("D4Q-3Q")
w = Label(root, text="DAQEQ 2.0   v0.01b", font=("Helvetica", 16), anchor=N)
w.pack()
width = int(0.9*root.winfo_screenwidth())
height = int(0.9*root.winfo_screenheight())
dpi = int(root.winfo_fpixels('1i'))
window = Frame(root, height = height, width = width)
window.pack( side = TOP)
fwidth = int(width/2 - 25)
fheight = int(height - 75)
figure0 = Figure(figsize=(fwidth/dpi,fheight/dpi), dpi=dpi)
canvas0 = FigureCanvasTkAgg(figure0,window)
canvas0.get_tk_widget().configure(highlightthickness = 0)
canvas0.get_tk_widget().place(x = 50, y = 25)
figure1 = Figure(figsize=(fwidth/dpi,fheight/dpi), dpi=dpi)
canvas1 = FigureCanvasTkAgg(figure1,window)
canvas1.get_tk_widget().place(x = int(width/2) + 25, y = 25)
canvas1.get_tk_widget().configure(highlightthickness = 0)
refresh = Button(window, text="Refresh", command = lambda: refreshPlot(figure0, figure1, canvas0, canvas1))
refresh.place(x = int(width/2 - 35), y = height - 40)


root.mainloop()
