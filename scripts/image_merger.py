#!/usr/bin/env python3

"""
Author: Ben Ralston
Date: 2020-11-19

Description: This program accepts images of various formats input by a
user and generates a PDF of the merged images.
"""

import os
import sys
import tkinter as tk
import tkinter.filedialog
from argparse import ArgumentParser
from shutil import rmtree
from platform import system as platform

import PyPDF2
from PIL import Image, UnidentifiedImageError
try:
    import pyheif
    pyheif_imported = True
except ImportError:
    pyheif_imported = False


class MainWindow(tk.Tk):
    """Subclass of tkinter.Tk which holds all elements of the GUI.

    Attributes:
        output_folder (str): Path to user-selected output folder.
        files (FileList): Stores user-selected files.
        left_frame (tkinter.Frame): Frame occupying left side of window
            with parent self.
        right_frame (tkinter.Frame): Frame occupying right side of
            window with parent self.
        canvas (tkinter.Canvas): Scrollable Canvas with parent
            left_frame.
        inner_frame (tkinter.Frame): Frame with parent canvas, holds all
            FileWidgets.
        folder_label (tkinter.Label): Label with parent right_frame,
            displays output_folder as text.

    """

    def __init__(self, **kwargs):
        """Creates children of main window and initializes attributes.

        Args:
            **kwargs: Arbitrary keyword arguments.

        """
        tk.Tk.__init__(self, **kwargs)

        # output_folder represents the directory at which the merged
        # PDF will be saved.
        self.output_folder = None
        self.files = FileList(self)

        # Fix window size to constant value.
        size_x, size_y, pos_x, pos_y = 600, 500, 100, 100
        self.wm_geometry('%dx%d+%d+%d' % (size_x, size_y, pos_x, pos_y))
        self.resizable(0, 0)

        self.title('Image Merger')

        # Create two tkinter.Frames and one tkinter.Canvas which are
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

        # Create tkinter.Scrollbar (which is not saved as a class
        # attribute because it is never accessed after __init__).
        scrollbar = tk.Scrollbar(self.left_frame, orient='vertical',
                                 command=self.canvas.yview)

        # Assign scrollbar to canvas, creating scrollable region,
        # and pack into left_frame.
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Don't fully understand what this does, but it helps create
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

        # Create three Buttons which control file selection,
        # merging into PDF, and output folder selection. Pack them
        # into right_frame.
        tk.Button(master=self.right_frame, command=self.select_files,
                  text='Select Files').pack(side='top', pady=(14, 20))
        tk.Button(master=self.right_frame, command=self.merge_files,
                  text='Merge Into PDF').pack(side='top', pady=20)
        tk.Button(master=self.right_frame, command=self.select_folder,
                  text='Select Output Folder').pack(side='top', pady=20)

        # Create Labels to display currently selected output folder.
        tk.Label(master=self.right_frame, text='Output Folder:')\
            .pack(side='top', pady=(5, 0), fill='x')
        self.out_label = tk.Label(master=self.right_frame, text='None',
                                  wraplength=185, justify='center')
        self.out_label.pack(side='top', pady=0, fill='x')

    def select_files(self):
        """Open file selection dialog and add selection to files."""
        files = tk.filedialog.askopenfilenames(multiple=True)
        for file in files:
            self.files.add_file(file)

    def merge_files(self):
        """Merge selected files into PDF saved in output_folder.

        Files are only merged if at least one file has been selected
        and the output folder has been specified by the user.

        """
        if self.files.files and self.output_folder:
            FileMerger(self.files.files, self.output_folder)

    def select_folder(self):
        """Open folder selection dialog and assign to output_folder.

        After the user has made a selection, the label showing the
        currently selected folder is updated.

        """
        self.output_folder = tk.filedialog.askdirectory()
        self.update_folder_text()

    def update_folder_text(self):
        """Update text of out_label."""
        if not self.output_folder:
            text = 'None'
        else:
            text = self.output_folder
        self.out_label.config(text=text)

    def configure_scroll(self, event):
        """Configure scroll area of canvas.

        Args:
            event (tkinter.Event): Unused parameter which is necessary
                to keep because an event will be passed to
                configure_scroll whenever it is called.

        """
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),
                              width=350, height=460)


