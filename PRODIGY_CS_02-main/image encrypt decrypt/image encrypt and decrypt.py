import tkinter as tk
from tkinter import filedialog, Label, Entry, Button
import os
from PIL import Image, ImageTk
import numpy as np
import csv

# Initialize main window
main = tk.Tk()
main.title("Image Encrypt Decrypt")
main.minsize(400, 300)
main.configure(background='#dfdddd')

# Labels and entries
Label(main, text="Open File:", font=('Impact', -20), bg='#dfdddd').grid(column=0, row=2, padx=20, pady=20)
Label(main, text="Enter Encryption Key:").grid(column=0, row=4)
Label(main, text="Enter Decryption Key:").grid(column=0, row=6)

enc_key_entry = Entry(main)
enc_key_entry.grid(column=1, row=4)
dec_key_entry = Entry(main)
dec_key_entry.grid(column=1, row=6)

# Function to show temporary message
def show_temp_message(message, row):
    label = Label(main, text=message, bg='#dfdddd')
    label.grid(column=0, row=row, columnspan=2)
    main.after(2000, label.destroy)

# File dialog function
def fileDialog():
    main.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    if main.filename:
        img = Image.open(main.filename)
        img.thumbnail((100, 100))
        img = ImageTk.PhotoImage(img)
        panel = Label(main, image=img)
        panel.image = img
        panel.grid(column=2, row=2, rowspan=2)

# Encryption function
def encryption():
    if not main.filename:
        show_temp_message("No file selected!", 8)
        return
    
    try:
        enc_key = int(enc_key_entry.get())
    except ValueError:
        show_temp_message("Invalid encryption key!", 8)
        return
    
    img = Image.open(main.filename)
    img_array = np.array(img)
    encrypted_array = (img_array + enc_key) % 256
    
    csv_filename = "encrypted_image.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(img_array.shape)
        for row in encrypted_array:
            writer.writerows(row)
    
    show_temp_message(f"Encryption Done! Saved as {csv_filename}", 8)

# Decryption function
def decryption():
    filename = filedialog.askopenfilename(initialdir="/", title="Select A CSV File", filetype=(("CSV files", "*.csv"), ("all files", "*.*")))
    if not filename:
        show_temp_message("No file selected!", 8)
        return
    
    try:
        dec_key = int(dec_key_entry.get())
    except ValueError:
        show_temp_message("Invalid decryption key!", 8)
        return
    
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        shape = next(reader)
        shape = tuple(map(int, shape))
        encrypted_array = np.array([row for row in reader], dtype=int).reshape(shape)
    
    decrypted_array = (encrypted_array - dec_key) % 256
    decrypted_img = Image.fromarray(decrypted_array.astype('uint8'))
    decrypted_img.save("decrypted_image.jpg")
    
    show_temp_message("Decryption Done! Saved as decrypted_image.jpg", 8)

# Show original image function
def original():
    if not main.filename:
        show_temp_message("No file selected!", 8)
        return

    img = Image.open(main.filename)
    img.show()

# Buttons
Button(main, text="Browse for image", font=('Impact', -10), command=fileDialog).grid(column=1, row=2)
Button(main, text="Original", command=original, bg='#e28743').grid(column=0, row=3)
Button(main, text="Encrypt", command=encryption, bg='#e28743').grid(column=2, row=4)
Button(main, text="Decrypt", command=decryption, bg='#e28743').grid(column=2, row=6)

# Run the main loop
main.mainloop()
