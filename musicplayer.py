from tkinter import *
from tkinter import filedialog
import pygame.mixer as mixer
import os


def play_song(song_name: StringVar,songs_list: Listbox, status: StringVar):
    song_name.set(songs_list.get(ACTIVE))
    mixer.music.load(songs_list.get(ACTIVE))
    mixer.music.play()

    status.set("PLAYING")

def stop_song(status:StringVar):
    mixer.music.stop()
    status.set("STOPPED")

def load(listbox):
    os.chdir(filedialog.askdirectory(title='Open Directory'))
    tracks =os.listdir()

    for track in tracks:
        if track.endswith('.mp3') or track.endswith('.m4a') or track.endswith('.aac') or track.endswith('.MP3') or track.endswith('.M4A'):
            listbox.insert(END , track)

def pause_song(status: StringVar):
    mixer.music.pause()
    status.set("PAUSE")

def resume_song(status: StringVar):
    mixer.music.unpause()
    status.set("RESUME")

mixer.init()
root = Tk()
root.geometry('400x420')
root.title('Samuel Music Player')
root.resizable(0,0)

song_frame = LabelFrame(root,text='Current Song', bg='LightGreen', width=400, height=80)
song_frame.place(x=0,y=0)

listbox_frame = LabelFrame(root,text='Playlist',bg='LightGreen')
listbox_frame.place(x=0,y=80,height=200,width=400)

button_frame= LabelFrame(root,text='Control', bg='Grey', width=400,height=120)
button_frame.place(y=280)


current_song=StringVar(root, value='<Not selected>')

song_status = StringVar(root, value='<Not Available>')

playlist = Listbox(listbox_frame,font =('Helvetica',11),fg= 'Green',selectbackground='Brown')

scroll_bar = Scrollbar(listbox_frame, orient = VERTICAL)
scroll_bar.pack(side= RIGHT, fill=BOTH)

playlist.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=playlist.yview)

playlist.pack(fill=BOTH, padx=5, pady = 5)

Label(song_frame,text='CURRENTLY PLAYING: ',bg='LightGreen', font=('Times',10,'bold')).place(x=5,y=20)

song_lbl = Label(song_frame,textvariable=current_song,bg='Green', font=("Times",12),width=25)
song_lbl.place(x=150,y=20)

pause_btn = Button(button_frame, text='Pause',bg='Black',fg='White',font=("Georgia",13),width=7,command=lambda: pause_song(song_status))
pause_btn.place(x=15 , y=10)


stop_btn = Button(button_frame,text='Stop',bg="Black",fg='White',font=("Georgia",13),width=7, command=lambda:stop_song(song_status))
stop_btn.place(x=105,y=10)

play_btn = Button(button_frame, text='Play', bg='Black',fg='White', font=("Georgia", 13), width=7,command=lambda: play_song(current_song, playlist, song_status))
play_btn.place(x=195, y=10)

resume_btn = Button(button_frame, text='Resume', bg='Black',fg='White', font=("Georgia", 13), width=7, command=lambda: resume_song(song_status))
resume_btn.place(x=285, y=10)

load_btn = Button(button_frame, text='Load Directory', bg='Black',fg='White' , font=("Georgia", 13), width=35 , command=lambda: load(playlist))
load_btn.place(x=10, y=55)

Label(root,textvariable=song_status, bg='Blue',fg='White', font=('Times',9),justify=LEFT).pack(side=BOTTOM,fill=X)

root.update()
root.mainloop()