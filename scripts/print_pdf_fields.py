#!/bin/env python3

from pdfrw import PdfReader
import sys

pdf = PdfReader(sys.argv[1])

fieldnames = [x['/T'] for x in pdf.Root.AcroForm.Fields]

for index, item in enumerate(fieldnames):
    print(item)
    # print(item, pdf.Root.AcroForm.Fields[index])
