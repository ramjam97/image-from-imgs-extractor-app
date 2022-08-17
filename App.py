import os
from pathlib import Path
import tkinter as tk
from tkinter import END, StringVar, filedialog
from tkinter.ttk import Progressbar
import cv2 as cv

fileList = []
extractedImgs = []

def imageProcessor(filePath=''):
    
    OUTPUT_PATH = outoutDIR_val.get()

    if filePath == '' or len(OUTPUT_PATH) <= 0:
        return

    fileName = Path(filePath).stem
    fileExt = os.path.splitext(filePath)[1]

    img = cv.imread(filePath)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    cap = cv.VideoCapture(filePath)
    hasFrame, frame = cap.read()
    face_cascade = cv.CascadeClassifier('haar_face.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    index = 1
    padding = 20
    for (x, y, w, h) in faces:
        fN = f'{fileName}{fileExt}'
        if len(faces) > 1 : 
            fN = f'{fileName}_{index}{fileExt}'

        face_img = frame[y:y+h, x:x+w]
        if len(face_img) <= 0:
            continue

        imgtoSave = frame[max(0, y-padding): min(y+h+padding, frame.shape[0]-1), max(0, x-padding): min(x+w+padding, frame.shape[1]-1)]
        cv.imwrite(f"{OUTPUT_PATH}/{fN}", imgtoSave)

        extractedImgs.append(fN)

        index += 1
    cap.release()
# end of imageProcessor()

def selectFile():
    image_formats= [("JPEG", "*.jpg")]
    selectedFiles = filedialog.askopenfilenames(filetypes=image_formats, initialdir="/Pictures", title='Please select a image(s) to analyze')

    if len(selectedFiles) > 0:
        for file in selectedFiles:
            fileList.append(file)

        list_selectedFiles.delete(0, END)
        for fD in fileList:
            list_selectedFiles.insert(END, fD)

def selectOutputDIR():
    disFolder = filedialog.askdirectory()
    if len(disFolder) > 0:
        outoutDIR_entry.configure(state="normal")
        outoutDIR_entry.delete(0,END)
        outoutDIR_entry.insert(END, disFolder)
        outoutDIR_entry.configure(state="disabled")

def run():
    OUTPUT_PATH = outoutDIR_val.get()

    if len(OUTPUT_PATH) <= 0:
        tk.messagebox.showwarning(title="Oopps!", message="Please select output destination first")
    else:
        if len(fileList) <= 0:
            tk.messagebox.showwarning(title="Oopps!", message="Please select image/s first")
            return

        run_button["state"] = "disabled"
        pb.stop()
        pb["value"] = 0;
        
        counter = 1;
        for file in fileList:
            imageProcessor(file)

            pb["value"] = (counter / len(fileList)) * 100
            pb.update()

            counter+=1

        tk.messagebox.showinfo(title="Extraction Completed!", message=f"Total extracted images : {len(extractedImgs)}")
        fileList.clear()
        extractedImgs.clear()
        os.startfile(OUTPUT_PATH)

        run_button["state"] = "normal"

app = tk.Tk()

button_frame = tk.Frame(app)
button_frame.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)

# select button
selectImg_button = tk.Button(button_frame, text='Select Images', fg="blue", bg="white", command=selectFile, width=15)
divider_label = tk.Label(button_frame)

# run button
run_button = tk.Button(button_frame, text='Run', fg="white", bg="#0048d8", command=run, width=8,)

button_frame.columnconfigure(0)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2)

selectImg_button.grid(row=0, column=0, sticky=tk.W+tk.E)
divider_label.grid(row=0, column=1, sticky=tk.W+tk.E)
run_button.grid(row=0, column=2, sticky=tk.W+tk.E)

list_selectedFiles = tk.Listbox(app, height=8)
list_selectedFiles.pack(fill=tk.X, padx=5)

outputDIR_frame = tk.Frame(app)
outputDIR_frame.pack(fill=tk.X, padx=5, pady=2.5)

outputDIR_frame.columnconfigure(0)
outputDIR_frame.columnconfigure(1, weight=1, minsize=5)
outputDIR_frame.columnconfigure(2)

selectDIR_label = tk.Label(outputDIR_frame, text="Output Path:", width=10)
outoutDIR_val = StringVar()
outoutDIR_entry = tk.Entry(outputDIR_frame, textvariable=outoutDIR_val, disabledbackground="white", disabledforeground="black", font=('bold', 11))
outoutDIR_entry.configure(state="disabled")
selectDIR_button = tk.Button(outputDIR_frame, text='...', command=selectOutputDIR, bg="white", borderwidth=0.5, width=3)

selectDIR_label.grid(row=0, column=0,sticky=tk.W+tk.E)
outoutDIR_entry.grid(row=0, column=1, sticky=tk.W+tk.E)
selectDIR_button.grid(row=0, column=2, sticky=tk.W+tk.E)

pb = Progressbar(app, orient='horizontal', mode='determinate', length=100)
pb.pack(fill=tk.X, padx=5, pady=2.5)

app.title("Face Extractor")
app.geometry('450x220')
app.mainloop()