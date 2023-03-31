from functions import *
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from tkinter import filedialog

def explorer():
    global directory
    directory = filedialog.askdirectory()
    label_directory.configure(text="Aktueller Wissenspfad: "+directory)

window = Tk()
window.title('Zentrum des Wissens')
window.geometry("1000x1000")

directory = StringVar()
label_directory = Label(window, text="Das Zentrum des Wissens", width=100, height=4, fg="blue")

figure = Figure(figsize=(8,8), dpi=100)
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.draw()

button_explorer=Button(master=window, command=explorer, height=2, width=10, text="Ordnerpfad")

selection_plot=StringVar()
selection_plot.set("Wähle Datenanalyse")
selection_data=StringVar()
selection_data.set("Datentyp")

menu_analysis=OptionMenu(window, selection_plot, "roher Datenplot", "Geclusterter Datenplot")
menu_type=OptionMenu(window, selection_data, "ToA", "ToT")

button_analysis=Button(master=window, command=lambda: analysis(directory, selection_plot.get(), selection_data.get(), canvas, figure, slider_file), height=2, width=10, text="Analyse")

slider_file=Scale(window, from_=0, to=0, orient="horizontal", width=20)

label_directory.grid(column=1, row=1)
button_explorer.grid(column=2, row=1)
menu_analysis.grid(column=1, row=2)
menu_type.grid(column=2, row=2)
button_analysis.grid(column=1, row=3)
canvas.get_tk_widget().grid(column=1, row=4, columnspan=2)
slider_file.grid(column=1, row=5, sticky='we')

window.mainloop()