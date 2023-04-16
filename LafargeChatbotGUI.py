from tkinter import *
from LafargeChatbotEngine import ChatbotEngine
import os
import pyttsx3
import speech_recognition as sr

class Lafarge_GUI:
    def __init__(self):
        self.usr_msgs = []
        self.chatbot_reply, self.chatbot_responses, self.chatbot_clr = engine.get_response(self.usr_msgs)
        # Start by creating your first window
        self.window = Tk()

        # Call any additional methods you created that shall affect your window
        self.customizeWindow()
        self.add_widgets(self.chatbot_reply)

    def run(self):
        self.window.mainloop()

    def customizeWindow(self): 
        self.window.title("Lafarge Chatbot")
        # Set the geometry (width, hight, padding x, padding y) of the window
        self.window.geometry('600x500+50+50')
        # State if the window is resizable with respect to width and height
        self.window.resizable(True,False)
        # Control the opacity of the window
        self.window.attributes('-alpha',1)
        # Set the icon on the window (This line may not work because you don't have the
        #       image "pizza.ico" in the directory of your python file)
        self.window.iconbitmap('./logo.ico')
        # Set the background of the window (can do more!!)
        self.window.configure(bg="#00a870")

    def add_widgets(self, welcome_txt):
        # First label widget
        main_label = Label(self.window, bg = "#00a870", fg="white", text="Lafarge Digital Assistent",
                    font="Calibri", padx="10", pady="5")
        # Placing the created label widget with a relative width of 1 (Same width of the parent window)
        main_label.place(relwidth=1)


        #Textbox widget
        self.text_widget = Text(self.window, width=20, height=2, bg="#00a870", fg="white",
                                font="Calibri", padx=5, pady=5)
        self.text_widget.place(relheight=0.65, relwidth=1, rely=0.08)
        self.text_widget.insert(END, "Lafarge Assistant: "+ welcome_txt + "\n\n")
        # Configuring the text widget to have the mouse change cursor over it to be arrow
        #       and disable the user/programmer from accessing the text widget
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        # Trying to insert a string at the end of the text widget (Won't work because the 
        #       state of the text widget is DISABLED)
        self.text_widget.insert(END, "Hi There")
        # Trying to get the text inside the text widget starting from the first row and
        #       the first column (1.1) till the end of the text widget
        content = self.text_widget.get('1.1','end')
        # For debugging
        print(content)


        #entry widget
        self.msg_entry = Entry(self.window, bg="white", fg="#00a870", font="Calibri")
        self.msg_entry.place(relwidth=0.75, relheight=0.06, x=0, y=450)
        # Starting the whole GUI with a focus on the entry widget, which means that the 
        #       application will start with the mouse and keyboard directed into the entry widget
        self.msg_entry.focus()
        # Binding the click on the "ENTER" of the keyboard to the "_on_enter_pressed" function
        #       (means that every time the user will click enter, this function will be called)
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        """
        # First Scrollbar widget
        # Creating the scrollbar widget and choosing the parent to be the text widget
        scrollbar = Scrollbar(self.text_widget)
        # Placing the created scrollbar widget with some choosen attributes
        scrollbar.place(relheight=1, relx=0.974)
        # Configuring the scrollbar widget to control the y-axis view of the text widget
        scrollbar.configure(command=self.text_widget.yview)
        """

        # Voice Button widget
        # Creating the button widget and linking it with the "_on_enter_pressed" function
        speak_button = Button(self.window, text="Speak", font="Calibri", width=20, bg="#00a870", fg = "white",
                               command=lambda: self.speak(None))
        # Placing the created button with some choosen attributes
        speak_button.place(relx=0.77, y=450, relheight=0.06, relwidth=0.10)


        # send Button widget
        # Creating the button widget and linking it with the "_on_enter_pressed" function
        send_button = Button(self.window, text="Send", font="Calibri", width=20, bg="#00a870", fg = "white",
                             command=lambda: self._on_enter_pressed(None))
        # Placing the created button with some choosen attributes
        send_button.place(relx=0.89, y=450, relheight=0.06, relwidth=0.10)


        #add responses buttons
        self.draw_buttons()


    def speak(self, event):
        # create a recognizer object
        r = sr.Recognizer()
    
        # use the default microphone as the audio source
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
        
            print("Say something!")
        
            audio = r.listen(source)
            text = r.recognize_google(audio)
            
        self.msg_entry.insert(0, text)

    def _on_enter_pressed(self, event):
        """
        * @brief Gets a message from the entry widgets and inserts it into the text widget
        """
        # Getting the text inside the entry widget and inserting it
        self._insert_message(self.msg_entry.get(), "You")
        
    def _insert_message(self, msg, sender):
        """
        * @brief Inserts both the user's message and the chatbot's reply into the text box
        * @param self, msg: (string) the messge to be inserted, sender: (string)
        """
        # Checking to make sure we don't insert an empty message
        if not msg:
            return
        
        # ----- This part is for showing the user's message after fromating -----
        # Deleting every thing (from start to end) in the entry widget
        self.msg_entry.delete(0, END)
        # Formatting the message (Concatination "You:" to the begining and 2 new lines to the end)
        msg1 = f"{sender}: {msg}\n\n"
        # Configuring the text widget to enable the user/programmer to access the text widget
        self.text_widget.configure(state=NORMAL)
        # Inserting a string at the end of the text widget
        self.text_widget.insert(END, msg1)
        # Configuring the text widget to disable the user/programmer from accessing the text widget
        self.text_widget.configure(state=DISABLED)

        # Validating the input of the user
        if msg.lower() in self.chatbot_responses:
            self.usr_msgs.append(self.chatbot_responses.index(msg.lower()))
            print(self.usr_msgs)
            self.chatbot_reply, self.chatbot_responses, self.chatbot_clr = engine.get_response(self.usr_msgs)
            self.update_buttons()
            if (self.chatbot_clr):
                self.usr_msgs = []
        else:
            self.chatbot_reply = "Sorry, I didn't understand that. Please try again!"

        # Formatting the message (Concatination "Maze Guide:" to the begining and 2 new lines to the end)
        msg2 = f"{'Lafarge Assistant'}: {self.chatbot_reply}\n\n"
        # Configuring the text widget to enable the user/programmer to access the text widget
        self.text_widget.configure(state=NORMAL)
        # Inserting a string at the end of the text widget
        self.text_widget.insert(END, msg2)
        # Configuring the text widget to disable the user/programmer from accessing the text widget
        self.text_widget.configure(state=DISABLED)
        # Configuring the text widget to always show the last message inserted inside 
        self.text_widget.see(END)
        self.text_widget.update()

        self.say(self.chatbot_reply)

    def draw_buttons(self):
        self.buttons = [None]*len(self.chatbot_responses)
        x1 = 0.05
        x2 = 0.05
        for i in range(len(self.chatbot_responses)):
            x = len(self.chatbot_responses[i])*0.019
            if (i<4):
                self.buttons[i] = Button(self.window, text=self.chatbot_responses[i], font="Calibri", width=20, bg="#00a870", fg = "white",
                             command=lambda i=i: self.msg_entry.insert(0, self.chatbot_responses[i]))
                self.buttons[i].place(relx = x1, y = 370, relheight = 0.06, relwidth = x)
                x1 = x1 + x + 0.02
            else:
                self.buttons[i] = Button(self.window, text=self.chatbot_responses[i], font="Calibri", width=20, bg="#00a870", fg = "white",
                             command=lambda i=i: self.msg_entry.insert(0, self.chatbot_responses[i]))
                self.buttons[i].place(relx = x2, y = 400, relheight = 0.06, relwidth = x)
                x2 = x2 + x + 0.02

    def update_buttons(self):
        for i in self.buttons:
            i.destroy()
        self.draw_buttons()
        print(self.chatbot_responses)

    def say(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()



if __name__ == "__main__":
    os.chdir("Y:\\Lafarge\\ChatBot\\LafargeChatbot")
    # The first line of code to be executed is to create an instance from your main class
    engine = ChatbotEngine()
    app = Lafarge_GUI()
    
    # Second and last thing is to call the "run" method on the main class instance
    app.run()

""" End of file --------------------------------------------------------------------------------"""