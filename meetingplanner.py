from googlemaps import GoogleMaps
from Tkinter import *
import numpy as np
import tkMessageBox
import tkFileDialog
import os
import time
 
class App:
    global address
    def __init__(self, master):
        global entryLabel
        global entryWidget
        global count
        global frame
        count = 0
 
 
        frame = Frame(master)
        
        self.button = Button(frame, text = "Import...", command = self.imports)
        self.button.pack(side = LEFT)
        self.file_opt = options = {}
        options['defaultextension'] = ''
        options['filetypes'] = [('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['parent'] = root
        options['title'] = "Choose the address file"
 
        entryLabel = Label(frame)
        entryLabel["text"] = "Address:"
        entryLabel.pack(side=LEFT)
        entryWidget = Entry(frame)
        entryWidget["width"] = 50
        entryWidget.pack(side=LEFT)
        frame.pack()
        self.next = Button(frame, text = "Next", command = self.occasion)
        self.quit = Button(frame, text = "Quit", command = frame.quit)
        self.quit.pack(side=BOTTOM)
        self.submit = Button(frame, text = "Submit", command = self.submit)
        self.submit.pack(side = LEFT)
        self.next.pack(side = LEFT)
    def submit(self):
        global gmaps
        global lats
        global lngs
        
        if(count==0):       
            lat, lng = gmaps.address_to_latlng(entryWidget.get())
            entryWidget.delete(0, END)
            lats.append(lat)
            lngs.append(lng)
 
        if(count >= 1):
 
        
            local = gmaps.local_search(entryWidget.get() + ' near ' + app.address)
            os.startfile(local['responseData']['cursor']['moreResultsUrl'])
            #for x in range(0,len(local['responseData']['results'])):
            #   print local['responseData']['results'][x]['titleNoFormatting'] +"\n"+ local['responseData']['results'][x]['streetAddress']+"\n"
 
    def imports(self):
        #tkFileDialog.askopenfile(mode='r', **self.file_opt)
    
        filename = tkFileDialog.askopenfilename(**self.file_opt)
        
        file = (open(filename, 'r'))
        
        addresses = file.read().splitlines()
        entryWidget.insert(0,"Processing...    ")
        for x in xrange(len(addresses)):
            
            lat, lng = gmaps.address_to_latlng(addresses[x])
            lats.append(lat)
            lngs.append(lng)
            frame.update()
            if(x%10==0):
                time.sleep(1)
            print lat, lng
            entryWidget.insert(13,str(x+1)+"/"+str(len(addresses))+"...")
            entryWidget.delete(20,END)
        self.occasion()
        
    def occasion(self):
        global count
        count+=1
        entryLabel["text"] = "Occasion:"
        entryWidget.delete(0, END)
        mean1 = np.array(lats[:])
        x = np.mean(mean1)
        mean2 = np.array(lngs[:])
        y = np.mean(mean2)
        x = float(x)
        y = float(y)
 
        reverse = gmaps.reverse_geocode(x,y)
 
        app.address = reverse['Placemark'][0]['address']
 
gmaps = GoogleMaps(APIKEY)      
lats = []
lngs = []           
root = Tk()
app = App(root)
root.title("Meeting Planner")
#root["padx"] = 200
#root["pady"] = 100
root.mainloop()