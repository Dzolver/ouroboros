from tkinter import *
#download and install pillow:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("Ouroboros Chatbot Application")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)

        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Undo")
        edit.add_command(label="Show Text",command=self.showText)
        menu.add_cascade(label="Edit", menu=edit)

        help = Menu(menu)
        help.add_command(label="About")
        menu.add_cascade(label="Help", menu=help)
        sentence_input = Text()
        sentence_input.pack()
        enter_input = Button(label="Enter Input")
        enter_input.pack()

    def showText(self):
        text = Label(self, textvariable = self.myvar)
        text.pack()

    def client_exit(self):
        exit()

root = Tk()

#size of the window
root.geometry("800x600")

app = Window(root)
root.mainloop()