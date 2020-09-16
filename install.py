import traceback
try:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r' 'requirements.txt'])
    print("Installation successful.")
    input("Press Enter to exit.")
except:
    traceback.print_exc()
    print("Oops, something went wrong.")
    print("To get help: Post the whole output above in a new issue at:")
    print("https://github.com/znes/enwajo/issues")
    input("Then press Enter to exit.")
    
