import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class CrossroadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Перекресток - Обучение ПДД")
        self.root.geometry("800x600")

        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

        self.image_dir = "traffic_images"
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

        self.create_menu()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.image_frame = tk.Frame(self.main_frame, bg="white")
        self.image_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.image_label = tk.Label(self.image_frame, text="Выберите пункт меню",
                                    font=("Arial", 16), bg="white")
        self.image_label.pack(expand=True, pady=50)

        self.desc_label = tk.Label(self.image_frame, text="",
                                   font=("Arial", 12), bg="white", wraplength=600)
        self.desc_label.pack(pady=10)

        self.nav_frame = tk.Frame(self.root)
        self.nav_frame.pack(side="bottom", fill="x", pady=5)

        self.prev_btn = tk.Button(self.nav_frame, text="← Назад",
                                  command=self.prev_item, state="disabled")
        self.prev_btn.pack(side="left", padx=20)

        self.next_btn = tk.Button(self.nav_frame, text="Вперед →",
                                  command=self.next_item, state="disabled")
        self.next_btn.pack(side="right", padx=20)

        self.current_category = None
        self.current_items = []
        self.current_index = 0

        self.show_welcome_message()

    def show_welcome_message(self):
        welcome_text = """Добро пожаловать в программу "Перекресток"!

Эта программа поможет изучить правила поведения на дороге.

Как пользоваться:
1. Выберите категорию в меню (Светофоры, Перекрестки или Знаки)
2. Выберите конкретный пункт из выпадающего меню
3. Используйте кнопки "Назад" и "Вперед" для навигации
4. Читайте описание под изображением

Будьте внимательны на дороге!"""

        messagebox.showinfo("Добро пожаловать!", welcome_text)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=self.root.quit)

        traffic_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Светофоры", menu=traffic_menu)
        traffic_menu.add_command(label="Красный свет",
                                 command=lambda: self.show_item("traffic", "red",
                                                                "Красный свет означает - СТОЙ! Нельзя переходить дорогу."))
        traffic_menu.add_command(label="Желтый свет",
                                 command=lambda: self.show_item("traffic", "yellow",
                                                                "Желтый свет означает - ВНИМАНИЕ! Будь готов к переходу."))
        traffic_menu.add_command(label="Зеленый свет",
                                 command=lambda: self.show_item("traffic", "green",
                                                                "Зеленый свет означает - ИДИ! Можно переходить дорогу."))

        cross_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Перекрестки", menu=cross_menu)
        cross_menu.add_command(label="Регулируемый перекресток",
                               command=lambda: self.show_item("cross", "regul",
                                                              "Перекресток со светофором. Переходи только на зеленый свет!"))
        cross_menu.add_command(label="Нерегулируемый перекресток",
                               command=lambda: self.show_item("cross", "nereg",
                                                              "Перекресток без светофора. Смотри по сторонам и переходи осторожно!"))

        signs_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Знаки", menu=signs_menu)
        signs_menu.add_command(label="Пешеходный переход",
                               command=lambda: self.show_item("signs", "perex",
                                                              "Этот знак показывает, где можно переходить дорогу."))
        signs_menu.add_command(label="Дети",
                               command=lambda: self.show_item("signs", "deti",
                                                              "Внимание! Здесь часто бывают дети. Будь осторожен!"))
        signs_menu.add_command(label="Стоп",
                               command=lambda: self.show_item("signs", "stop",
                                                              "Знак СТОП. Обязательно остановись!"))

    def show_item(self, category, image_name, description):
        self.current_category = category
        self.current_items = self.get_items_for_category(category)
        item_titles = [item[0] for item in self.current_items]

        current_title = None
        for title, img_name in self.current_items:
            if img_name == image_name:
                current_title = title
                break

        if current_title:
            self.current_index = item_titles.index(current_title)

        self.update_display(image_name, description)

        if len(self.current_items) > 1:
            self.prev_btn.config(state="normal")
            self.next_btn.config(state="normal")
            self.update_nav_buttons()

    def get_items_for_category(self, category):
        items_map = {
            "traffic": [("Красный свет", "red"), ("Желтый свет", "yellow"), ("Зеленый свет", "green")],
            "cross": [("Регулируемый перекресток", "regul"), ("Нерегулируемый перекресток", "nereg")],
            "signs": [("Пешеходный переход", "perex"), ("Дети", "deti"), ("Стоп", "stop")]
        }
        return items_map.get(category, [])

    def update_display(self, image_name, description):
        image_path = os.path.join(self.image_dir, f"{image_name}.png")

        try:
            img = Image.open(image_path)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo

            for title, img_name in self.current_items:
                if img_name == image_name:
                    self.image_label.config(text=title)
                    break
        except:
            self.image_label.config(image='', text=f"{image_name}")

        self.desc_label.config(text=description)

    def prev_item(self):
        if self.current_items and len(self.current_items) > 1:
            self.current_index = (self.current_index - 1) % len(self.current_items)
            self.show_category_item()

    def next_item(self):
        if self.current_items and len(self.current_items) > 1:
            self.current_index = (self.current_index + 1) % len(self.current_items)
            self.show_category_item()

    def show_category_item(self):
        if not self.current_items:
            return

        image_name = self.current_items[self.current_index][1]

        descriptions = {
            "red": "Красный свет означает - СТОЙ! Нельзя переходить дорогу.",
            "yellow": "Желтый свет означает - ВНИМАНИЕ! Будь готов к переходу.",
            "green": "Зеленый свет означает - ИДИ! Можно переходить дорогу.",
            "regul": "Перекресток со светофором. Переходи только на зеленый свет!",
            "nereg": "Перекресток без светофора. Переходи осторожно!",
            "perex": "Этот знак показывает, где можно переходить дорогу.",
            "deti": "Внимание! Здесь часто бывают дети. Будь осторожен!",
            "stop": "Знак СТОП. Обязательно остановись!"
        }

        description = descriptions.get(image_name, "Описание отсутствует")
        self.update_display(image_name, description)
        self.update_nav_buttons()

    def update_nav_buttons(self):
        if len(self.current_items) <= 1:
            self.prev_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
        else:
            self.prev_btn.config(state="normal")
            self.next_btn.config(state="normal")

def main():
    root = tk.Tk()
    app = CrossroadApp(root)

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()

if __name__ == "__main__":
    main()