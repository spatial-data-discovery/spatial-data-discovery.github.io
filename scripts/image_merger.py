import os
import sys
import tkinter as tk
from tkinter import filedialog
from argparse import ArgumentParser
from shutil import rmtree
from platform import system as platform

import PyPDF2
from PIL import Image
try:
    import pyheif
    pyheif_imported = True
except ImportError:
    pyheif_imported = False


class MainWindow(tk.Tk):
    """
    This is a subclass of tkinter.Tk which holds all elements of the GUI.

    Attributes
    ----------
    output_folder : str
        path to user-selected output folder
    files : FileList
        instance of FileList, stores user-selected files
    left_frame : tkinter.Frame
        Frame occupying left side of window with parent self
    right_frame : tkinter.Frame
        Frame occupying right side of window with parent self
    canvas : tkinter.Canvas
        scrollable Canvas with parent left_frame
    inner_frame : tkinter.Frame
        Frame with parent canvas, holds all FileWidgets
    folder_label : tkinter.Label
        Label with parent right_frame, displays output_folder as text

    Methods
    -------
    select_files():
        Opens file selection dialog and adds selection to files.
    merge_files():
        Merges selected files into PDF saved in output_folder.
    select_folder():
        Opens folder selection dialog and assigns selection
        to output_folder.
    update_folder_text():
        Updates text of folder_label.
    configure_scroll(event):
        Configures scroll area of canvas.
    """

    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        # output_folder represents the directory at which the merged
        # PDF will be saved.
        self.output_folder = None
        self.files = FileList(self)

        # Fixes window size to constant value.
        size_x, size_y, pos_x, pos_y = 600, 500, 100, 100
        self.wm_geometry('%dx%d+%d+%d' % (size_x, size_y, pos_x, pos_y))
        self.resizable(0, 0)

        self.title('Image Merger')

        # Creates two tkinter.Frames and one tkinter.Canvas which are
        # used to make a scrollable region to display and interact with
        # selected files. inner_frame's children are FileWidgets which
        # represent the selected files.
        self.left_frame = tk.Frame(self, relief=tk.GROOVE, width=350,
                                   height=460, bd=2)
        self.left_frame.place(x=20, y=20)
        self.canvas = tk.Canvas(self.left_frame)
        self.canvas.pack(side='left', fill='both')
        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame.pack(side='right', fill='both')

        # Creates tkinter.Scrollbar (which is not saved as a class
        # attribute because it is never accessed after __init__).
        # Assigns scrollbar to canvas, creating scrollable region,
        # and packs into left_frame.
        scrollbar = tk.Scrollbar(self.left_frame, orient='vertical',
                                 command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Don't fully understand what this does, but helps create
        # scrollable region.
        self.canvas.create_window((0, 0), window=self.inner_frame,
                                  anchor='nw', width=350)
        self.inner_frame.bind('<Configure>', self.configure_scroll)

        # right_frame is where everything besides FileWidgets will
        # be packed, including three tkinter.Buttons and two
        # tkinter.Labels.
        self.right_frame = tk.Frame(self, width=200, height=600)
        self.right_frame.place(x=400, y=0)
        self.right_frame.pack_propagate(0)

        # Creates three Buttons which control file selection,
        # merging into PDF, and output folder selection. Packs them
        # into right_frame.
        tk.Button(master=self.right_frame, command=self.select_files,
                  text='Select Files').pack(side='top', pady=(14, 20))
        tk.Button(master=self.right_frame, command=self.merge_files,
                  text='Merge Into PDF').pack(side='top', pady=20)
        tk.Button(master=self.right_frame, command=self.select_folder,
                  text='Select Output Folder').pack(side='top', pady=20)

        # Creates Labels to display currently selected output folder.
        tk.Label(master=self.right_frame, text='Output Folder:')\
            .pack(side='top', pady=(5, 0), fill='x')
        self.out_label = tk.Label(master=self.right_frame, text='None',
                                  wraplength=185, justify='center')
        self.out_label.pack(side='top', pady=0, fill='x')

    def select_files(self):
        files = filedialog.askopenfilenames(multiple=True)
        for file in files:
            self.files.add_file(file)

    def merge_files(self):
        if self.files.files and self.output_folder:
            FileMerger(self.files.files, self.output_folder)

    def select_folder(self):
        self.output_folder = filedialog.askdirectory()
        self.update_folder_text()

    def update_folder_text(self):
        if not self.output_folder:
            text = 'None'
        else:
            text = self.output_folder
        self.out_label.config(text=text)  # Changes text of out_label

    def configure_scroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),
                              width=350, height=460)


