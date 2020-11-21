import os
import sys
import fnmatch
import numpy as np
import pandas as pd

symbols = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "SCREEN": 16384, "KBD": 24576, 
            "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7, "R8": 8,
            "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15}

destinationDict = {"":"000", "M": "001", "D": "010", "MD": "011", 
                "A": "100", "AM": "101", "AD": "110", "AMD": "111"}

codeDict ={"0" : "101010", "1" : "111111", "-1" : "111010", "D" : "001100", "A" : "110000", 
            "!D" : "001101", "!A" : "110001", "-D" : "001111", "-A" : "110011", "D+1" : "011111", 
            "A+1" : "110111", "D-1" : "001110", "A-1" : "110010", "D+A" : "000010", "D-A" : "010011", 
            "A-D" : "000111", "D&A" : "000000", "D|A" : "010101", "M" : "110000", "!M" : "110001", 
            "-M" : "110011", "M+1" : "110111", "M-1" : "110010", "D+M" : "000010", "D-M" : "010011", 
            "M-D" : "000111", "D&M" : "000000", "D|M" : "010101"}

jumpDict = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

class Assembler:
    '''
    Assembler Program used for converting Hack-Machine Language Code to Binary Format
    that can be burned into ROM unit and can be understood by "Hack CPU"
    '''

    def __init__(self, read_path, write_path):
        self.read_path = read_path
        self.write_path = write_path

    def content_extractor(self):
        content = []
        with open(self.read_path, 'r') as asm_file:
            lines = asm_file.readlines()
            for line in lines:
                if((not line.startswith('//')) and ("@" in line or "=" in line or "(" in line or ";" in line)):
                    if(line.find("//") != -1):
                        line = line[:line.find("//")]
                    line = line.replace('\n', '')
                    line = line.replace(" ", "")
                    content.append(line)
        return content
    
    def label_processor(self, content):
        labels = [element for element in content if "(" in element]
        label_counter = 1
        for label in labels:
            place = content.index(label) + 1 - label_counter
            new_symbol = label.replace("(", "")
            symbols[new_symbol.replace(")", "")] = place
            label_counter = label_counter + 1
        for label in labels:
            content.remove(label)
        return content
    
    def variable_processor(self, pure_content):
        variableless_content = []
        freeRamPointer = 16
        for instruction in pure_content:
            if(not instruction.startswith('@')):
                variableless_content.append(instruction)
            else:
                Aregister = instruction.replace("@", "")
                if(Aregister.isnumeric()):
                    variableless_content.append(instruction)
                else:
                    if(Aregister in list(symbols.keys())):
                        value = symbols[Aregister]
                        replacement = "@" + str(value)
                        variableless_content.append(replacement)
                    else:
                        symbols[Aregister] = freeRamPointer
                        replacement = "@" + str(freeRamPointer)
                        variableless_content.append(replacement)
                        freeRamPointer = freeRamPointer + 1
        return variableless_content
    
    def Ainstruction(self, Ainstr):
        get_bin = lambda x, n: format(x, 'b').zfill(n)
        binary_code = get_bin(int(Ainstr[1:]), 16)
        return binary_code
    
    def CParser(self, Cinstr):
        instruction_length = len(Cinstr)
        jump = ""
        code = ""
        dest = ""
        a = ""
        if((Cinstr.find(";") !=-1) & (Cinstr.find(";") != instruction_length-1)):
            jump = Cinstr[Cinstr.find(";")+1:]
            computation = Cinstr[:Cinstr.find(";")]
            if("=" in computation):
                dest = computation[:computation.find("=")]
                code = computation[computation.find("=")+1:]
            else:
                code = computation
        else:
            dest = Cinstr[:Cinstr.find("=")]
            code = Cinstr[Cinstr.find("=")+1:]
        if(code=="" or ("M" in code)):
            a = "1"
        else:
            a = "0" 
        return a, code, dest, jump
    
    def instruction_processor(self, variableless_content):
        binary_instructions = []
        for instruction in variableless_content:
            if(instruction.startswith('@')):
                Ainstr = self.Ainstruction(instruction)
                binary_instructions.append(Ainstr)
            else:
                a, code, dest, jump = self.CParser(instruction)
                code_binary = codeDict[code]
                dest_binary = destinationDict[dest]
                jump_binary = jumpDict[jump]
                Cinstr = "111" + a + code_binary + dest_binary + jump_binary
                binary_instructions.append(Cinstr)
        return binary_instructions

    def ASSEMBLEprocess(self):
        content = self.content_extractor()
        labelless_content = self.label_processor(content)
        variableless_content = self.variable_processor(labelless_content)
        hack_code = self.instruction_processor(variableless_content)
        with open(self.write_path, 'w') as hack_file:
            for binary in hack_code:
                line = binary + "\n"
                hack_file.write(line)
        # print(labelless_content)
        # print(variableless_content)
        # print(hack_code)
        # print(symbols.keys())
        # print(symbols.values())
    


def main():
    read_path = r'D:\Study\MPUsMCUs\nand2tetris\Solutions\Proj6\rect\RectL.asm'
    write_path = r'D:\Study\MPUsMCUs\nand2tetris\Solutions\Proj6\RectL.hack'
    assembler = Assembler(read_path, write_path)
    assembler.ASSEMBLEprocess()

if __name__ == "__main__":
    main()