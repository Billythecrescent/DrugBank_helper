# DrugBank_helper
It is a simple tool for users to crab drug data(name &amp; links) for a specific Indication (disease).

Windows/Linux are all supported.

Usage:

Python DrugBank_spider4.0.py [indication_name] [format]

indication_name:

&nbsp;&nbsp;&nbsp;&nbsp;  the name of the disease to be searched, with a space to split if multiple indications are needed. 

for example: 

&nbsp;&nbsp;&nbsp;&nbsp;  lung_cancer intestine_cancer 

format:

**csv**:

&nbsp;&nbsp;&nbsp;&nbsp;  If you want to output .csv format file.

**txt**:

&nbsp;&nbsp;&nbsp;&nbsp;  If you want to output .txt format file.
  
Case example:

Python DrugBank_spider4.0.py lung_cancer txt
