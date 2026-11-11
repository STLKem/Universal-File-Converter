import threading
from tkinter import END
from tkinter.filedialog import askopenfilename, asksaveasfilename

from converters import TARGETS, convert, validate
from utils import default_output_name, ensure_extension, shorten_path


class ConverterActions:

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
                self.log("Open canceled: no input file selected")
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
                self.log("Save canceled: no output path selected")
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
            self.root.after(0, self.on_convert_error, str(e))
        else:
            self.root.after(
                0,
                self.on_convert_done,
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
