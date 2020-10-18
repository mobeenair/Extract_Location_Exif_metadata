from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import folium       # folium map to display the extracted location in map
# import webbrowser # for opening map.html in web browser
import webview      # for opening map.html in desktop window
import piexif       # for extracting exif_dict from byte data of image


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()

        # Tkinter window GUI...
        self.title("Image Locator")
        self.geometry('440x150')
        self.resizable(width=False, height=False)

        self.title_label = Label(self, text='Find Location, where image was captured...', padx=10, pady=20)
        self.title_label.config(font=("Courier", 12, 'bold'))
        self.title_label.grid(column=0, row=0)

        self.browse_button = Button(self, text="Browse Image", command=self.file_dialog, height=2, width=15)
        self.browse_button.grid(column=0, row=2)

        # Menu Bar and sub menus...
        my_menu = Menu(self)
        self.config(menu=my_menu)

        sub_menu = Menu(my_menu)
        my_menu.add_cascade(label='File', menu=sub_menu)
        sub_menu.add_command(label='Browse Image...', command=self.file_dialog)
        sub_menu.add_command(label='Open a map...')
        sub_menu.add_separator()
        sub_menu.add_command(label='Save as')
        sub_menu.add_separator()
        sub_menu.add_command(label='Exit', command=self.destroy)

        view_submenu = Menu(my_menu)
        my_menu.add_cascade(label='Edit', menu=view_submenu)
        view_submenu.add_command(label='Show World Map')
        view_submenu.add_command(label='Full Screen')
        view_submenu.add_separator()
        view_submenu.add_command(label='Dark Theme')
        view_submenu.add_command(label='Light Theme')

        help_submenu = Menu(my_menu)
        my_menu.add_cascade(label='Help', menu=help_submenu)
        help_submenu.add_command(label='App Guide')
        help_submenu.add_command(label='About')

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetype=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        # this label shows name of image file in UI after we select
        self.label = ttk.Label(self)
        self.label.grid(column=0, row=4, pady=10)
        self.label.configure(text=os.path.basename(self.filename))

        # image_read data in bytes
        image_file = open(self.filename, 'rb')
        image_read = image_file.read()

        # DICTIONARY_OF_EXIF_DATA = piexif.load(IMAGE_DATA_IN_BYTES)
        # image bytes to exif_dict
        exif_dict = piexif.load(image_read)
        for key in exif_dict:
            if 'GPS' in key:
                # get Degree, Minutes, Seconds data of longitude and latitude from exif_dict
                # dividing the 2 values in D, M and S tuples respectively in nested exif_dict to get decimal values
                lat_degree = exif_dict['GPS'][2][0][0] / exif_dict['GPS'][2][0][1]
                lat_min = exif_dict['GPS'][2][1][0] / exif_dict['GPS'][2][1][1]
                lat_sec = exif_dict['GPS'][2][2][0] / exif_dict['GPS'][2][2][1]

                lon_degree = exif_dict['GPS'][4][0][0] / exif_dict['GPS'][4][0][1]
                lon_min = exif_dict['GPS'][4][1][0] / exif_dict['GPS'][4][1][1]
                lon_sec = exif_dict['GPS'][4][2][0] / exif_dict['GPS'][4][2][1]

                # Calculate decimal latitude and longitude
                lat_deci = lat_degree + lat_min/60 + lat_sec/3600
                lon_deci = lon_degree + lon_min/60 + lon_sec/3600

        # mapping the location in folium map using latitude and longitude calculated before
        my_map = folium.Map(location=[lat_deci, lon_deci], zoom_start=689)
        folium.Marker(location=[lat_deci, lon_deci], popup='Image_Location').add_to(my_map)
        my_map.save("my_map.html")

        print("Map Saved...")

        # opening my_map.html in "webview" desktop window
        webview.create_window("Selected Image's Location", 'my_map.html', min_size=(1100, 300))
        webview.start()

        # optional for opening my_map.html in default web browser
        # webbrowser.open('my_map.html')


# Root class init is triggered as its object is instantiated and UI elements are created
root = Root()
root.mainloop()     # to keep the window OPEN
