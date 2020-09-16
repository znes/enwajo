from model import run
from tkinter import filedialog, Tk
import traceback

try:
    input("Press Enter to choose a scenario folder.")
    root = Tk()
    root.withdraw()
    scenario = filedialog.askdirectory(title='Please select scenario folder')
    root.destroy()
    run(scenario)
except:
    traceback.print_exc()
    print("Oops, something went wrong.")
    print("To get help: Post the whole output above in a new issue at:")
    print("https://github.com/znes/enwajo/issues")
    input("Then press Enter to exit.")
