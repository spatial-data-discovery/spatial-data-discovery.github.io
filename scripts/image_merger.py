import os
import sys
import argparse
import PyPDF2
import tkinter as tk
from tkinter import filedialog
from shutil import rmtree
from PIL import Image
from platform import system as platform
try:
    import pyheif
    pyheif_imported = True
except ImportError:
    pyheif_imported = False


class MainWindow(tk.Tk):

    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        size_x = 600
        size_y = 500
        pos_x = 100
        pos_y = 100
        self.wm_geometry('%dx%d+%d+%d' % (size_x, size_y, pos_x, pos_y))
        self.title('Image Merger')
        self.resizable(0, 0)

        self.left_frame = tk.Frame(self, relief=tk.GROOVE, width=350, height=460, bd=2)
        self.left_frame.place(x=20, y=20)
        self.canvas = tk.Canvas(self.left_frame)
        self.canvas.pack(side="left", fill='both')
        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame.pack(side='right', fill='both')

        my_scrollbar = tk.Scrollbar(self.left_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=my_scrollbar.set)
        my_scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw', width=350)
        self.inner_frame.bind("<Configure>", self.configure_scroll)

        self.right_frame = tk.Frame(self, width=200, height=600)
        self.right_frame.place(x=400, y=0)
        self.right_frame.pack_propagate(0)

        file_button = tk.Button(master=self.right_frame, text='Select Files', bg='black', fg='red',
                                command=self.select_files)
        file_button.pack(side='top', pady=(14, 20))

        compile_button = tk.Button(master=self.right_frame, text='Merge Into PDF',
                                   command=self.merge_files)
        compile_button.pack(side='top', pady=20)

        output_button = tk.Button(master=self.right_frame, text='Select Output Folder',
                                  command=self.select_folder)
        output_button.pack(side='top', pady=20)

        self.folder = None
        self.output_label = tk.Label(master=self.right_frame, text='Output Folder:')
        self.output_label.pack(side='top', pady=(5, 0), fill='x')
        self.folder_label = tk.Label(master=self.right_frame, text='None', wraplength=185, justify='center')
        self.folder_label.pack(side='top', pady=0, fill='x')

        self.file_class = FileList(self)

    def select_files(self):
        files = filedialog.askopenfiles(multiple=True)
        if files:
            for file in files:
                self.file_class.add_file(file)

    def select_folder(self):
        self.folder = filedialog.askdirectory()
        self.update_folder_text()

    def update_folder_text(self):
        if not self.folder:
            text = 'None'
        else:
            text = self.folder
        self.folder_label.config(text=text)

    def merge_files(self):
        if self.file_class.files and self.folder:
            FileMerger(self.file_class.files, self.folder)

    def configure_scroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=350, height=460)


class FileWidget(tk.Frame):

    def __init__(self, parent_frame, file_class, file, index, **kwargs):
        tk.Frame.__init__(self, parent_frame, highlightbackground="black", highlightthickness=1, **kwargs)

        self.file = file
        self.index = index

        tk.Label(self, text=self.get_filename(file), anchor="w").pack(side='left')
        tk.Button(self, text='Remove', bg='black',
                  command=lambda: file_class.remove_file(index=self.index)).pack(side='right')
        tk.Button(self, text='Down', bg='black',
                  command=lambda: file_class.move_down(self.index)).pack(side='right')
        tk.Button(self, text='Up', bg='black',
                  command=lambda: file_class.move_up(self.index)).pack(side='right')

    @staticmethod
    def get_filename(file):
        if type(file) == int:
            return str(file)
        full_path = file.name

        last_break = None
        for i in range(len(full_path)):
            if full_path[-1 - i] == '/' or full_path[-1 - i] == '\\' or full_path[-1 - i] == ':':
                last_break = -1 - i
                break

        if last_break:
            return full_path[last_break+1:]
        else:
            return full_path


