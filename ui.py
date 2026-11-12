from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from actions import ConverterActions
from app_logger import write_app_log
from converters import TARGETS


class FileConverter(ConverterActions):

    def __init__(self, root):
        self.root = root
        self.OpenedFile = None
        self.SaveFile = None
        self.busy = False

        root.title("File Converter")

        mainframe = ttk.Frame(root, padding=(12))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Label(mainframe, text="File Converter").grid(
            column=0, row=0, columnspan=6, sticky=(W, E)
        )

        ttk.Label(mainframe, text="From").grid(column=0, row=1, sticky=(W, E))
        self.fromFormat = StringVar()
        self.fromConvert = ttk.Combobox(
            mainframe, textvariable=self.fromFormat, state="readonly", width=8
        )
        self.fromConvert.grid(column=1, row=1, sticky=(W, E))
        self.fromConvert["values"] = tuple(TARGETS)
        self.fromConvert.bind("<<ComboboxSelected>>", self.update_to_formats)

        ttk.Label(mainframe, text="To").grid(column=2, row=1, sticky=(W, E))
        self.toFormat = StringVar()
        self.toConvert = ttk.Combobox(
            mainframe, textvariable=self.toFormat, state="readonly", width=8
        )
        self.toConvert.grid(column=3, row=1, sticky=(W, E))
        self.toConvert["values"] = ()

        ttk.Label(mainframe, text="Input file:").grid(column=0, row=2, sticky=(W, E))
        self.OpenPath = StringVar()
        self.openPathLabel = ttk.Label(mainframe, textvariable=self.OpenPath, width=36)
        self.openPathLabel.grid(column=1, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Open File", command=self.open_file).grid(
            column=2, row=2, sticky=(W, E)
        )

        ttk.Label(mainframe, text="Output path:").grid(column=0, row=3, sticky=(W, E))
        self.SavePath = StringVar()
        self.savePathLabel = ttk.Label(mainframe, textvariable=self.SavePath, width=36)
        self.savePathLabel.grid(column=1, row=3, sticky=(W, E))
        ttk.Button(mainframe, text="Save Path", command=self.save_file).grid(
            column=2, row=3, sticky=(W, E)
        )

        self.convertButton = ttk.Button(mainframe, text="Convert", command=self.convert)
        self.convertButton.grid(column=1, row=4, sticky=(W, E))

        ttk.Label(mainframe, text="Status:").grid(column=0, row=5, sticky=(W, E))
        self.status = StringVar(value="waiting")
        ttk.Label(mainframe, textvariable=self.status).grid(
            column=1, row=5, columnspan=5, sticky=(W, E)
        )

        ttk.Label(mainframe, text="Log:").grid(column=0, row=6, sticky=(W, E))
        self.logBox = ScrolledText(mainframe, height=8, wrap="word", state="disabled")
        self.logBox.grid(column=0, row=7, columnspan=6, sticky=(N, W, E, S))

        root.minsize(700, 380)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        for column in range(6):
            mainframe.columnconfigure(column, weight=1)
        mainframe.rowconfigure(7, weight=1)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        write_app_log("Application started")
