import threading
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from converters import TARGETS, convert, validate
from utils import default_output_name, ensure_extension, shorten_path


class FileConverter:

    def __init__(self, root):
        self.root = root
        self.OpenedFile = None
        self.SaveFile = None
        self.busy = False

        root.title("File Converter")

        mainframe = ttk.Frame(root, padding=(12))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Label(mainframe, text="FileConverter").grid(column=1, row=0, sticky=(W, E))

        ttk.Label(mainframe, text="From").grid(column=2, row=0, sticky=(W, E))

        self.fromFormat = StringVar()
        self.fromConvert = ttk.Combobox(
            mainframe, textvariable=self.fromFormat, state="readonly", width=8
        )
        self.fromConvert.grid(column=3, row=0, sticky=(W, E))
        self.fromConvert["values"] = tuple(TARGETS)
        self.fromConvert.bind("<<ComboboxSelected>>", self.update_to_formats)

        ttk.Label(mainframe, text="To").grid(column=4, row=0, sticky=(W, E))

        self.toFormat = StringVar()
        self.toConvert = ttk.Combobox(
            mainframe, textvariable=self.toFormat, state="readonly", width=8
        )
        self.toConvert.grid(column=5, row=0, sticky=(W, E))
        self.toConvert["values"] = ()

        ttk.Label(mainframe, text="File To Convert: ").grid(column=0, row=1, sticky=(W, E))
        self.OpenPath = StringVar()
        self.openPathLabel = ttk.Label(mainframe, textvariable=self.OpenPath, width=36)
        self.openPathLabel.grid(column=1, row=1, sticky=(W, E))
        ttk.Button(mainframe, text="Open File", command=self.openfile).grid(
            column=2, row=1, sticky=(W, E)
        )

        ttk.Label(mainframe, text="Path Output: ").grid(column=0, row=2, sticky=(W, E))
        self.SavePath = StringVar()
        self.savePathLabel = ttk.Label(mainframe, textvariable=self.SavePath, width=36)
        self.savePathLabel.grid(column=1, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Save Path", command=self.savefile).grid(
            column=2, row=2, sticky=(W, E)
        )

        self.convertButton = ttk.Button(mainframe, text="Convert", command=self.convert)
        self.convertButton.grid(column=1, row=3, sticky=(W, E))

        ttk.Label(mainframe, text="Status:").grid(column=0, row=4, sticky=(W, E))
        self.status = StringVar(value="ожидание")
        ttk.Label(mainframe, textvariable=self.status).grid(
            column=1, row=4, columnspan=5, sticky=(W, E)
        )

        ttk.Label(mainframe, text="Log:").grid(column=0, row=5, sticky=(W, E))
        self.logBox = ScrolledText(mainframe, height=8, wrap="word", state="disabled")
        self.logBox.grid(column=0, row=6, columnspan=6, sticky=(N, W, E, S))

        root.minsize(700, 340)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        for column in range(6):
            mainframe.columnconfigure(column, weight=1)
        mainframe.rowconfigure(6, weight=1)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def log(self, message):
        self.logBox.configure(state="normal")
        self.logBox.insert(END, message + "\n")
        self.logBox.see(END)
        self.logBox.configure(state="disabled")

    def set_status(self, text):
        self.status.set(text)

    def open_file(self):
        try:
            path = askopenfilename()
            if not path:
                self.log("Open cancelled: no input file selected")
                return
            self.OpenedFile = path
            self.OpenPath.set(shorten_path(path))
            self.log(f"Input file selected: {path}")
        except Exception as e:
            self.set_status("error")
            self.log(str(e))

    def save_file(self):
        try:
            target_format = self.toFormat.get()
            if not target_format:
                self.set_status("error")
                self.log("Error: choose a To format before saving")
                return

            path = asksaveasfilename(
                filetypes=[(f"{target_format.upper()} files", f"*.{target_format}")],
                initialfile=default_output_name(self.OpenedFile, target_format),
            )
            if not path:
                self.log("Save cancelled: no output path selected")
                return

            self.SaveFile = ensure_extension(path, target_format)
            self.SavePath.set(shorten_path(self.SaveFile))
            self.log(f"Output path selected: {self.SaveFile}")
        except Exception as e:
            self.set_status("error")
            self.log(str(e))

    def update_to_formats(self, event=None):
        targets = TARGETS[self.fromFormat.get()]
        self.toConvert["values"] = targets
        self.toFormat.set(targets[0])

    def convert(self):
        if self.busy:
            self.log("Conversion already in progress")
            return

        source_format = self.fromFormat.get()
        target_format = self.toFormat.get()
        source_path = self.OpenedFile
        target_path = self.SaveFile

        error = validate(source_format, target_format, source_path, target_path)
        if error:
            self.set_status("error")
            self.log(error)
            return

        self.busy = True
        self.convertButton.configure(state="disabled")
        self.set_status("converting")
        self.log(f"Converting: {source_path} to {target_path}")

        worker = threading.Thread(
            target=self.convert_worker,
            args=(source_format, target_format, source_path, target_path),
            daemon=True,
        )
        worker.start()

    def convert_worker(self, source_format, target_format, source_path, target_path):
        try:
            convert(source_format, target_format, source_path, target_path)
        except Exception as e:
            self.root.after(0, self._on_convert_error, str(e))
        else:
            self.root.after(
                0,
                self._on_convert_done,
                f"Done: {source_path} to {target_path}",
            )

    def on_convert_done(self, message):
        self.busy = False
        self.convertButton.configure(state="normal")
        self.set_status("ready")
        self.log(message)

    def on_convert_error(self, message):
        self.busy = False
        self.convertButton.configure(state="normal")
        self.set_status("error")
        self.log(f"Conversion failed: {message}")
