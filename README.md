# README for COMP26120 LAB 4 Submission

## Author
Mohamed Farid Patel - e60822mp

## Introduction
This repository contains the source code for the LAB 4 assignment on Register Allocation using Graph Colouring for the COMP26120 course. The main objective of this assignment is to implement a graph colouring algorithm that assigns registers (represented as colours) to nodes in an interference graph, ensuring that no two adjacent nodes share the same register.

## Prerequisites
- Python 3.x installed on your system.

## Files
- `plplab.py`: The Python script that contains the implementation of the graph colouring algorithm.
- `README.md`: This file, providing instructions on how to run the code.

## Running the Code
To run the code, you will need an input file that describes the interference graph and a name for the output file where the register allocations will be written.

### Format of the Input File
The input file should list the interference graph's nodes. Each line corresponds to a node, starting with the node's number, followed by the numbers of all nodes it interferes with, separated by commas. For example:
```
1,2,3,4
2,4,1
3,1
4,1,2
```
### Command to Run
Navigate to the directory containing `plplab.py` and use the following command in your terminal or command prompt:
```
python3 plplab.py <input_file.txt> <output_file.txt>
```
Replace `<input_file.txt>` with the path to your input file and `<output_file.txt>` with the desired path for the output file.

### Example
To test with a file named `testfile.txt` and write the output to `outputfile.txt`, the command would be:
```
python3 plplab.py testfile.txt outputfile.txt
```

## Output
The script will write the register allocations to the output file specified in the command line. Each line in the output file will contain a node number and its assigned register (colour), for example:
```
1A
2B
3B
4C
```

## Troubleshooting
Ensure your input file is correctly formatted and does not contain any characters other than digits, commas, and end-of-line characters. If you encounter any issues, verify that Python 3.x is properly installed and accessible from your terminal or command prompt.

---

Feel free to adjust the README as necessary to match the specifics of your project or any additional details you'd like to include.