class FileWidget(tk.Frame):
    """Representation of a single file the user has selected.

    Subclass of tkinter.Frame which stores a single file path
    and displays it as a widget with Up, Down, and Remove buttons.

    Attributes:
        file (str): Path to user-selected output folder.
        index (int): Index of corresponding file in FileList.files.

    """

    def __init__(self, parent_frame, file_class, file, index, **kwargs):
        """Initialize attributes and create buttons for widget.

        Args:
            parent_frame (tkinter.Frame): Parent of this object.
            file_class (FileList): Instance of FileList.
            file (str): Name of file to store.
            index (int): Position relative to other FileWidget objects.
            **kwargs: Arbitrary keyword arguments.

        """
        tk.Frame.__init__(self, parent_frame, highlightbackground='black',
                          highlightthickness=1, **kwargs)

        self.file = file
        # Represent index of corresponding file in FileList.list.
        self.index = index

        # This Label displays the filename portion of the full path.
        tk.Label(self, text=self.get_filename(file),
                 anchor='w').pack(side='left')

        # Create functions which call methods of FileList.
        def remove_lambda():
            """Call FileList.remove_file with argument index."""
            file_class.remove_file(self.index)

        def down_lambda():
            """Call FileList.move_down with argument index."""
            file_class.move_down(self.index)

        def up_lambda():
            """Call FileList.move_up with argument index."""
            file_class.move_up(self.index)

        # Create three buttons for moving up, moving down,
        # or removing FileWidgets.
        tk.Button(self, command=remove_lambda,
                  text='Remove').pack(side='right')
        tk.Button(self, command=down_lambda,
                  text='Down',).pack(side='right')
        tk.Button(self, command=up_lambda,
                  text='Up').pack(side='right')

    @staticmethod
    def get_filename(full_path):
        """Get filename portion of full_path.

        Args:
            full_path (str): Full path of a file.

        Returns:
            str: Filename portion of full_path.

            The filename is truncated if the entire filename would be
            too long to display.

        """
        last_break = None
        for i in range(len(full_path)):
            # Check whether current character is a path delimiter,
            # starting at end of path and moving backwards.
            if full_path[-1 - i] in ['/', '\\', ':']:
                last_break = -1 - i
                break

        # Assign the filename portion of full_path to file_name, or
        # assign all of full_path if no delimiter is found.
        if last_break is not None:
            file_name = full_path[last_break + 1:]
        else:
            file_name = full_path

        # Shorten file_name if file_name is too large.
        if len(file_name) > 20:
            return file_name[:17] + '...'
        else:
            return file_name


class FileList:
    """Storage container for user-selected files and FileWidgets.

    This class stores selected files and FileWidgets, displays
    FileWidgets in MainWindow.inner_frame, and handles any changes
    (movement up/down or deletion) to FileWidgets.

    Attributes:
        files (list of str): Paths to user-selected files.
        widgets (list of FileWidgets): List of FileWidgets which
            correspond to elements of files.
        window (MainWindow): Reference to instance of MainWindow.

    """

    def __init__(self, window):
        """Initialize files and widgets to empty lists.

        Args:
            window (MainWindow): Instance of MainWindow.

        """
        self.files = []
        self.widgets = []
        self.window = window

    def add_file(self, file):
        """Append file to files and re-draw FileWidgets.

        Args:
            file (str): Path of user-selected file.

        """
        self.files.append(file)
        self.draw_widgets()

    def clear_all(self):
        """Delete all FileWidgets and stop displaying them."""
        for widget in self.widgets:
            widget.pack_forget()
            widget.destroy()
        self.widgets = []

    def draw_widgets(self):
        """Delete and re-make FileWidgets based on files."""
        self.clear_all()  # Clear old FileWidgets.

        # Create new FileWidget for each file in files.
        for i in range(len(self.files)):
            file = self.files[i]
            new_widget = FileWidget(self.window.inner_frame, self,
                                    file, i)
            new_widget.pack(side='top', fill='x', padx=5, pady=5)
            self.widgets.append(new_widget)

    def remove_file(self, index):
        """Remove element by index from files and draw FileWidgets.

        Args:
            index (int): Index of file to remove.

        """
        del self.files[index]
        self.draw_widgets()

    def move_up(self, index):
        """Move specified file up by one position in files.

        Args:
            index (int): Index of file to move up.

        """
        if index == 0:  # Can't move file higher than the top position
            return
        to_move = self.files.pop(index)
        self.files.insert(index - 1, to_move)
        self.draw_widgets()

    def move_down(self, index):
        """Move specified file down by one position in files.

        Args:
            index (int): Index of file to move down.

        """
        if index + 1 == len(self.files):
            return
        to_move = self.files.pop(index)
        self.files.insert(index + 1, to_move)
        self.draw_widgets()


