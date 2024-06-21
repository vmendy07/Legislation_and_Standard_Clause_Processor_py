import pymupdf
import re
import csv

doc = pymupdf.open("PER.pdf")  # open a document
section_headers = []  # list to store section headers
last_known_header = ""  # variable to store the last known header

# function to convert roman numeral to integer
def roman_to_int(s):
    roman_values = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000}
    total = 0
    prev_value = 0
    for char in reversed(s):
        current_value = roman_values[char.lower()]
        if current_value >= prev_value:
            total += current_value
        else:
            total -= current_value
        prev_value = current_value
    return total

# function to detect requirement types
def detect_requirement_types(text):
    words_found = []
    if re.search(r'\bmust\b', text, re.IGNORECASE):
        words_found.append("must")
    if re.search(r'\bshall\b', text, re.IGNORECASE):
        words_found.append("shall")
    if re.search(r'\bshould\b', text, re.IGNORECASE):
        words_found.append("should")
    
    # # debugging output
    # print(f"Text: {text[:100]}...")  # print first 100 characters of the text
    # print(f"Words found: {words_found}")
    
    return words_found

# function to create sub identity
def create_sub_identity(section_number, numeric_index, alpha_index, roman_index):
    sub_identity = section_number
    if numeric_index:
        sub_identity += '.' + numeric_index.strip('()')
    if alpha_index:
        sub_identity += '.' + alpha_index.strip('()')
    if roman_index:
        sub_identity += '.' + roman_index.strip('()')
    return sub_identity

for page in doc:  # iterate the document pages
    text = page.get_text("text")  # get structured text
   
    # regular expression pattern to match section headers
    pattern = r"\n\s*(?:([A-Z][a-zA-Z0-9 \n'(),']*?)\n)?(\d{1,4}|100)\."
   
    # split the text into sections based on the pattern
    sections = re.split(pattern, text)
   
    # extract section headers, numbers, and corresponding text
    for i in range(1, len(sections), 3):
        section_header = sections[i].strip() if sections[i] else ""
        section_number = sections[i+1]
        section_text = sections[i+2].strip() if sections[i+2] else ""
        
        # replace "—(<number/letter/roman>)" or "(<number/letter/roman>)" with "(<number/letter/roman>)" at the start of section text
        section_text = re.sub(r"^[—–-]?\s*(\(\d+\)|\([a-h]\)|\([ivxlcdm]+\))", r"\1", section_text)
       
        # remove any spaces at the start of section text
        section_text = re.sub(r"^\s+", "", section_text)
       
        # assign the last known header if no header is present
        if not section_header:
            section_header = last_known_header
        else:
            last_known_header = section_header
        
        # split the section text into sub-sections based on the sub-index pattern (numeric, alphabetic a-h, or roman)
        sub_sections = re.split(r"(\(\d+\)|\([a-z]\)|\([ivxlcdm]+\))", section_text)
        
        # process each sub-section
        if len(sub_sections) > 1:
            current_numeric_index = None
            current_alpha_index = None
            current_roman_index = None
            current_text = ""

            for j in range(1, len(sub_sections)):
                if re.match(r"\(\d+\)", sub_sections[j]):
                    # If we encounter a new numeric index, save the previous sub-section (if any) and start a new one
                    if current_text:
                        sub_identity = create_sub_identity(section_number, current_numeric_index, current_alpha_index, current_roman_index)
                        section_headers.append((section_header, sub_identity, current_text.strip()))
                    current_numeric_index = sub_sections[j]
                    current_alpha_index = None
                    current_roman_index = None
                    current_text = ""
                elif re.match(r"\([a-z]\)", sub_sections[j]):
                    current_alpha_index = sub_sections[j]
                elif re.match(r"\([ivxlcdm]+\)", sub_sections[j]):
                    current_roman_index = sub_sections[j]
                else:
                    current_text += sub_sections[j]

            # Add the last sub-section
            if current_text:
                sub_identity = create_sub_identity(section_number, current_numeric_index, current_alpha_index, current_roman_index)
                section_headers.append((section_header, sub_identity, current_text.strip()))
        else:
            # If there are no sub-sections, add the entire section with just the section number
            section_headers.append((section_header, section_number, section_text))

# open a CSV file for writing
with open("clause_info.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
   
    # write the header row
    writer.writerow(["section", "clause_number", "clause_text", "requirement_type"])
   
    # write the section information and words found to the CSV file
    for header, sub_identity, text in section_headers:
        # detect requirement types
        words_found = detect_requirement_types(text)
       
        if words_found:  # Write the row if any requirement type is found
            # replace newline characters with spaces in the section header and text
            header = header.replace("\n", " | ")
            text = text.replace("\n", " ")
           
            # write the section information and words found to the CSV file
            writer.writerow([
                header, 
                sub_identity,
                text, 
                ", ".join(words_found)
            ])

print("Processing complete. Check the CSV file.")