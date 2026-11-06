from pathlib import Path
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk

import csv
import json

import pypandoc


class FileConverter:

    TARGETS = {
        "csv": ("json",),
        "json": ("csv",),
        "docx": ("txt", "odt"),
        "txt": ("docx",),
        "odt": ("docx",),
    }

    def __init__(self, root):

        self.OpenedFile = None
        self.SaveFile = None

        root.title("File Converter")

        mainframe = ttk.Frame(root, padding=(12))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Label(mainframe, text="FileConverter").grid(column=1, row=0, sticky=(N))


        ttk.Label(mainframe, text="From").grid(column=2, row=0, sticky=(N))

        self.fromFormat = StringVar()
        self.fromConvert = ttk.Combobox(mainframe, textvariable=self.fromFormat, state="readonly")
        self.fromConvert.grid(column=3, row=0, sticky=(N))
        self.fromConvert['values'] = tuple(self.TARGETS)
        self.fromConvert.bind("<<ComboboxSelected>>", self.update_to_formats)

        ttk.Label(mainframe, text="To").grid(column=4, row=0, sticky=(N))

        self.toFormat = StringVar()
        self.toConvert = ttk.Combobox(mainframe, textvariable=self.toFormat, state="readonly")
        self.toConvert.grid(column=5, row=0, sticky=(N))
        self.toConvert['values'] = ()

        ttk.Label(mainframe, text="File To Convert: ").grid(column=0, row=1, sticky=(N, W, E, S))
        self.OpenPath = StringVar()
        ttk.Label(mainframe, textvariable=self.OpenPath).grid(column=1, row=1, sticky=(N, W, E, S))
        ttk.Button(mainframe, text="Open File", command=self.openfile).grid(column=2, row=1, sticky=(N, W, E, S))
        
        ttk.Label(mainframe, text="Path Output: ").grid(column=0, row=2, sticky=(N, W, E, S))
        self.SavePath = StringVar()
        ttk.Label(mainframe, textvariable=self.SavePath).grid(column=1, row=2, sticky=(N, W, E, S))
        ttk.Button(mainframe, text="Save Path", command=self.savefile).grid(column=2, row=2, sticky=(N, W, E, S))

        ttk.Button(mainframe, text="Convert", command=self.convert).grid(column=1, row=3, sticky=(N, W, E, S))


        # #self.feet = StringVar()
        # feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        # feet_entry.grid(column=2, row=1, sticky=(W, E))
        # #self.meters = StringVar()

        # #ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        # ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)

        # ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        # ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        # ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=1)
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        # feet_entry.focus()
        #root.bind("<Return>", self.calculate)
    def openfile(self):
        try:
            path = askopenfilename()
            if not path:
                print("Open cancelled: no input file selected")
                return
            self.OpenedFile = path
            self.OpenPath.set(path)
        except Exception as e:
            print(e)

    def savefile(self):
        try:
            target_format = self.toFormat.get()
            if not target_format:
                print("Error: choose a To format before saving")
                return

            if self.OpenedFile:
                initialfile = f"{Path(self.OpenedFile).stem}.{target_format}"
            else:
                initialfile = f"output.{target_format}"

            path = asksaveasfilename(
                defaultextension=f".{target_format}",
                filetypes=[
                    (f"{target_format.upper()} files", f"*.{target_format}")
                ],
                initialfile=initialfile,
            )
            if not path:
                print("Save cancelled: no output path selected")
                return

            path = Path(path)
            if path.suffix.lower().lstrip(".") != target_format:
                path = path.with_suffix(f".{target_format}")

            self.SaveFile = str(path)
            self.SavePath.set(self.SaveFile)
        except Exception as e:
            print(e)

    def update_to_formats(self, event=None):
        targets = self.TARGETS[self.fromFormat.get()]
        self.toConvert['values'] = targets
        self.toFormat.set(targets[0])

    def validate(self, key):
        source_format, target_format = key

        if not source_format:
            print("Error: choose a From format")
            return False
        if not target_format:
            print("Error: choose a To format")
            return False
        if source_format not in self.TARGETS:
            print(f"Error: unknown From format '{source_format}'")
            return False
        if target_format not in self.TARGETS[source_format]:
            print(f"Error: cannot convert {source_format} to {target_format}")
            return False

        if not self.OpenedFile:
            print("Error: choose an input file")
            return False
        if not self.SaveFile:
            print("Error: choose an output path")
            return False

        source = Path(self.OpenedFile)
        target = Path(self.SaveFile)

        if not source.is_file():
            print(f"Error: input file not found: {source}")
            return False

        source_ext = source.suffix.lower().lstrip(".")
        target_ext = target.suffix.lower().lstrip(".")

        if source_ext != source_format:
            print(
                f"Error: input file is .{source_ext}, but From is set to {source_format}"
            )
            return False
        if target_ext != target_format:
            print(
                f"Error: output file is .{target_ext or '(no extension)'}, "
                f"but To is set to {target_format}"
            )
            return False

        return True

    def csv_to_json(self):
        with open(self.OpenedFile, mode='r', newline='', encoding='utf-8') as csvfile:
            data = list(csv.DictReader(csvfile))

        with open(self.SaveFile, mode='w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4)

    def json_to_csv(self):
        with open(self.OpenedFile, mode='r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

        with open(self.SaveFile, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def convert(self):
        converters = {
            ("csv", "json"): self.csv_to_json,
            ("json", "csv"): self.json_to_csv,
            ("docx", "txt"): lambda: pypandoc.convert_file(self.OpenedFile, "plain", outputfile=self.SaveFile),
            ("txt", "docx"): lambda: pypandoc.convert_file(self.OpenedFile, "docx", format="plain", outputfile=self.SaveFile),
            ("docx", "odt"): lambda: pypandoc.convert_file(self.OpenedFile, "odt", outputfile=self.SaveFile),
            ("odt", "docx"): lambda: pypandoc.convert_file(self.OpenedFile, "docx", outputfile=self.SaveFile),
        }
        try:
            key = (self.fromFormat.get(), self.toFormat.get())
            if not self.validate(key):
                return
            converters[key]()
            print(f"Done: {self.OpenedFile} -> {self.SaveFile}")
        except Exception as e:
            print(f"Conversion failed: {e}")
        
    # def calculate(self, *args):
    #     try:
    #         value = float(self.feet.get())
    #         self.meters.set(round(0.3048 * value, 4))
    #     except ValueError:
    #         pass

root = Tk()
root.geometry('450x400')
FileConverter(root)
root.mainloop()

# from tkinter import *
# from tkinter.filedialog import *

# Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# files = [('All Files', '*.*'), 
#              ('Python Files', '*.py'),
#              ('Text Document', '*.txt')]
# filename = asksaveasfile(filetypes = files, defaultextension = files)
# print(filename)
