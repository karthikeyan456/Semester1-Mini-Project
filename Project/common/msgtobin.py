def msgtobin(data):
    #Function to convert the message into a binary string
    binstr=""
    for char in data:
        binstr+=format(ord(char),"08b")
    
    return binstr