class FileList:
    files = []
    widgets = []

    def __init__(self, window):
        self.window = window

    def add_file(self, file):
        self.files.append(file)
        self.draw_widgets()

    def remove_file(self, index):
        del self.files[index]
        self.draw_widgets()

    def clear_all(self):
        for widget in self.widgets:
            widget.pack_forget()
            widget.destroy()

    def draw_widgets(self):
        self.clear_all()
        current_index = 0
        for file in self.files:
            new_widget = FileWidget(self.window.inner_frame, self, file, current_index)
            new_widget.pack(side='top', fill='x', padx=5, pady=5)
            self.widgets.append(new_widget)
            current_index += 1

    def move_up(self, index):
        if index == 0:
            return
        to_move = self.files.pop(index)
        self.files.insert(index - 1, to_move)
        self.draw_widgets()

    def move_down(self, index):
        if index + 1 == len(self.files):
            return
        to_move = self.files.pop(index)
        self.files.insert(index + 1, to_move)
        self.draw_widgets()


class FileMerger:

    def __init__(self, files, output_folder):
        self.files = files
        self.output_folder = output_folder
        self.temp_path = self.make_temp_folder()
        self.make_temp_PDFs()
        self.merge_PDFs()
        self.delete_temp()

    def make_temp_folder(self):
        temp_name = 'temp'
        temp_path = os.path.join(self.output_folder, temp_name)
        while os.path.exists(temp_path):
            if '_' in temp_name:
                current_number = int(temp_name[temp_name.index('_')+1:])
                new_number = str(current_number + 1)
                temp_name = 'temp_' + new_number
                temp_path = os.path.join(self.output_folder, temp_name)
            else:
                temp_name = 'temp_0'
                temp_path = os.path.join(self.output_folder, temp_name)

        os.mkdir(temp_path)
        return temp_path

    def make_temp_PDFs(self):
        for i in range(len(self.files)):
            pdf_name = str(i) + '.pdf'
            pdf_path = os.path.join(self.temp_path, pdf_name)
            img_path = self.files[i].name
            filename, extension = os.path.splitext(img_path)

            if extension.lower() == '.heic':
                if not pyheif_imported:
                    raise ImportError('pyheif package required for converting HEIF files')
                heif_file = pyheif.read(img_path)
                pil_image = Image.frombytes(heif_file.mode,
                                            heif_file.size,
                                            heif_file.data,
                                            "raw",
                                            heif_file.mode,
                                            heif_file.stride,
                                            )
            elif extension.lower() == '.pdf':
                with open(img_path, 'rb') as in_file, open(pdf_path, 'wb') as out_file:
                    out_file.write(in_file.read())
                    continue
            else:
                pil_image = Image.open(img_path)
            pil_image = pil_image.convert('RGB')
            pil_image.save(pdf_path)

    def merge_PDFs(self):
        files = os.listdir(self.temp_path)
        files.sort(key=self.file_comparison)

        merger = PyPDF2.PdfFileMerger()
        for file in files:
            file_path = os.path.join(self.temp_path, file)
            merger.append(file_path)

        output_name = 'MergedImages.pdf'
        output_path = os.path.join(self.output_folder, output_name)
        while os.path.exists(output_path):
            if '_' in output_name:
                current_number = int(output_name[13:-4])
                output_name = 'MergedImages_%i.pdf' % (current_number + 1)
                output_path = os.path.join(self.output_folder, output_name)
            else:
                output_name = 'MergedImages_0.pdf'
                output_path = os.path.join(self.output_folder, output_name)

        merger.write(output_path)

    def delete_temp(self):
        rmtree(self.temp_path)

    @staticmethod
    def file_comparison(filename):
        return int(filename[:-4])


def requirements():
    package_list = [
        'Pillow',
        'PyPDF2',
        'tkinter',
        'pyheif (only if you need to convert .HEIF files)'
    ]
    print('Required packages:')
    for package in package_list:
        print(package)
    sys.exit()


def focus_window(window):
    if platform() == 'Darwin':  # How Mac OS X is identified by Python
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    else:
        window.focus_force()
        window.focus_set()
        window.focus()
        window.lift()


def main():
    parser = argparse.ArgumentParser(
             description="Merges image files of different formats to a multi-page PDF.")
    parser.add_argument("-r", "--requirements", action='store_true', default=False,
                        help="display all required packages and exit")

    args = parser.parse_args()
    if args.requirements:
        requirements()

    window = MainWindow()
    focus_window(window)
    window.mainloop()


if __name__ == '__main__':
    main()
