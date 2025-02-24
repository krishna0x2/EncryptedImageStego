
# Image Steganography with Encryption

This project allows you to embed and extract secret messages within images using steganography and encryption techniques. The application uses the Fernet symmetric encryption method to secure the messages.

## Features

- Load an image to embed a secret message.
- Encrypt the message with a passcode.
- Embed the encrypted message into the image.
- Extract and decrypt the message from the image using the passcode.

## Requirements

- Python 3.x
- OpenCV
- Tkinter
- Cryptography
- Pillow

## Installation

1. Clone the repository or download the source code.
2. Install the required Python packages using pip:
    ```bash
    pip install opencv-python cryptography pillow
    ```

## Usage

1. Run the `Image_Steganography_Ui.py` script:
    ```bash
    python Image_Steganography_Ui.py
    ```
2. Use the GUI to load an image, enter a secret message and passcode, and embed the message into the image.
3. To extract a message, load the image with the embedded message, enter the passcode, and extract the message.

## License

This project is licensed under the MIT License.
