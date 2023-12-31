from pyfa_eftparser import PEFTParser


with open("./fits/[Leshak, TEST 4]", "r") as f:
    eft_block = f.read()

print(eft_block)

print(PEFTParser.split_blocks(eft_block))