class FileWidget(tk.Frame):
    """
    This is a subclass of tkinter.Frame which stores a single file path
    and displays it as a widget with Up, Down, and Remove buttons.

    Attributes
    ----------
    file : str
        path to user-selected output folder
    index : int
        index of corresponding file in FileList.files

    Methods
    -------
    static get_filename(full_path):
        Returns filename portion of full_path. Shortens filename if
        length is too long to display.
    """

    def __init__(self, parent_frame, file_class, file, index, **kwargs):
        tk.Frame.__init__(self, parent_frame, highlightbackground='black',
                          highlightthickness=1, **kwargs)

        self.file = file
        # Represents index of corresponding file in FileList.list.
        self.index = index

        # This Label displays the filename portion of the full path.
        tk.Label(self, text=self.get_filename(file),
                 anchor='w').pack(side='left')

        # Creates functions which call methods of FileList.
        def remove_lambda(): file_class.remove_file(self.index)
        def down_lambda(): file_class.move_down(self.index)
        def up_lambda(): file_class.move_up(self.index)

        # Creates three buttons for moving up, moving down,
        # or removing FileWidgets.
        tk.Button(self, command=remove_lambda,
                  text='Remove').pack(side='right')
        tk.Button(self, command=down_lambda,
                  text='Down',).pack(side='right')
        tk.Button(self, command=up_lambda,
                  text='Up').pack(side='right')

    @staticmethod
    def get_filename(full_path):
        last_break = None
        for i in range(len(full_path)):
            # Checks whether current character is a path delimiter,
            # starting at end of path and moving backwards.
            if full_path[-1 - i] in ['/', '\\', ':']:
                last_break = -1 - i
                break

        # Assigns the filename portion of full_path to file_name, or
        # assigns all of full_path if no delimiter is found.
        if last_break is not None:
            file_name = full_path[last_break + 1:]
        else:
            file_name = full_path

        # Shortens file_name if file_name is too large.
        if len(file_name) > 20:
            return file_name[:17] + '...'
        else:
            return file_name


