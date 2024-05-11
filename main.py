import customtkinter as ctk
from settings import *
import darkdetect
try:
    from ctypes import windll,byref,c_int,sizeof
except:pass
# creating the calculator
class window(ctk.CTk):
    def __init__(self,is_dark): # taking value from as dark or not
        
        # setting the background color, and it is color value is defined in setting.py
        super().__init__(fg_color=((White_color,Black_color)))

        # window_setup
        self._set_appearance_mode("dark" if is_dark else "light")
        self.geometry(WINDOW_SIZE)
        self.title("")
        try:
            self.iconbitmap("empty.ico")
        except Exception as error_c:
            print(error_c)
            print("The error could be of the icon file is Not found, \n Plz see the \"empty.ico\" file ")
    
        self.resizable(False,False)
        self.title_bar_color_change(is_dark)   

        # creating the row and the coloumn in window
        self.rowconfigure(list(range(MAIN_ROWS)),weight=1,uniform="a")
        self.columnconfigure(list(range(MAIN_COLUMN)),weight=1)  

        # calling the buttons
        buttons__(self)

        #runner
        self.mainloop()
       
    def title_bar_color_change(self,is_dark):
        # here we are cahnging color of task bar accordingly
        try:    
            HWND= windll.user32.GetParent(self.winfo_id())
            color_=title_bar_balck_color if is_dark else title_bar_white_color
            windll.dwmapi.DwmSetWindowAttribute(HWND,
                                        35,
                                        byref(c_int(color_)),
                                        sizeof(c_int))
        except:   pass 

class buttons__():
    def __init__(self,window):
        self.window=window
        self.history_box()
        self.answer_box()
        self.numbers_button()
        self.arithmetic()
        self.up_three()

        # values
        self.total_called=0
        self.dot_present =False
        self.bodmas = False
        self.front_minus=False

    def history_box(self):
        # simple just making a label and giving it an text_variable and griding it 
        self.history_value=ctk.StringVar()
        self.history_= ctk.CTkLabel(self.window,font=("s",30),textvariable=self.history_value)
        self.history_.grid(row=0,column= 0,columnspan=4,sticky="e",padx=18)

    def answer_box(self):
        # simple just making a label and giving it an text_variable and griding it
        self.Answer_value=ctk.StringVar(value=0)
        self.Answer_= ctk.CTkLabel(self.window,textvariable=self.Answer_value,font=ctk.CTkFont(size=50,weight="bold"))
        self.Answer_.grid(row=1,column= 0,columnspan=4,sticky="e",padx=8)

    def numbers_button(self):
        # here we are creating numbers of button and calling the operation by assing the value
        self.dot=ctk.CTkButton(self.window,text=".",fg_color="#BEBCBD",corner_radius=0,
                                text_color="#000",hover_color="#F0EFEE",font=("s",25), 
                                command=lambda :operation(self,"."))
        self.dot.grid(row=6,column=2,columnspan=1,sticky="nsew")             

        for key,value in numbers_gidding.items():
            numbers_button(self.window,key,self.numpressed ,value[0],value[1],value[2]) #instances of the numbers_button class are created, but command for the button is not executed
    def numpressed(self,key):
        # only get executed when number is pressed, comming from numbers_button callback
        operation(self,key) # it will gain the spefic text value like if 9 was pressed, text=9, so {self.numpressed(9)},and here the key is nine

    def arithmetic(self):
       # here we are creating numbers of button and calling the operation by assing the value
        for key,value in arithmetic_gridding.items():
            arithmetic_button(self.window,key,"#FE9801","#FEB54E",("s",28),self.arithmetic_press,value[0],value[1]) 
    def arithmetic_press(self,key):
        operation(self,key)

    def up_three(self):
       # here we are creating numbers of button and calling the operation by assing the value
        for key, value in up_three_gridding.items():
            arithmetic_button(self.window,key,"#5A595A","#716E70",("ss",30),self.arithmetic_press,value[0],value[1]) 

class numbers_button(ctk.CTkButton):
    def __init__(self,window,text,func,row,column,columnspan):
        super().__init__(
            master=window,
            text=text,
            command=lambda :func(text), #its callback function, which callback the {self.numpressed(text)} when button pressed,casue func= self.numpressed
            fg_color="#BEBCBD",
            corner_radius=0,
            text_color="#000",hover_color="#F0EFEE",font=("s",25),
        )
        self.grid(row=row,column=column,columnspan=columnspan,sticky="nsew")
        pass

class arithmetic_button(ctk.CTkButton):
    def __init__(self,window,text,fg_color,hover_color,font,func,row,column):
        super().__init__(
            master=window,
            text=text,
            command=lambda :func(text), #its callback function, which callback the {self.arithmetic_press(text)} when button pressed,casue func= self.arithmetic_press
            fg_color=fg_color,
            corner_radius=0,
            hover_color=hover_color,font=font,
        )
        self.grid(row=row,column=column,sticky="nsew")


