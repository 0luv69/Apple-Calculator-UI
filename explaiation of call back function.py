# explaining the callback function 


import customtkinter as ctk

class window(ctk.CTk):
    def __init__(self): 
        super().__init__()

        # window_setup
        self.geometry("400x500")
        self.title("")

        # setting rows and coloum
        self.rowconfigure(list(range(7)),weight=1,uniform="a")
        self.columnconfigure(list(range(4)),weight=1) 

        self.gridding_buttons()

        #runner
        self.mainloop()

    def gridding_buttons(self):
        numbers_gidding_value ={  0:[6,0,2],
                            1:[5,0,1],
                            2:[5,1,1],
                            3:[5,2,1],
                            4:[4,0,1],
                            5:[4,1,1],
                            6:[4,2,1],
                            7:[3,0,1],
                            8:[3,1,1],
                            9:[3,2,1]}

        for key,value in numbers_gidding_value.items():
            numbers_button(self,key,self.numpressed ,value[0],value[1],value[2])

    def numpressed(self,key):
        print(key)

class numbers_button(ctk.CTkButton):
    def __init__(self,window,text,func,row,column,columnspan):
        super().__init__(
            master=window,
            text=text,
            command=lambda :func(text),
            fg_color="#BEBCBD",
            corner_radius=0,
            text_color="#000",hover_color="#F0EFEE",font=("s",25),
        )
        self.grid(row=row,column=column,columnspan=columnspan,sticky="nsew")



window()

# # Explaination
# 1, When the window class is instantiated, it enters the gridding_buttons function.

# 2, Inside the loop in this function, instances of the numbers_button class are created. 
#         However, at this point, the command for the button is not executed. It's set up to execute a command when the button is clicked.

# 3, The command parameter specifies what to do when the button is pressed. It's a callback function. 
#         When a button is clicked, the command (callback) is triggered. It uses a lambda function to call func(text), 
#         where text is the number associated with the button that was clicked. For example, if the button with the number 3 is clicked, the command becomes func(3).

# 4, Moving to line 33, where func = self.numpressed, it means that self.numpressed becomes the callback function for the button. 
#         So, when the button is clicked, it calls self.numpressed(clicked_text), passing the clicked text (number) as an argument.            
