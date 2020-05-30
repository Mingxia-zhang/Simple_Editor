# -- coding: utf-8 --

from tkinter import *
from tkinter import filedialog, colorchooser, simpledialog, messagebox
import tkinter.ttk as ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
from config import ICONS, Format, shutcuts
                                                                                                                                                                                                                                                                                                   
class Editor(Tk):
    def __init__(self):
        super().__init__()
        self.file_name = "Untitled"
        self.current_font_family = "Liberation Mono"
        self.current_font_size = 12
        self.fontColor = '#000000'
        self.fontBackground = '#FFFFFF'
        self.icon_res = []
        self.font_res = []
        self.changeFlag = False
        self._main_window()
        self._set_menu()
        self._set_tool_bar()
        self._set_font_bar()
        self._set_body()
    def _main_window(self):
        self.title("Untitled - Script Editor")
        self.geometry("600x550")
        # setting resizable window
        self.resizable(True, True)
        self.minsize(600, 550) # minimimum size possible
        self.protocol('WM_DELETE_WINDOW', self._exit)
    def _set_menu(self):
        menu = Menu(self)
        self.config(menu=menu)
        # File menu.
        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu, underline=0)
        file_menu.add_command(label="New", command = self.new, compound='left', accelerator='Ctrl+N', underline=0) # command passed is here the method defined above.
        file_menu.add_command(label="Open", command = self.open_file, compound='left', accelerator='Ctrl+O', underline=0)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command = self.save, compound='left', accelerator='Ctrl+S', underline=0)
        file_menu.add_command(label="Save As", command = self.save_as, accelerator='Ctrl+Shift+S', underline=1)
        file_menu.add_command(label="Rename", command = self.rename, accelerator='Ctrl+Shift+R', underline=0)
        file_menu.add_separator()
        file_menu.add_command(label="Close", command = self.close_file, accelerator='Alt+F4', underline=0)

        # Edit Menu.
        edit_menu = Menu(menu)
        menu.add_cascade(label="Edit", menu = edit_menu, underline=0)
        edit_menu.add_command(label="Undo", command = self.undo, compound='left', accelerator='Ctrl+Z', underline=0)
        edit_menu.add_command(label="Redo", command = self.redo, compound='left', accelerator='Ctrl+Y', underline=0)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command = self.cut, compound='left', accelerator='Ctrl+X', underline=0)
        edit_menu.add_command(label="Copy", command = self.copy, compound='left', accelerator='Ctrl+C', underline=1)
        edit_menu.add_command(label="Paste", command = self.paste, compound='left', accelerator='Ctrl+P', underline=0)
        edit_menu.add_command(label="Delete", command = self.delete, underline=0)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command = self.select_all, accelerator='Ctrl+A', underline=0)
        edit_menu.add_command(label="Clear All", command = self.delete_all, underline=6)

        #Tool Menu
        tool_menu = Menu(menu)
        menu.add_cascade(label="Tools", menu=tool_menu, underline=0)
        tool_menu.add_command(label="Change Color")
        tool_menu.add_command(label="Search", compound='left', accelerator='Ctrl+F')

        # Help Menu
        help_menu = Menu(menu)
        menu.add_cascade(label="Help", menu=help_menu, underline=0)
        help_menu.add_command(label="About", accelerator='Ctrl+H', underline=0)
    def _set_tool_bar(self):
        # TOOLBAR
        toolbar = Frame(self, pady=2)
        toolbar.pack(side="top", fill="x")
        # TOOLBAR BUTTONS
        for icon in ICONS:
            photo = Image.open("icons/{}.png".format(icon))
            photo = photo.resize((18, 18), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(photo)
            if icon == "open":
                icon = icon + "_file"
            elif icon == "find":
                icon = icon + "_text"
            else:
                pass
            button = Button(toolbar, image = image, borderwidth=1, width=20, height=20, command = getattr(self, icon))
            button.pack(side="left", padx=4, pady=4)
            self.icon_res.append(image)
    def _set_font_bar(self):
        # FORMATTING BAR
        formattingbar = Frame(self, padx=2, pady=2)
        formattingbar.pack(side="top", fill="x")
        # FORMATTING BAR COMBOBOX - FOR FONT AND SIZE
        # font combobox
        self.all_fonts = StringVar()
        font_menu = ttk.Combobox(formattingbar, textvariable=self.all_fonts , state = "readonly")
        font_menu.pack(side="left", padx=4, pady=4)
        font_menu['values'] = ( 'Courier', 'Helvetica', 'Liberation Mono', 'OpenSymbol', 'Century Schoolbook L', 'DejaVu Sans Mono', 'Ubuntu Condensed', 'Ubuntu Mono', 'Lohit Punjabi', 'Mukti Narrow', 'Meera', 'Symbola', 'Abyssinica SIL')
        #font_menu.bind('<<ComboboxSelected>>',change_font)
        font_menu.current(2)
        # size combobox
        self.all_size = StringVar()
        size_menu = ttk.Combobox(formattingbar, textvariable=self.all_size , state='readonly', width=5)
        size_menu.pack(side="left", padx=4, pady=4)
        size_menu['values'] = ('10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30')
        #size_menu.bind('<<ComboboxSelected>>',change_size)
        size_menu.current(1)
        # FORMATBAR BUTTONS
        for font_item in Format:
            photo_font = Image.open("icons/{}.png".format(font_item))
            photo_font = photo_font.resize((18, 18), Image.ANTIALIAS)
            image_font = ImageTk.PhotoImage(photo_font)
            if font_item == "font-color":
                font_item = "change_color"
            elif font_item.find("-"):
                font_item = font_item.replace("-", "_")
            else:
                pass
            font_button = Button(formattingbar, image = image_font, borderwidth=1, width=20, height=20, pady=10, padx=10, command = getattr(self, font_item))
            font_button.pack(side="left", padx=4, pady=4)
            self.font_res.append(image_font)
    def _set_body(self):
        # STATUS BAR
        status = Label(self, text="", bd=1, relief=SUNKEN, anchor=W)
        status.pack(side="bottom", fill="x")
        # CREATING TEXT AREA - FIRST CREATED A FRAME AND THEN APPLIED TEXT OBJECT TO IT.
        self.text_frame = Frame(self, borderwidth=1, relief="sunken")
        self.text = Text(self.text_frame, wrap="word", font=("Liberation Mono", 12), background="white", borderwidth=0, highlightthickness=0 , undo= True)
        self.text.pack(side="left", fill="both", expand=True) # pack text object.
        self.text_frame.pack(side="bottom", fill="both", expand=True)
        self.text.focus_set()
    def _bind_shutcuts_func(self):
        for key, cmd in shortcuts:
            self.text.bind(key, getattr(self, cmd))
    def _bind_other_func(self):
        self.text.bind('<Key>', self.changeAction)
        
        # --------------- METHODS ---------------- #
    def _exit(self):
        if self.changeFlag:
            ans = messagebox.askquestion(title="Save File" , message="Would you like to save this file")
            if ans:
                self.save()
        if messagebox.askokcancel('Quit?','Are you sure to Quit?'):
            self.destroy()

    def changeAction(self):
        self.changeFlag = True
        self.title(self.file_name + "* - Script Editor")
        
    def new(self, event=None):
        if self.changeFlag:
            ans = messagebox.askquestion(title="Save File" , message="Would you like to save this file")
            if ans is True:
                self.save()
            self.delete_all()
        self.file_name = "Untitled"

    def open_file(self, event=None):
        self.new()
        file = filedialog.askopenfile()
        self.file_name = file.name
        self.text.insert(END, file.read())

    def save(self, event=None):
        if self.changeFlag:
            path = filedialog.asksaveasfilename(title = self.file_name, filetypes=[("txt",".txt")])
            if path == "":
                return
            else:
                self.file_name = path
        self.title(self.file_name + " - Script Editor")
        with open(path, mode='w') as f:
            f.write(self.text.get("1.0", END))

    def save_as(self, event=None):
        path = filedialog.asksaveasfilename(title = self.file_name, filetypes=[("txt",".txt")])
        f = filedialog.asksaveasfile(mode='w')
        if f is None: 
            return
        if path != "":
            self.file_name = path
        self.title(self.file_name + " - Script Editor")
        text2save = str(self.text.get(1.0, END)) 
        f.write(text2save)
        f.close()

    def rename(self, event=None):
        if self.file_name == "":
            open_file()
        arr = self.file_name.split('/')
        path = ""
        for i in range(0 , len(arr) -1):
            path = path + arr[i] + '/'
        new_name = simpledialog.askstring("Rename", "Enter new name")
        os.rename(self.file_name , str(path) + str(new_name))
        self.file_name = str(path) + str(new_name)
        self.title(self.file_name + " - Script Editor")

    def close_file(self, event=None):
        content = self.text.get(1.0, END)
        if content != "":
            self.save()
        self.destroy()

    def cut(self, event=None):
        # first clear the previous text on the clipboard.
        self.clipboard_clear()
        self.text.clipboard_append(string = self.text.selection_get())
        #index of the first and yhe last letter of our selection.
        self.text.delete(index1=SEL_FIRST, index2=SEL_LAST)

    def copy(self, event=None):
        # first clear the previous text on the clipboard.
        print(self.text.index(SEL_FIRST))
        print(self.text.index(SEL_LAST))
        self.clipboard_clear()
        self.text.clipboard_append(string = self.text.selection_get())

    def paste(self, event=None):
        # get gives everyting from the clipboard and paste it on the current cursor position
        # it doesn't remove it from the clipboard.
        self.text.insert(INSERT, self.clipboard_get(type = "STRING"))

    def delete(self):
        self.text.delete(index1=SEL_FIRST, index2=SEL_LAST)

    def undo(self):
        self.text.edit_undo()

    def redo(self):
        self.text.edit_redo()

    def select_all(self, event=None):
        self.text.tag_add(SEL, "1.0", END)

    def delete_all(self):
        self.text.delete(1.0, END)
    # TOOLS MENU METHODS
    def make_tag(self):
        current_tags = self.text.tag_names()
        if "bold" in current_tags:
            weight = "bold"
        else:
            weight = "normal"

        if "italic" in current_tags:
            slant = "italic"
        else:
            slant = "roman"

        if "underline" in current_tags:
            underline = 1
        else:
            underline = 0

        if "overstrike" in current_tags:
            overstrike = 1
        else:
            overstrike = 0

        big_font = tkFont.Font(self.text, self.text.cget("font"))
        big_font.configure(slant= slant , weight= weight , underline= underline , overstrike= overstrike , family= current_font_family , size= current_font_size )
        self.text.tag_config("BigTag", font=big_font , foreground= fontColor , background= fontBackground) 
        if "BigTag" in  current_tags:
            self.text.tag_remove("BigTag" , 1.0 , END)
        self.text.tag_add("BigTag" , 1.0 , END)
    def change_color(self):
        color = colorchooser.askcolor(initialcolor='#ff0000')
        color_name = color[1]
        self.fontColor = color_name
        current_tags = self.text.tag_names()
        if "font_color_change" in current_tags:
            # first char is bold, so unbold the range
            self.text.tag_delete("font_color_change", 1.0 , END)
        else:
            # first char is normal, so bold the whole selection
            self.text.tag_add("font_color_change", 1.0 , END)
        self.make_tag()

    # Adding Search Functionality

    def check(self, value):
        self.text.tag_remove('found', '1.0', END)
        self.text.tag_config('found', foreground='red')
        list_of_words = value.split(' ')
        for word in list_of_words:
            idx = '1.0'
            while idx:
                idx = self.text.search(word, idx, nocase=1, stopindex=END)
                if idx:
                    lastidx = '%s+%dc' % (idx, len(word))
                    self.text.tag_add('found', idx, lastidx)
                    print(lastidx)
                    idx = lastidx

    # implementation of search dialog box - calling the check method to search and find_text_cancel_button to close it
    def find_text(self, event=None):
        search_toplevel = Toplevel(self)
        search_toplevel.title('Find Text')
        search_toplevel.transient(self)
        search_toplevel.resizable(False, False)
        Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
        search_entry_widget = Entry(search_toplevel, width=25)
        search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
        search_entry_widget.focus_set()
        Button(search_toplevel, text="Ok", underline=0, command=lambda: check( search_entry_widget.get())).grid(row=0, column=2, sticky='e' +'w', padx=2, pady=5)
        Button(search_toplevel, text="Cancel", underline=0, command=lambda: find_text_cancel_button(search_toplevel)).grid(row=0, column=4, sticky='e' +'w', padx=2, pady=2)

    # remove search tags and destroys the search box
    def find_text_cancel_button(search_toplevel):
        self.text.tag_remove('found', '1.0', END)
        search_toplevel.destroy()
        return "break"

    # FORMAT BAR METHODS

    def bold(self, event=None):
        current_tags = self.text.tag_names()
        if "bold" in current_tags:
            # first char is bold, so unbold the range
            self.text.tag_delete("bold",  1.0, END)
        else:
            # first char is normal, so bold the whole selection
            self.text.tag_add("bold", 1.0, END)
        self.make_tag()

    def italic(self, event=None):
        current_tags = self.text.tag_names()
        if "italic" in current_tags:
            self.text.tag_add("roman",  1.0, END)
            self.text.tag_delete("italic", 1.0, END)
        else:
            self.text.tag_add("italic",  1.0, END)
        self.make_tag()

    def underline(self, event=None):
        current_tags = self.text.tag_names()
        if "underline" in current_tags:
            self.text.tag_delete("underline",  1.0, END)
        else:
            self.text.tag_add("underline",  1.0, END)
        self.make_tag()

    def strike(self):
        current_tags = self.text.tag_names()
        if "overstrike" in current_tags:
            self.text.tag_delete("overstrike" ,"1.0", END)
        else:
            self.text.tag_add("overstrike" , 1.0, END)
        self.make_tag()

    def highlight(self):
        color = colorchooser.askcolor(initialcolor='white')
        color_rgb = color[1]
        self.fontBackground= color_rgb
        current_tags = self.text.tag_names()
        if "background_color_change" in current_tags:
            self.text.tag_delete("background_color_change", "1.0", END)
        else:
            self.text.tag_add("background_color_change", "1.0", END)
        self.make_tag()

    # To make align functions work properly
    def remove_align_tags(self):
        all_tags = self.text.tag_names(index=None)
        if "center" in all_tags:
            self.text.tag_remove("center", "1.0", END)
        if "left" in all_tags:
            self.text.tag_remove("left", "1.0", END)
        if "right" in all_tags:
            self.text.tag_remove("right", "1.0", END)

    # align_center
    def align_center(self, event=None):
        self.remove_align_tags()
        self.text.tag_configure("center", justify='center')
        self.text.tag_add("center", 1.0, "end")

    # align_justify
    def align_justify(self):
        self.remove_align_tags()

    # align_left
    def align_left(self, event=None):
        self.remove_align_tags()
        self.text.tag_configure("left", justify='left')
        self.text.tag_add("left", 1.0, "end")

    # align_right
    def align_right(self, event=None):
        self.remove_align_tags()
        self.text.tag_configure("right", justify='right')
        self.text.tag_add("right", 1.0, "end")

    # Font and size change functions - BINDED WITH THE COMBOBOX SELECTION
    # change font and size are methods binded with combobox, calling fontit and sizeit
    # called when <<combobox>> event is called

    def change_font(self, event):
        f = all_fonts.get()
        self.current_font_family = f
        self.make_tag()

    def change_size(self, event):
        sz = int(all_size.get())
        self.current_font_size = sz
        self.make_tag()

if __name__ == '__main__':
    app = Editor()
    app.mainloop()