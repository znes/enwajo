from model import run
from tkinter import filedialog

scenario = filedialog.askdirectory(title='Please select scenario folder')

run(scenario)
