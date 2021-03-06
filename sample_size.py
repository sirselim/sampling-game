#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 13:24:25 2015
Last modified on Thur Feb 26 21:45:32 2015

@author: uqrblick
"""
from tkinter import *
from tkinter import ttk
import random
import math

class guessN:

    def __init__(self, master):
        
        self.frame_header=ttk.Frame(master)
        self.frame_header.pack()
        master.resizable(False,False)
        #master.configure(background='CornflowerBlue')
        
        self.style=ttk.Style()
        #self.style.configure('TFrame',background='CornflowerBlue')
        self.style.configure('TLabel',font=('Arial',11))
        self.style.configure('Header.TLabel',font=('Arial',20,'bold'))
        #self.style.configure('TButton',background='CornflowerBlue')        
        
        # build the application header
        self.img=PhotoImage(file = "images//logo.gif").subsample(5,5)
        ttk.Label(self.frame_header, image=self.img, anchor=CENTER).grid(row=0,column=0,rowspan=2, padx=10,pady=10)
        ttk.Label(self.frame_header, text = "Welcome to guessN!", style='Header.TLabel').grid(row=0,column=1, padx=10,pady=10)
        ttk.Label(self.frame_header, wraplength=600,text = ("Evaluate your own skill in guessing how many samples " 
                                                    "you need to record a loss in a population...")).grid(row=1, column=1,padx=10)      
        
        # create a frame to hold the content
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack(side=LEFT)
        
        # assign a label to the user entry field
        ttk.Label(self.frame_content,text="Enter your guess below...").grid(row=1,column=0)

        
        # assign entry field associated with the users guess
        self.entry_guessN = ttk.Entry(self.frame_content,width=24)
        self.text_instructions = Text(self.frame_content, width = 50, height=8, font=('Arial',11))
        self.text_results = Text(self.frame_content, width = 50, height = 10, font=('Arial',11))

        
        # specify the location of widgets
        self.entry_guessN.grid(row = 2, column=0,padx=10,pady=10)
        self.text_instructions.grid(row=0, column=0, columnspan=3,padx=10,pady=10)
        self.text_results.grid(row=4, column=0, columnspan=3,padx=10,pady=10)
        
        # Add buttons for playing and quiting the program
        PlayButton=ttk.Button(self.frame_content, text="Play",command=self.play)
        PlayButton.grid(row=2, column = 1, padx=5, pady=5)
        ttk.Button(self.frame_content, text="Submit",command=self.submit).grid(row=3, column = 1, padx=5, pady=5)
        ttk.Button(self.frame_content, text="Clear",command=self.clear).grid(row=2,column = 2,padx=5,pady=5)  
        ttk.Button(self.frame_content, text="Exit game",command=self.exit).grid(row=3, column = 2, padx=5,pady=5)
        
        # Create plotting frame
        self.frame_plot = ttk.Frame(master)
        self.frame_plot.pack(side=TOP)
        
        # add a temporary place holder for the figure
        self.temp_img=PhotoImage(file = "images/logo.gif").subsample(2,2)
        ttk.Label(self.frame_plot, image=self.temp_img, anchor=CENTER).grid(row=0,column=0, padx=10,pady=10)
        
          # Create plotting frame
        self.frame_concept = ttk.Frame(master)
        self.frame_concept.pack(side=BOTTOM)
        
        # add a temporary place holder for the figure
        self.temp2_img=PhotoImage(file = "images/logo.gif").subsample(2,2)
        ttk.Label(self.frame_concept, image=self.temp2_img, anchor=CENTER).grid(row=0,column=0, padx=10,pady=10)
        
   
    def play(self):
        """Assigns a mean population size (mu) sd and the percentage of loss to game variables, 
        and calculates the new mean (after loss) and the required N to realiably detect the loss."""
        self.mu1=random.randrange(20,40,1)
        self.sd=round(self.mu1*(5/30))
        self.loss=random.randrange(5,20,1)
        self.alpha = 1.96 # set to 5%
        self.beta = 0.84 # set to 80%
        self.mu2= self.mu1-self.mu1*(self.loss/100)
        self.n=((self.alpha+self.beta)/((self.mu2-self.mu1)/self.sd))**2
        # clear all fields        
        self.clear()        
        #
        # Add instruction text to the first text window
        self.instruction_message=("If you have a population mean of %s "
                                    "\nand a standard deviation of %s,"
                                    "\nwhat sample size is required\n" 
                                    "to detect a loss of %s percent? \n"
                                    "\nNote: alpha = 5 percent and power = 80 percent" %(self.mu1,self.sd,self.loss))
        
        self.text_instructions.insert(0.0,self.instruction_message)
        # disable the play button so it cannot be pressed again
       
      
    def submit(self):
        """        
        The submit function takes the information from the users entry,
        and compares it with the correct and calculated N required to detect the loss.
        This function determines three outcomes as an overestimate, underestimate or a correct guess."
        
        """ 
        content=self.entry_guessN.get()
        ##
        try:
            #self.Guess_ID += 1
            type(content) == type(int) or type(float)
            
            # if statements are adjusted to be within 1 sampling unit of the correct answer
            if int(content) <= (self.n-1):
                diff = self.n - int(content)
                message= "You have underestimated the number of samples by " + str(int(math.ceil(diff))) + "\nYou would need " + str(int(math.ceil(self.n))) + " samples to detect a loss of " + str(int(math.ceil(self.loss))) + "%"      
                
            elif int(content) >= (self.n+1):
                diff = int(content)-(self.n)
                message="You have overestimated the number of samples by " + str(int(math.ceil(diff))) + "\nYou need " + str(int(math.ceil(self.n))) + " samples to detect a loss of " + str(int(math.ceil(self.loss))) + "%" 
     
            else: 
                diff = 0.0
                message="Correct"   

            self.text_results.delete(1.0,'end')
            self.text_results.insert(0.0,message)
            
        except:
            self.exception_message ='Opps! Something went wrong. Try entering an integer \nor floating point number'
            self.text_results.insert(0.0,self.exception_message)
            
    def clear(self):
        """
        The clear function removes all entries from the fields
        """
        self.entry_guessN.delete(0,'end')
        self.text_instructions.delete(1.0,'end')
        self.text_results.delete(1.0,'end')
        
        # activate the play button again!!

        
    def exit(self): 
        """
        The exit function with root.destroy() works across multiple OS platforms
        note: sys.ext() makes evil things happen with Windows
        """
   		root.destroy()
   		pass
  
root=Tk()
app=guessN(root)
root.title("guessN! (GUI) v0.1 by RayBlick")
root.mainloop()