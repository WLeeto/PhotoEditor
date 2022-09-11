from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Notebook
import os


class PyPhotoEditor:
    def __init__(self):
        self.root = Tk()
        self.image_tabs = Notebook(self.root)
        self.opened_images = []
        self.init()

        self.filetypes = (
            ("Images", "*.jpeg; *.jpg, *.png"),
        )

    def init(self):
        self.root.title("Photo Editor")
        self.root.iconbitmap('resourses/ico.ico')
        self.image_tabs.enable_traversal()  # Включает сочетание клавищ для переключения м/у вкладками

        self.root.bind('<Escape>', self._close)

    def run(self):
        self.draw_menu()
        self.draw_widgets()

        self.root.mainloop()

    def draw_menu(self):
        menu_bar = Menu(self.root)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_new_images)
        file_menu.add_command(label="Save as", command=self.save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._close)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.configure(menu=menu_bar)

    def draw_widgets(self):
        self.image_tabs.pack(fill="both", expand=1)

    def open_new_images(self):
        image_paths = fd.askopenfilenames(filetypes=self.filetypes)
        for image_path in image_paths:
            self.add_new_image(image_path)

    def add_new_image(self, image_path):
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)
        self.opened_images.append([image_path, image])

        image_tab = Frame(self.image_tabs)

        image_label = Label(image_tab, image=image_tk)
        image_label.image = image_tk
        image_label.pack(side='bottom', fill='both', expand=1)

        self.image_tabs.add(image_tab, text=image_path.split('/')[-1])
        self.image_tabs.select(image_tab)

    def save_image_as(self):

        current_tab = self.image_tabs.select()  # .select возвращает идентификатор текущей вкладки
        if not current_tab:
            return
        tab_number = self.image_tabs.index(current_tab)

        old_path, old_ext = os.path.splitext(self.opened_images[tab_number][0])
        new_path = fd.asksaveasfilename(initialdir=old_path, filetypes=self.filetypes)

        if not new_path:
            return

        new_path, new_ext = os.path.splitext(new_path)
        if not new_ext:
            new_ext = old_ext
        elif old_ext != new_ext:
            mb.showerror("Неверное расширение", f"Указано расширение {new_ext}. Старое расширение {old_ext}")
            return

        image = self.opened_images[tab_number][1]
        image.save(new_path + new_ext)
        image.close()

        del self.opened_images[tab_number]
        self.image_tabs.forget(current_tab)

        self.add_new_image(new_path + new_ext)

    def _close(self, event=None):
        self.root.quit()


if __name__ == "__main__":
    PyPhotoEditor().run()
