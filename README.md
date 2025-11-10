# FPS-Cursor-Overlay
This project provides a simple, free, and open-source solution for displaying a custom image as a static crosshair overlay in your favorite FPS games. If you've ever wanted to improve your aim accuracy by using a unique image for your crosshair but found dedicated applications to be paid (such as [Cursor Engine](https://store.steampowered.com/app/2201210/Cursor_Engine) sold on Steam), this Python script is the perfect alternative.

The script creates a small, click-through window that stays on top of all other applications, including full-screen games. It centers a custom `.png` image on your screen, effectively acting as a permanent crosshair to aid in aiming.

## Features

*   **Custom Image Overlay:** Use any `.png` image as your crosshair.
*   **Always on Top:** The overlay remains visible over full-screen applications and games.
*   **Click-Through:** The overlay does not interfere with mouse clicks or game input.
*   **Automatic Resizing:** Automatically scales your image to an appropriate size for an overlay.
*   **Lightweight:** Built with Python and PyQt6, ensuring minimal performance impact.

## How It Works

The script uses the `PyQt6` library to create a transparent, frameless window. This window is configured to always stay on top of other windows and to ignore all mouse inputs, making it "click-through". It loads an image named `overlay.png` from its directory, resizes it, and displays it in the exact center of the primary screen.

## Getting Started

### Prerequisites

*   Python 3.x.x
*   pip

### Installation

There are two ways to use this program.

### 1. For Users (Recommended)

This is the easiest way to get started. It requires no installation or technical knowledge.

1.  Go to the [**Releases Page**](https://github.com/Aru-gxtx/FPS-Cursor-Overlay/releases).
2.  Under the latest release or your preferred compatible version, find the **Assets** section.
3.  Download the `fps_cursor_overlay.exe` file.
4.  Run the file.

### 2. For Developers (Running from Source)

Use this method if you want to run the Python script directly or modify the code.

1.  Clone the repository to your local machine:
    ```bash
    git clone [https://github.com/Aru-gxtx/FPS-Cursor-Overlay.git](https://github.com/Aru-gxtx/FPS-Cursor-Overlay.git)
    ```
2.  Navigate into the project directory:
    ```bash
    cd FPS-Cursor-Overlay
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the script:
    ```bash
    python fps_cursor_overlay.py
    ```

## Usage

1.  **Customize Your Crosshair**
    
    Replace the default `overlay.png` file in the root directory with your desired `.png` image. For best results, use an image with a transparent background. The script will automatically scale the image down to 5% of its original size upon launch. Image size of around 480p (e.g., 360x480) is recommended for the best results.

2.  **Run the Script**
    
    Execute the Python script from your terminal:
    ```bash
    python fps_cursor_overlay.py
    ```
    The overlay will appear in the center of your primary monitor. To close it, stop the script by pressing `Ctrl+C` in the terminal where it is running or clowing the overlay window.