class FileList:
    """
    This class stores selected files and FileWidgets, displays
    FileWidgets in MainWindow.inner_frame, and handles any changes
    (movement up/down or deletion) to FileWidgets.

    Attributes
    ----------
    self.files : list(str)
        list representing paths to user-selected files
    widgets : list(FileWidgets)
        list of FileWidgets which correspond to elements of files
    window : MainWindow
        reference to instance of MainWindow

    Methods
    -------
    add_file(file):
        Appends file to files and re-draws FileWidgets.
    clear_all():
        Deletes all FileWidgets from widgets and stops displaying them.
    draw_widgets():
        Deletes and re-makes FileWidgets based on files.
    remove_file(index):
        Removes element by index from files and re-draws FileWidgets.
        Removes element by index from files and re-draws FileWidgets.
    move_up(index):
        Moves element by index from files up by one position in files
        and re-draws FileWidgets.
    move_down(index):
        Moves element by index from files down by one position in files
        and re-draws FileWidgets.
    """

    files = []
    widgets = []

    def __init__(self, window):
        self.window = window

    def add_file(self, file):
        self.files.append(file)
        self.draw_widgets()

    def clear_all(self):
        # Unpacks and removes all FileWidgets but does not change files.
        for widget in self.widgets:
            widget.pack_forget()
            widget.destroy()
        self.widgets = []

    def draw_widgets(self):
        # Clears old FileWidgets.
        self.clear_all()

        # Creates new FileWidget for each file in files.
        for i in range(len(self.files)):
            file = self.files[i]
            new_widget = FileWidget(self.window.inner_frame, self,
                                    file, i)
            new_widget.pack(side='top', fill='x', padx=5, pady=5)
            self.widgets.append(new_widget)

    def remove_file(self, index):
        del self.files[index]
        self.draw_widgets()

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
    """
    This class creates a merged PDF from files and
    saves it in output_folder.

    Attributes
    ----------
    files : list(str)
        list representing paths to user-selected files
    output_folder : str
        path to user-selected output folder
    temp_path : str
        path to directory used to store converted, unmerged PDF files

    Methods
    -------
    make_temp_folder():
        Creates new directory in output_folder directory named
        'temp' or 'temp_i' where i is some number. Returns path to
        new directory.
    make_temp_PDFs():
        Creates new PDF file in temp_path directory for each
        file in files.
    merge_temp_PDFs():
        Combines all PDFs in temp_path directory into a single
        multi-page PDF written to output_folder directory.
    delete_temp():
        Recursively deletes temp_path directory.
    static int_from_filename(filename):
        Returns int corresponding to the numeric portion of filename.
    """

    def __init__(self, files, output_folder):
        self.files = files
        self.output_folder = output_folder
        self.temp_path = self.make_temp_folder()
        self.make_temp_PDFs()
        self.merge_temp_PDFs()
        self.delete_temp()

    def make_temp_folder(self):
        # Checks if directory named 'temp' exists in output_folder.
        # If it does exist, checks whether 'temp_0' exists. Continues
        # to check whether temp_name directory exists, incrementing
        # numeric portion of temp_name each time.
        #
        # This ensures an existing directory isn't written over or
        # deleted.
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
            img_path = self.files[i]
            file_name, extension = os.path.splitext(img_path)

            # Checks whether file type is HEIC or PDF. If so, deals
            # with the file accordingly.
            if extension.lower() == '.heic':
                # Uses pyheif to load HEIC file into
                # PIL.Image instance.
                if not pyheif_imported:
                    raise ImportError('pyheif package required '
                                      'for converting HEIF files')
                heif_file = pyheif.read(img_path)
                pil_image = Image.frombytes(heif_file.mode,
                                            heif_file.size,
                                            heif_file.data,
                                            'raw',
                                            heif_file.mode,
                                            heif_file.stride)
            elif extension.lower() == '.pdf':
                # Image file is already in PDF format, so the file
                # can be copied directly to temp_path directory.
                with open(img_path, 'rb') as in_file,\
                     open(pdf_path, 'wb') as out_file:
                    out_file.write(in_file.read())
                    continue
            else:
                # For all other file types, load image into PIL.Image.
                pil_image = Image.open(img_path)

            # Converts image to PDF and saves it in temp_folder.
            pil_image = pil_image.convert('RGB')
            pil_image.save(pdf_path)

    def merge_temp_PDFs(self):
        files = os.listdir(self.temp_path)
        # Sorts files by the numeric portion of filename.
        files.sort(key=self.int_from_filename)

        merger = PyPDF2.PdfFileMerger()
        for file in files:
            file_path = os.path.join(self.temp_path, file)
            merger.append(file_path)

        # Finds unused filename in output_folder to name new
        # PDF. See make_temp_folder comment for detailed explanation.
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
        # Deletes tmp_path directory and all of its contents.
        rmtree(self.temp_path)

    @staticmethod
    def int_from_filename(filename):
        # Slicing with [:-4] removes '.pdf' from filename.
        return int(filename[:-4])


def requirements():
    """
    Prints all required packages.
    """

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
    """
    Takes tkinter.Tk instance, brings GUI window to top of screen.
    Only tested on OS X, so may not work as expected on Windows
    or Linux.
    """

    # Uses different ways to focus on window depending on
    # operating system.
    if platform() == 'Darwin':  # How Mac OS X is identified by Python
        os.system('/usr/bin/osascript -e \'tell app "Finder" to set '
                  'frontmost of process "Python" to true \'')
    else:  # All other operating systems
        window.focus_force()
        window.focus_set()
        window.focus()
        window.lift()


def main():
    """
    Runs program.
    """

    # Allows program to accept commandline arguments. Valid arguments
    # are '-h'/'--help' and '-r'/'--requirements'.
    parser = ArgumentParser(description='Merges image files of various '
                                        'formats to a multi-page PDF.')
    parser.add_argument('-r', '--requirements', action='store_true',
                        help='display all required packages and exit',
                        default=False)

    args = parser.parse_args()
    if args.requirements:
        requirements()

    window = MainWindow()
    focus_window(window)
    window.mainloop()


if __name__ == '__main__':
    main()