class FileMerger:
    """Constructor of merged PDF.

    This class creates a merged PDF from files and saves it in
    output_folder.

    Attributes:
        files (list of str): Strings representing paths to
            user-selected files.
        output_folder (str): Path to user-selected output folder.
        temp_path (str): Path to directory used to store converted,
            unmerged PDF files.

    """

    def __init__(self, files, output_folder):
        """Call class methods to create merged PDF.

        After initializing attributes, call the primary methods of this
        class in order to create the final merged PDF.

        Args:
            files (list of str): Files to merge.
            output_folder (str): Path of user-selected directory.

        """
        self.files = files
        self.output_folder = output_folder
        self.temp_path = self.make_temp_folder()
        self.make_temp_PDFs()
        self.merge_temp_PDFs()
        self.delete_temp()

    def make_temp_folder(self):
        """Create new directory without name conflict.

        The default name of the directory is 'temp'. Check if directory
        named 'temp' exists in output_folder. If it does exist, check
        whether 'temp_0' exists. Continue to check whether temp_name
        directory exists, incrementing numeric portion of temp_name each
        time. This ensures an existing directory isn't written over or
        deleted.

        Returns:
            str: Path to newly created directory.

        """
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
        """Convert and save each file in files to PDF format.

        The new PDFs are stored in the temp_path directory, with each
        named i.pdf where i is an int ranging from zero to one less than
        the length of files.

        """
        for i in range(len(self.files)):
            pdf_name = str(i) + '.pdf'
            pdf_path = os.path.join(self.temp_path, pdf_name)
            img_path = self.files[i]
            file_name, extension = os.path.splitext(img_path)
            base_name = os.path.basename(img_path)

            try:
                # Check whether file type is HEIC or PDF. If so, deals
                # with the file accordingly.
                if extension.lower() == '.heic':
                    # Use pyheif to load HEIC file into
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
                    try:
                        pil_image = Image.open(img_path)

                    # Error handling for when PIL cannot read file as image:
                    except UnidentifiedImageError:
                        print("Could not convert %s into PDF." % base_name)
                        continue

            # Error handling for when a file does not exist:
            except FileNotFoundError:
                print("%s does not exist." % base_name)
                continue

            # Error handling for all other exceptions:
            except:
                print("Something went wrong while converting %s." % base_name)
                continue

            # Convert image to PDF and save it in temp_folder.
            pil_image = pil_image.convert('RGB')
            pil_image.save(pdf_path)

    def merge_temp_PDFs(self):
        """Combine all temp PDFs into single merged PDF.

        Combine all PDFs stored in temp_path directory into a single
        multi-page PDF written to the output_folder directory.

        """
        files = os.listdir(self.temp_path)
        # Sort files by the numeric portion of filename.
        files.sort(key=self.int_from_filename)

        merger = PyPDF2.PdfFileMerger()
        for file in files:
            file_path = os.path.join(self.temp_path, file)
            merger.append(file_path)

        # Find unused filename in output_folder to name new
        # PDF. See make_temp_folder docstring for detailed explanation.
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

        # Clear memory usage and frees PDFs to be deleted.
        merger.close()

    def delete_temp(self):
        """Delete temp_path directory and all of its contents."""
        rmtree(self.temp_path)

    @staticmethod
    def int_from_filename(filename):
        """Return numeric portion of filename as int."""
        return int(filename[:-4])


def requirements():
    """Print all required packages and exit program."""
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
    """Bring window to top of screen.

    Note:
        Only tested on OS X, so may not work as expected on Windows or
        Linux.

    Args:
        window (tkinter.Tk): Window to focus on.

    """

    # Use different methods to focus on window depending on operating
    # system.
    if platform() == 'Darwin':  # Mac OS X
        os.system('/usr/bin/osascript -e \'tell app "Finder" to set '
                  'frontmost of process "Python" to true \'')

    else:  # All other operating systems
        window.focus_force()
        window.focus_set()
        window.focus()
        window.lift()


def main():
    """Run program."""
    parser = ArgumentParser(description='Merges image files of various '
                                        'formats to a multi-page PDF.')
    parser.add_argument('-r', '--requirements', action='store_true',
                        help='display all required packages and exit',
                        default=False)

    # Valid arguments are '-h'/'--help' and '-r'/'--requirements'.
    args = parser.parse_args()

    if args.requirements:
        requirements()

    window = MainWindow()
    focus_window(window)
    window.mainloop()


if __name__ == '__main__':
    main()
