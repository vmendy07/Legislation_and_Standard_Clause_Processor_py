# Legislation and Standards Clause Processor

This program is designed to process legislation and standards documents, specifically the Pressure Equipment (Safety) Regulations (PER), and extract clauses along with their associated metadata. The program reads the PER document in PDF format, parses the clause text and clause numbers, determines the type of requirement (must, shall, or should), and exports the extracted information to a CSV file.

## Features

- PDF Processing: The program uses the `pymupdf` library to open and read the PER document in PDF format. It iterates through each page of the document and extracts the structured text.

- Clause Parsing: Regular expressions are used to split the text into sections based on section headers and section numbers. The program extracts section headers, section numbers, and the corresponding text for each section. If a section header is missing, the program assigns the last known header to maintain consistency. The section text is further split into sub-sections based on sub-index patterns (numeric, alphabetic a-h, or roman numerals). Each sub-section is processed to extract the clause text and clause numbers.

- Requirement Type Determination: The program defines a function called `detect_requirement_types()` to determine the type of requirement for each clause. It searches for the presence of the words "must," "shall," or "should" (case-insensitive) in the clause text using regular expressions. The function returns a list of the requirement types found in the clause text.

- CSV Export: The program opens a CSV file named "clause_info.csv" for writing. It writes a header row to the CSV file with the column names: "section," "clause_number," "clause_text," and "requirement_type." For each clause, the program writes a row to the CSV file containing the section header, clause number, clause text, and the requirement types found. Newline characters in the section header and clause text are replaced with spaces to ensure proper formatting in the CSV file.

- Reusability and Repeatability: The program is designed with reusability and repeatability in mind. It uses modular functions to encapsulate specific tasks and make the code more readable and maintainable. The code is structured in a way that allows for easy modification and adaptation to process similar documents with different formats or requirements.

## Requirements

- Python 3.x
- `pymupdf` library

## Usage

1. Install the required dependencies by running the following command:
   ```
   pip install pymupdf
   ```

2. Place the Pressure Equipment (Safety) Regulations (PER) document in PDF format in the same directory as the program file.

3. Run the program using the following command:
   ```
   python clause_processor.py
   ```

4. The program will process the PER document and extract the clauses along with their metadata.

5. The extracted information will be exported to a CSV file named "clause_info.csv" in the same directory.

## Future Enhancements

- Improving the accuracy of section and clause parsing by handling more complex document structures and edge cases.
- Adding error handling and logging to gracefully handle any exceptions or unexpected scenarios during the processing.
- Implementing a command-line interface or graphical user interface to allow users to input the PDF file path and specify output options.
- Extending the program to support processing multiple PDF files in a batch mode.
- Enhancing the requirement type detection by considering additional keywords or patterns specific to the domain.

~ Vincent Mendy
