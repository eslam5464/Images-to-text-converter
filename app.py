from datetime import datetime
from tkinter import filedialog
from pathlib import Path
import cv2
from PIL import Image as PILImage
from pytesseract import pytesseract
from tkinter import *
from datetime import datetime
import webbrowser

appVersion = 0.1


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)

        self.lbl_userHint = Label(self, text="Press letter 'S' in keyboard to save the image", fg="blue")
        self.lbl_appVersion = Label(self, text=f"Version: {appVersion}", fg="brown")

        self.lbl_videoCamNum = Label(self, text="Video camera number: ")
        self.entry_videoCamNum_text = StringVar()
        self.entry_videoCamNum_text.set("1")
        self.entry_videoCamNum = Entry(self, width=2, textvariable=self.entry_videoCamNum_text)

        self.lbl_imageLocation = Label(self, text="Image Location: ")
        self.entry_imageLocation_text = StringVar()
        self.entry_imageLocation = Entry(self, width=85, textvariable=self.entry_imageLocation_text)
        self.btn_getImageLocation = Button(self, text="Set image location", command=self.SetImageLocation)
        self.grid()

        self.lbl_outputTextLocation = Label(self, text="Output Location: ")
        self.entry_outputTextLocation_text = StringVar()
        self.entry_outputTextLocation = Entry(self, width=85, textvariable=self.entry_outputTextLocation_text)
        self.btn_getTextOutputLocation = Button(self, text="Set output text location", command=self.SetOutputTextLocation)

        self.btn_start = Button(self, text="Start", command=self.TesseractStart)

        self.lbl_error = Label(self, text="", fg="red")

        self.lbl_info = Label(self, text="", fg="green")

        self.Create_widgets()

    def Create_widgets(self):
        line = 1
        self.lbl_userHint.grid(row=line, column=2, sticky="we")
        self.lbl_appVersion.grid(row=line, column=3, sticky="e")

        line += 1
        self.lbl_videoCamNum.grid(row=line, column=1, sticky=W)
        self.entry_videoCamNum.grid(row=line, column=2, sticky=W)

        line += 1
        self.lbl_imageLocation.grid(row=line, column=1, sticky=W)
        self.entry_imageLocation.grid(row=line, column=2, sticky=W)
        self.btn_getImageLocation.grid(row=line, column=3)

        line += 1
        self.lbl_outputTextLocation.grid(row=line, column=1, sticky=W)
        self.entry_outputTextLocation.grid(row=line, column=2, sticky=W)
        self.btn_getTextOutputLocation.grid(row=line, column=3)

        line += 1
        self.btn_start.grid(row=line, column=2)

        line += 1
        self.lbl_error.grid(row=line, column=2, sticky="we")

        line += 1
        self.lbl_info.grid(row=line, column=2, sticky="we")

    def SetImageLocation(self):
        folder_selected = filedialog.askdirectory()
        folder_selected = folder_selected.replace("/", "\\")
        self.entry_imageLocation_text.set(folder_selected)

    def SetOutputTextLocation(self):
        folder_selected = filedialog.askdirectory()
        folder_selected = folder_selected.replace("/", "\\")
        self.entry_outputTextLocation_text.set(folder_selected)

    def TesseractStart(self):
        location_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        my_file = Path(location_tesseract)
        if not my_file.is_file():
            self.lbl_error.config(text="Tesseract is not installed")

        elif self.entry_videoCamNum.get() == "":
            self.lbl_error.config(text="Camera number not entered")

        elif self.entry_imageLocation_text.get() == "":
            self.lbl_error.config(text="Image location not selected")

        elif self.entry_outputTextLocation.get() == "":
            self.lbl_error.config(text="Output location not selected")

        else:
            self.lbl_error.config(text="")
            time_now = datetime.now()
            time_now_str = time_now.strftime("%d/%m/%Y %I:%M:%S %p")
            self.imgName = time_now.strftime("%Y%m%d %H%M%S")

            self.StartImageCapture()
            image_path = rf"{self.entry_imageLocation_text.get()}\{self.imgName}.jpg"
            pytesseract.tesseract_cmd = location_tesseract
            text = pytesseract.image_to_string(PILImage.open(image_path))

            with open(rf"{self.entry_outputTextLocation_text.get()}\{self.imgName}.txt", "w") as fWrite:
                fWrite.write(text[:-1])

            self.lbl_info.config(text=f"Image taken at: {time_now_str}")
            webbrowser.open(rf"{self.entry_outputTextLocation_text.get()}\{self.imgName}.txt")

    def StartImageCapture(self):
        camera = cv2.VideoCapture(int(self.entry_videoCamNum.get()))
        windowName = "Image to text"
        cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
        _, image = camera.read()
        cv2.imshow(windowName, image)

        while cv2.getWindowProperty(windowName, 0) >= 0:
            _, image = camera.read()
            cv2.imshow(windowName, image)
            if cv2.waitKey(1) & 0xFF == ord("s"):
                cv2.imwrite(rf"{self.entry_imageLocation_text.get()}\{self.imgName}.jpg", image)
                break
        camera.release()
        cv2.destroyAllWindows()


Window = Tk()
Window.title("Image to Text")
Window.geometry("780x170")
app = Application(Window)
app.mainloop()
