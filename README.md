# MyNoteCalendar 📝

A simple, **dynamic** calendar agenda built with **Kivy** that automatically updates each year to always stay current. Quickly view, plan, and note daily tasks or appointments — all stored securely on your device for full privacy.

---
## 📁 Project Structure

```bash
project_root/
│
├── kivy_files/
│ ├── AgendaWidget.kv # Main window layout
│ └── NotePopup.kv # All popup-related layouts and widgets
│
├── globale_gestion.py # Main application logic and classes
│
└── calendar_gestion.py # Helper functions for calendar management
```

## Overview

Each task on the calendar is represented by a **dot**.  
To add a task, use a **dash** (`-`) in the note.  
If there is no dash, a single dot appears by default to let the user know there is something to do on that day.  

- The **current day** is highlighted in blue.  
- Days outside the current month (e.g., before August 1st if the month starts on a Friday) are disabled.

<img width="500" alt="image" src="https://github.com/user-attachments/assets/8cef196a-8797-4112-9236-9f11e1cfd251" />


---

## Fullscreen Mode Available

You can switch to fullscreen for a more immersive and focused experience.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/18ac3461-e6b2-42fc-9cd1-97d0b75a491d" />

---

## Note Pop-up Presentation

Kivy doesn’t support direct editing inline, so a **RelativeLayout** is used to switch between:

- A **preview mode** (summary view)  
- And a **note input mode** (full text editor)

Toggle between these modes with the small arrow button left of the Save button, which switches between `->` and `<-`.

<p float="left">
  <img width="500" alt="image" src="https://github.com/user-attachments/assets/0f379133-189a-47c3-a601-44b484a42da6" style="margin-right:10px"/>
  <img width="500" alt="image" src="https://github.com/user-attachments/assets/54b2bf36-feff-4959-b340-e3b268cffda9" />
</p>

---

## Pastel Colors Submenu

You can highlight notes using pastel colors from a submenu:

<img width="500" alt="image" src="https://github.com/user-attachments/assets/8189683d-6dd0-4ca5-ac2c-53d32cc2c448" />

---

## Classic Colors Submenu

Or choose classic colors from another submenu:

<img width="500" alt="image" src="https://github.com/user-attachments/assets/fa4b6b9e-f556-4d26-8432-71c2bb5c8433" />

---

## Important Note on Colors and Styles

To **remove a color or style**, select the text and press the same color or style button again. This works for both pastel and classic colors, as well as other effects like bold, italic, or underline.
Demonstration :

<img src="https://github.com/user-attachments/assets/4eef2749-4fc1-4fe3-b826-ccac8267be5d" width="500" />

---

## Very Interesting Feature: Detailed Preview Mode

Press the **`p` key** to toggle a much more detailed preview compared to the simple dots on the calendar. This lets each user customize their overview to their liking — one of the project’s favorite features!

<img width="500" alt="image" src="https://github.com/user-attachments/assets/80e860a7-fdc3-4324-a5cd-5b268ef9557a" />

---

## Privacy

All notes and data are saved locally on your device to guarantee **full privacy** with no cloud or internet dependency.

---

## Technologies Used

- [Kivy](https://kivy.org/) — Python framework for multitouch applications  
- Python 3.10+  

---

## How to Run

```bash
git clone https://your-repo-url.git
cd MyNoteCalendar
python3 globale_gestion.py main.py
```

# APK Availability  
The APK will soon be available in the Kivy folders for download so everyone can easily install and use the app on their devices.
Feel free to give me your feedback and suggestions to improve the app ! ;)

