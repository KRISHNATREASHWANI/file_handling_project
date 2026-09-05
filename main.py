from pathlib import Path
import os

def createfile():
    try:
        name = input("please tell  your file name :- ")
        path = Path(name)
        if not path.exists():
            with open(path,"w") as fs:
                data = input("what you want to write: ")
                fs.write(data)
            print("file created successfully")
        else:
            print("file already exist")
    except Exception as err:
        print(f"an errot occured as {err}")

def readfile():
    try:
        name = input("enter the name of the file")
        path = Path(name)
        if path.exists():
            with open(path,"r") as fs:
                content = fs.read
                print(f"your file content is \n {content}")
        else:
            print("error no such file exists")
    except Exception as err:
        print(f"an error occured as {err}")


def updatefile():
    try:
        name = input("enter the name of the file")
        path = Path(name)
        if path.exists():
            print("opertation")
            print("1. rename the file")
            print("2. appending the content")
            print("3. overwritting the file")

            choice = int(input("enter your option"))
            if choice == 1:
                newname = input("tell yout new file name:- ")
                new_path = Path(newname)
                if not new_path.exists():
                    path.rename(new_path)
                    print("path rename successfully")
                else:
                    print("file already exists")
            elif choice == 2:
                with open(path,'a') as fs:
                    data = input("what you want to append")
                    fs.write("\n" + data)
                print("append successfully")
            elif choice == 3:
                with open(path,'w') as fs:
                     data = input("what you want to overwrite")
                     fs.write("\n" + data)
                print("overwrite successfully")
    except Exception as err:
        print(f"an error occured {err}")


def deletefile():
    try:
        name = input("tell your file name")
        path = Path(name)
        if path.exists():
            path.unlink()
            print("file deleted successfully")
        else:
            print("error no such file exists")
    except Exception as err:
        print(f"an error occured {err}")



print("press 1 for creating a file")
print("press 2 for reading a file")
print("press 3 for update a file")
print("press 4 for delete a file ")

a = input("\ntell your response:- ")

if a == 1:
    createfile()
if a == 2:
    readfile()
if a == 3:
    updatefile()
if a ==4 :
    deletefile()