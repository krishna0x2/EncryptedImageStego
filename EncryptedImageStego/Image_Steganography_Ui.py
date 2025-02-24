import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
from PIL import Image, ImageTk

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def embed_message():
    global img, encrypted_msg, key
    msg = message_entry.get()
    password = password_entry.get()
    
    if not msg or not password:
        messagebox.showerror("Error", "Please enter both message and password.")
        return
    
    key = generate_key()
    encrypted_msg = encrypt_message(msg, key)
    
    n, m, z = 0, 0, 0
    for byte in encrypted_msg:
        img[n, m, z] = byte
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3
    
    cv2.imwrite("encryptedImage.jpg", img)
    messagebox.showinfo("Success", "Message embedded successfully.")

def extract_message():
    global img, encrypted_msg, key
    
    def decrypt_window():
        pas = decrypt_password_entry.get()
        
        if not pas:
            messagebox.showerror("Error", "Passcode is required for decryption.")
            return
        
        n, m, z = 0, 0, 0
        extracted_bytes = bytearray()
        
        for _ in range(len(encrypted_msg)):
            extracted_bytes.append(img[n, m, z])
            n = (n + 1) % img.shape[0]
            m = (m + 1) % img.shape[1]
            z = (z + 1) % 3
        
        try:
            decrypted_msg = decrypt_message(bytes(extracted_bytes), key)
            
            popup = tk.Toplevel()
            popup.title("Decrypted Message")
            popup.geometry("450x350")
            popup.configure(bg="#263238")
            
            img_display = Image.open("encryptedImage.jpg")
            img_display = img_display.resize((250, 250))
            img_tk = ImageTk.PhotoImage(img_display)
            
            label_img = tk.Label(popup, image=img_tk, bg="#263238")
            label_img.image = img_tk
            label_img.pack(pady=10)
            
            label_msg = tk.Label(popup, text=f"Decrypted Message:\n{decrypted_msg}", bg="#263238", fg="white", font=("Arial", 12))
            label_msg.pack(pady=10)
        
        except Exception as e:
            messagebox.showerror("Error", "Failed to decrypt. Possible wrong passcode or corrupted data.")
    
    decrypt_popup = tk.Toplevel()
    decrypt_popup.title("Enter Passcode")
    decrypt_popup.geometry("320x150")
    decrypt_popup.configure(bg="#37474F")
    
    tk.Label(decrypt_popup, text="Enter Passcode for Decryption:", bg="#37474F", fg="white", font=("Arial", 12)).pack(pady=5)
    decrypt_password_entry = tk.Entry(decrypt_popup, width=30, show="*")
    decrypt_password_entry.pack(pady=5)
    tk.Button(decrypt_popup, text="Decrypt", command=decrypt_window).pack(pady=10)

def load_image():
    global img
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg;.png;*.jpeg")])
    if file_path:
        img = cv2.imread(file_path)
        if img is None:
            messagebox.showerror("Error", "Image not found or unsupported format.")
            return
        img_label.config(text=f"Loaded Image: {os.path.basename(file_path)}")
        messagebox.showinfo("Success", "Image loaded successfully.")

root = tk.Tk()
root.title("Image Steganography with Encryption")
root.geometry("600x500")
root.configure(bg="#212121")

load_image_button = tk.Button(root, text="Load Image", command=load_image, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
load_image_button.pack(pady=10)

img_label = tk.Label(root, text="No image loaded", fg="white", bg="#212121", font=("Arial", 12))
img_label.pack(pady=5)

message_label = tk.Label(root, text="Enter Secret Message:", bg="#212121", fg="white", font=("Arial", 12))
message_label.pack(pady=5)
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=5)

password_label = tk.Label(root, text="Enter Passcode:", bg="#212121", fg="white", font=("Arial", 12))
password_label.pack(pady=5)
password_entry = tk.Entry(root, width=50, show="*")
password_entry.pack(pady=5)

embed_button = tk.Button(root, text="Embed Message", command=embed_message, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
embed_button.pack(pady=10)

extract_button = tk.Button(root, text="Extract Message", command=extract_message, bg="#FF5722", fg="white", font=("Arial", 12, "bold"))
extract_button.pack(pady=10)

root.mainloop()
