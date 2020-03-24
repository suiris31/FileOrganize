from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from tkinter import *
from initial_config import *
from tkinter import filedialog
import os, time, datetime, logging, subprocess, webbrowser
from pathlib import Path


class MyHandler(FileSystemEventHandler):

    def __init__(self):
        logging.basicConfig(filename='FileOrganizer.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)
        self.tkWindow = TkinterWindow(self)
        self.tkWindow.set_window_title()
        self.tkWindow.set_window_background()
        self.tkWindow.set_label_title()
        self.tkWindow.set_tracked_folder_button()
        self.tkWindow.set_reception_folder_button()
        self.tkWindow.set_button_start()
        self.tkWindow.set_button_stop()
        self.tkWindow.set_button_run_once()
        self.tkWindow.set_log_book()
        self.tkWindow.start_window()

    folder_to_track = str(os.path.join(Path.home(), "Downloads"))
    if not os.path.exists(os.path.join(Path.home(), "Desktop/reception")):
        os.makedirs(os.path.join(Path.home(), "Desktop/reception"))
    folder_destination = os.path.join(Path.home(), "Desktop/reception")
    currdir = str(os.path.join(Path.home(), "Downloads"))

    def on_modified(self, event):
        self.tkWindow.log_book.config(state="normal")
        for filename in os.listdir(self.folder_to_track):
            extension = os.path.splitext(filename)[1]
            src = self.folder_to_track + "/" + filename
            if extension.lower() in img_extentions:
                subfoler="/img"
            elif extension.lower() in office_extentions:
                subfoler="/office"
            elif extension.lower() in adobe_extentions:
                subfoler="/adobe"
            elif extension.lower() in compressed_extentions:
                subfoler="/compressed"
            else:
                subfoler="/undifined"
            destination = self.folder_destination + subfoler
            if not os.path.exists(destination):
                os.makedirs(destination)
            os.rename(src, destination+'/'+filename)
            entry = "["+datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")+"] Fichier : "+filename+" déplacer dans le dossier : "+destination
            self.tkWindow.print_on_logbook(entry)
            logging.info(entry)
        self.tkWindow.log_book.config(state="disabled")
    
    def run_once(self, bol=True):
        if bol:
            self.tkWindow.log_book.config(state="normal")
            self.tkWindow.print_on_logbook("Début lancement rangement manuel")
            self.tkWindow.log_book.config(state="disabled")
            logging.info("Début lancement rangement manuel")
        self.on_modified(None)
        if bol:
            self.tkWindow.log_book.config(state="normal")
            logging.info("Fin lancement rangement manuel")
            self.tkWindow.print_on_logbook("Fin lancement rangement manuel")
            self.tkWindow.log_book.config(state="disabled")
    
    def get_traqued_folder(self):
        tmpDir = filedialog.askdirectory(initialdir=self.currdir, title='Selectionner le dossier à traquer')
        if tmpDir:
            self.folder_to_track = tmpDir

    def get_reception_folder(self):
        tmpDir = filedialog.askdirectory(initialdir=self.currdir, title='Selectionner le dossier de réception')
        if tmpDir:
            self.folder_destination = tmpDir

