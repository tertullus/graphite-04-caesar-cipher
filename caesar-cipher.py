import string
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class Caesar:
    def __init__(self):
        self.__key = int(input("Enter your cipher key: "))
        self.__letters = {v: (k + 1)
                          for k, v in enumerate(string.ascii_lowercase)}
        self.__reverse_letters = {v: k for k, v in self.__letters.items()}

    def read_pdf(self, plain_file):
        with open(plain_file, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            pdf_text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                pdf_text += page.extract_text() + "\n"
        return pdf_text

    def save_text_to_pdf(self, pdf_text, output_pdf_file):
        c = canvas.Canvas(output_pdf_file, pagesize=letter)
        width, height = letter

        lines = pdf_text.split('\n')
        y_position = height - 50

        for line in lines:
            if y_position < 50:
                c.showPage()
                y_position = height - 50
            c.drawString(50, y_position, line)
            y_position -= 15

        c.save()

    def encrypt(self, plain_file, code_file):
        pdf_text = self.read_pdf(plain_file)
        temp = ""
        encrypted_char = ""
        for char_index in range(len(pdf_text)):
            char = pdf_text[char_index]
            if char.isalpha():
                lower_char = char.lower()
                shifted_index = (
                    self.__letters[lower_char] + self.__key) % len(self.__letters)
                if shifted_index == 0:
                    shifted_index = len(self.__letters)
                encrypted_char = self.__reverse_letters[shifted_index]
                if char.isupper():
                    temp += encrypted_char.upper()
                else:
                    temp += encrypted_char
            else:
                temp += char
        self.save_text_to_pdf(temp, code_file)

    def decrypt(self, code_file, new_plain_file):
        pdf_text = self.read_pdf(code_file)
        temp = ""
        decrypted_char = ""
        for char_index in range(len(pdf_text)):
            char = pdf_text[char_index]
            if char.isalpha():
                lower_char = char.lower()
                shifted_index = (
                    self.__letters[lower_char] - self.__key) % len(self.__letters)
                if shifted_index == 0:
                    shifted_index = len(self.__letters)
                decrypted_char = self.__reverse_letters[shifted_index]
                if char.isupper():
                    temp += decrypted_char.upper()
                else:
                    temp += decrypted_char
            else:
                temp += char
        self.save_text_to_pdf(temp, new_plain_file)


plain_file = "./plain_file.pdf"
code_file = "./code_file.pdf"
new_plain_file = "./new_plain_file.pdf"

sample = Caesar()
sample.encrypt(plain_file, code_file)
sample.decrypt(code_file, new_plain_file)
