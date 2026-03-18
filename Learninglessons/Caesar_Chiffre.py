text = input("Geben Sie Ihren Text ein: ")
offset = int(input("Um wieviel willst du deinen Text verschieben? "))

def chiffre(text, offset):
    result = ""
    for char in text:
        if 'a' <= char <= 'z':
            result += chr((ord(char) - ord('a') + offset) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            result += chr((ord(char) - ord('A') + offset) % 26 + ord('A'))
        else:
            result += char
    return result

encrypted = chiffre(text, offset)
print("Verschlüsselt:", encrypted)

decrypted = chiffre(encrypted, -offset)
print("Entschlüsselt:", decrypted)