class TkinterWindow:
    def __init__(self, handler):
        self.observer = Observer()
        self.event_handler = handler
        self.observer.schedule(self.event_handler, self.event_handler.folder_to_track, recursive=True)
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_window_title(self, title = 'File Organizer'):
        self.window.title(title)
    
    def set_window_background(self, bg = 'white'):
        self.window.config(background=bg)

    def set_label_title(self, text = 'Bienvenue sur File Organizer', font = ('Helvetica', 18), bg = 'yellow', fg = 'black' ):
        self.label_title = Label(self.window,text = text, font= font, bg = bg,fg= fg)
        self.label_title.grid(row=0, column=0, columnspan=3, sticky='new', pady=(0, 10))

    def open_folder(self, path):
        webbrowser.open(path)

    def set_tracked_folder_button(self):
        self.label_change_tracked_folder = Label(self.window, text = "Changer dossier traqué : ", font= ('Helvetica', 12), bg ='white', fg= 'black')
        self.label_change_tracked_folder.grid(row=2, column=0, columnspan=1, sticky='ew')
        self.button_select_tracked_folder = Button(
            self.window,
            text="Selectionner le dossier à traquer",
            font=('Helvetica', 12),
            bg='red',
            fg='black', 
            command= lambda:[f() for f in [self.event_handler.get_traqued_folder, self.update_traqued_folder]])
        self.button_select_tracked_folder.grid(row=2, column=1, columnspan=2, sticky='ew')
        self.label_tracked_folder = Label(self.window, text = "Dossier traqué : ", font= ('Helvetica', 12), bg ='white', fg= 'black')
        self.label_tracked_folder.grid(row=3, column=0, columnspan=1, sticky='ew')
        self.button_open_selected_tracked_folder = Button(
            self.window,
            text=self.event_handler.folder_to_track,
            font=('Helvetica', 12),
            bg=None,
            fg='black', 
            command= lambda: self.open_folder(self.event_handler.folder_to_track))
        self.button_open_selected_tracked_folder.grid(row=3, column=1, columnspan=2, sticky='ew')

    def set_reception_folder_button(self):
        self.label_change_tracked_folder = Label(self.window, text = "Changer dossier de réception : ", font= ('Helvetica', 12), bg ='white', fg= 'black')
        self.label_change_tracked_folder.grid(row=4, column=0, columnspan=1, sticky='ew')
        self.button_select_reception_folder = Button(
            self.window,
            text="Selectionner le dossier de réception",
            font=('Helvetica', 12),
            bg='red',
            fg='black', 
            command= lambda:[f() for f in [self.event_handler.get_reception_folder, self.update_reception_folder]])
        self.button_select_reception_folder.grid(row=4, column=1, columnspan=2, sticky='ew', pady=(10, 0))
        self.label_reception_folder = Label(self.window, text = "Dossier de réception : ", font= ('Helvetica', 12), bg ='white', fg= 'black')
        self.label_reception_folder.grid(row=5, column=0, columnspan=1, sticky='ew')
        self.button_open_selected_reception_folder = Button(
            self.window,
            text=self.event_handler.folder_destination,
            font=('Helvetica', 12),
            bg=None,
            fg='black', 
            command= lambda: self.open_folder(self.event_handler.folder_destination))
        self.button_open_selected_reception_folder.grid(row=5, column=1, columnspan=2, sticky='ew')

    
    def update_traqued_folder(self):
        self.button_open_selected_tracked_folder.config(text = self.event_handler.folder_to_track)

    def update_reception_folder(self):
        self.button_open_selected_reception_folder.config(text = self.event_handler.folder_destination)
    
    def set_button_start(self):
        self.button_start = Button(self.window,text="Démarrer",font=('Helvetica', 12),bg='green',fg='white', command=self.start_file_organizer)
        self.button_start.grid(row=6, column=0, padx=2, pady=10, sticky='news')

    def set_button_stop(self):
        self.button_stop = Button(self.window,text="Arreter", state='disabled', font=('Helvetica', 12),bg='red',fg='white', command=self.stop_file_organize)
        self.button_stop.grid(row=6, column=2, padx=2, pady=10, sticky='news')
    
    def set_button_run_once(self):
        self.button_run_once = Button(self.window,text="Ranger dossier", font=('Helvetica', 12),bg='blue',fg='white', command=self.event_handler.run_once)
        self.button_run_once.grid(row=6, column=1, padx=2, pady=10, sticky='news')
    
    def set_log_book(self):
        self.label_log_title = Label(self.window,text = "logbook", font= ('Helvetica', 12), bg = 'white',fg= "black")
        self.label_log_title.grid(row=7, column=0, columnspan=3, sticky='new')
        self.log_frame = Frame(self.window)
        self.log_frame.grid(row=8, column=0, columnspan=3)
        self.log_book = Text(self.log_frame, font= ('Helvetica', 8))
        self.log_scroll = Scrollbar(self.log_frame, command = self.log_book.yview)
        self.log_book.config(yscrollcommand=self.log_scroll.set)
        self.log_book.pack(side=LEFT)
        self.log_scroll.pack(side=RIGHT, fill=Y)
    
    def stop_file_organize(self):
        self.observer.stop()
        self.observer.join()
        self.observer = None
        self.button_select_tracked_folder.config(state="normal")
        self.button_select_reception_folder.config(state="normal")
        self.button_start.config(state="normal")
        self.button_stop.config(state="disabled")
    
    def print_on_logbook(self, t):
        self.log_book.insert(INSERT, t + "\n")
        self.log_book.yview(END)
    
    def start_file_organizer(self):
        if self.observer is None:
            self.observer = Observer()
            self.observer.schedule(self.event_handler, self.event_handler.folder_to_track, recursive=True)
        self.observer.start()
        self.event_handler.run_once(False)
        self.button_select_tracked_folder.config(state="disabled")
        self.button_select_reception_folder.config(state="disabled")
        self.button_start.config(state="disabled")
        self.button_stop.config(state="normal")
    
    def on_closing(self):
        try:
            self.observer.stop()
            self.observer.join()
        except:
            pass
        self.window.destroy()
    
    def start_window(self):
        self.window.mainloop()