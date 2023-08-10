import os

for file in os.listdir("./editedImgs"):
    os.remove(f"./editedImgs/{file}")