class operation():
    def __init__(self,boxess,value) -> None:
        self.window= window
        self.boxes=boxess
        self.value= value

        # here if the total number written is more then 12 then decresing the font size same decreasing while reached more then 21 
        if self.boxes.total_called >12:
            self.boxes.Answer_.configure(font=ctk.CTkFont(size=30,weight="bold"))
        if self.boxes.total_called >21:
            self.boxes.Answer_.configure(font=ctk.CTkFont(size=15,weight="bold"))
        self.display()

    def display(self):   
        # this function's just display according to button we press
          
        # numbers 0 to 9
        try: # using try so that we could make self.value intger to identify the numbers "0 to 9"
            if int(self.value) in [0,1,2,3,4,5,6,7,8,9]:
                # running this if statement so that in bodmas it would stop removing the arithmetic value before used
                if self.boxes.bodmas == True:
                    self.boxes.bodmas = False

                self.boxes.total_called += 1 # counting the total number typed
                if self.boxes.total_called ==1:
                    # we are here only to remove first zero and insert the value without adding zero at front
                    self.boxes.Answer_value.set("") # so we are setting the answer box empty & removing zero    
                if self.value==0 and self.boxes.total_called==1: 
                    #we are here to stop from repeting 0 again & again, if user clicks more then 1 zero at fist it will stop and ends with one zero
                    self.boxes.Answer_value.set(0)  #so we are setting zero in answer box
                    self.boxes.total_called -=1     # making totaltyped number = 0, so this would be called again if zero pressed then
                else:
                    # else it will set the previous number and resently typed number in answer box
                    inputs=(f"{(self.boxes.Answer_value.get())}{self.value}")
                    self.boxes.Answer_value.set(inputs)          
        except:pass
        
        # dot "."
        if self.value == ".":         
            if self.boxes.dot_present:# if dot is present in first partition then to avoid from pressing more then one "." we pass
                pass
            else: # but incase no . is used then dot will be added in answer box and incresing the typed number/ total_called
                self.boxes.total_called += 1
                inputs=(f"{(self.boxes.Answer_value.get())}{self.value}")
                self.boxes.Answer_value.set(inputs)  
                self.boxes.dot_present =True  #also here we are setting dot prsent true, to to avoid from overpressing dot

        # arithmetic 
        if self.value in ["/","x","+","-"]:   # if value is in (bdmas) rules then it gets into this 
            self.boxes.total_called += 1        
            if not self.boxes.bodmas : #if false / incase of not used bodmas before
                self.boxes.dot_present=False # setting dot present false casue we are moving to new partition
                self.boxes.bodmas =True
                inputs=(f"{(self.boxes.Answer_value.get())}{self.value}")
                self.boxes.Answer_value.set(inputs)  

            elif self.boxes.bodmas :
                #if bodmas is just used and no number is typed, to avoid from overtyped of {x,/,+,-} sign we remove the previous sign and assine the new one
                self.boxes.total_called -=1
                edited_ans=(self.boxes.Answer_value.get())[:-1]
                inputs=(f"{edited_ans}{self.value}")
                self.boxes.Answer_value.set(inputs) 

        # equals too sign '='
        if self.value =="=":    
            answer= ((self.boxes.Answer_value.get()).replace("x", "*")) #repalcing x to *, so that eval could calulate
            result=self.calculate(answer) #sending the string to calculate function, it will return the calculated of all using eval 
            if result !="f": # only gets inside if returned the value by calculate function
                self.boxes.front_minus=False
                if (len((self.boxes.Answer_value.get()))) > 21:  #also setting the size of history box small if more then 21 words
                    self.boxes.history_.configure(font=("s",18))
                self.boxes.history_value.set(self.boxes.Answer_value.get()) # adding all the tranjaction to history box
                self.boxes.Answer_value.set(result)
            if result ==0:
                self.boxes.total_called = 0 #so that it goes to remove the front zero and overwrite of zero
   
        # AC crear screen
        elif self.value =="AC":
            #clear all the answer box, total typed, changing the size to orginal and dot present false
            self.boxes.Answer_.configure(font=ctk.CTkFont(size=50,weight="bold"))
            self.boxes.history_.configure(font=("s",30))
            self.boxes.Answer_value.set(0)
            self.boxes.total_called =0
            self.boxes.dot_present=False
            self.boxes.front_minus=False
            
        # percentage
        if  self.value == "%":
            answer= ((self.boxes.Answer_value.get()).replace("x", "*")) # this line will calculte the answer by replacing x to * 
            result=self.calculate(answer)
            if result !="f":               # only gets inside if returned the value by calculate function
                if (len((self.boxes.Answer_value.get()))) > 21: #also setting the size of history box small if more then 21 words
                    self.boxes.history_.configure(font=("s",18))
                
                in_percent=result/100  # calculating percentage                                      
                self.boxes.history_value.set(f"{self.boxes.Answer_value.get()}%")    
                self.boxes.Answer_value.set(in_percent) 

        # - the front
        if self.value == "+\\-":
        # adding - sign in front if not aviliable as front_minus is true or false
            if not self.boxes.front_minus:
                inputs=(f"-{(self.boxes.Answer_value.get())}")
                self.boxes.front_minus=True
            else:
                inputs=(f"{(self.boxes.Answer_value.get())}")[1:]
                self.boxes.front_minus=False
            self.boxes.Answer_value.set(inputs)        

    def calculate(self,answer):
        try:
            # calculating the answer of string using eval 
            calculate_result= eval(answer)
            return calculate_result
        except: return "f"  # if has some wrong arthmatic placed then it will retun f so no result will be printed
            

if __name__=="__main__":
    # darkdectect.isDark gives boolen value depending on dark or not 
    window((darkdetect.isDark())) # calling window    