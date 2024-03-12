# README for COMP26120 LAB 4 Submission

## Author
Mohamed Farid Patel - e60822mp

## Introduction
In this repository, i have included my implementation of a graph coloring algorithm.
Please Read the full README before testing my code.

## Prerequisites
- You need to have Python 3 installed on your computer/desktop.

## Files
- `lab4plp.py`: The Python script containing the algorihtm.
- `README.md`: The instruction file.

## Input File Format
The input file should be of the form:
```
1,2,3,4
2,4,1
3,1
4,1,2
```
Where each line corresponds to a node, starting with the node's number, followed by the numbers of all its neighbours/conflicts.

For the above example, node 1 interferes with nodes 2, 3, and 4. Node 2 interferes with nodes 1 and 4. Node 3 interferes with nodes 1 and 4 interferes with nodes 1 and 2.

### Invalid Formats
Ensure your input file is correctly formatted and does not contain any characters other than digits & commas.
e.g. any variation of
```
,1,2,3
```
```
1,2,,3
```
```
1,2,3,
```
```
1,2,3.
```

are consided to be incorrectly formatted.

You should also ensure that there are no more than 50 nodes, and that every node has at least one neighbour.


## Command to Run / Testing Steps
Navigate to the directory containing `lab4plp.py` and use the following command in your terminal or command prompt:
```
python3 lab4plp.py <input_file.txt> <output_file.txt>
```
Replace `<input_file.txt>` with the path to your input file and `<output_file.txt>` with the desired path for the output file.

**NOTE:** It is much easier to place your `<input_file.txt>` file in the same directory as `lab4plp.py`, as this way you just have to specify the file name and not a path. Similarly you can just specify the `<output_file.txt>` without the path, and your reults file will be placed in the same directory and lab4plp & input_file.txt.


### Example
To test with a file named `smalltest.txt` and write the output to `smalltestresults.txt`:
1) Navigate to the directory containing lab4plp.py.
2) Place your 'smalltest.txt' file within this same directory.
3) Run the command:
```
python3 lab4plp.py smalltest.txt smalltestresults.txt
```

### Output
Following the steps above will cause the program to create a new file called ``smalltestresults.txt``, which will be placed in your current directory (the directory which contains lab4plp.py and smalltest.txt).
The text file shows the nodes with their allocated colors. 

e.g. if smalltestresults.txt contained: 
```
1A
2B
3B
4C
```
This would mean that Node 1 has been assigned color A, Node 2 has been assiged B, and so on.
Each line in the output file contains a node and its assigned color.

## Large Test File:

As provided on Blackboard, here is a large test file that you can use to test my program:
```
1,37,34,30,44,48,35,27,24,12,5,13,16,10,32,36,43,19,33,6,8,42,14,21,22,40,23,20,15,49,46,7,17,3,4,11,18,31,41
2,5,17,49,7,13,31,8,9,12,22,23,29,30,44,45,46,50
3,48,44,12,34,13,10,32,20,26,25,30,40,6,29,14,31,43,1,19,39,42,38,37,36,8,41,5,7,28,9,18,24,27,45,46
4,16,49,28,5,27,13,19,25,39,1,37,48,32,7,43,34,9,18,24,26,30,31,40,44,45,47
5,1,2,3,4,13,30,33,26,12,25,47,43,8,31,37,11,19,36,45,20,23,46,10,35,32,28,21,6,16,29,41,42,50
6,1,3,32,7,21,23,5,20,12,37,29,43,9,26,33,49,13,15,16,22,24,34,41,47
7,1,2,3,4,6,8,21,43,19,29,12,34,27,10,9,13,15,18,22,23,24,26,30,32,33,35,37,39,47
8,1,3,5,7,2,9,12,13,22,24,31,33,34,37,41,44,46,47
9,6,8,35,29,23,20,47,15,42,40,36,44,48,14,28,33,3,4,37,7,19,11,34,45,39,16,38,46,12,2,21,10,13,17,18,22,24,32
10,1,3,5,7,24,16,26,44,33,9,29,17,15,45,37,32,12,30,31,19,18,14,20,34,41,43
11,5,9,1,33,20,36,17,49,13,16,22,23,32,45,47,48
12,1,3,5,6,7,9,10,26,25,47,22,41,45,36,17,34,2,24,28,21,32,8,39,13,16,30,23,29,38,20,48,15,31,37,43,50
13,1,2,3,4,5,12,33,7,44,45,38,34,46,16,35,19,20,36,37,27,8,25,30,48,49,26,21,9,11,29,6,15,41,31,43,22,23,24,42,47
14,1,3,9,10,18,23,24,26,31,32,37,42,43,46
15,1,9,10,13,42,40,41,6,44,29,24,12,38,30,43,49,45,19,7,22,21,20,23,26,31,32,33,35,46,47
16,1,4,9,10,12,13,6,28,18,5,11,31,47,42,44,27,17,20,29,30,33,35,48
17,1,2,10,11,12,25,26,24,47,18,23,45,22,46,16,41,33,48,40,42,35,36,37,27,9,19,31,43
18,10,16,17,48,30,44,36,42,9,43,31,37,29,25,1,14,32,26,20,46,41,4,40,38,45,3,7,39,22,24,33,47
19,1,3,4,5,7,9,10,13,15,17,22,23,44,27,46,29,20,28,30,31,33,37,47,48
20,1,3,5,6,9,11,12,13,15,18,23,37,19,16,33,30,10,42,22,27,29,31,32,34,40,41,45
21,1,5,6,7,9,12,13,15,34,22,23,24,29,31,33,37,44,45,47,50
22,1,12,15,17,19,21,36,8,47,45,27,20,37,39,13,35,11,48,46,28,42,25,34,41,9,7,18,6,43,44,2,31,24,26,32,33
23,1,5,6,9,12,17,19,20,47,13,45,49,46,2,37,21,24,27,14,38,11,25,39,30,36,48,33,15,26,43,7,31,32,34,40
24,1,10,12,15,17,23,4,9,34,42,3,22,13,7,31,14,48,39,8,29,38,21,18,35,46,36,6,26,30,33,37,44,47
25,3,4,5,12,13,17,18,22,23,37,44,48,40,32,33,46
26,3,5,6,10,12,13,17,18,23,33,35,44,34,4,7,14,24,15,47,30,22,29
27,1,4,7,13,16,17,19,22,23,28,20,46,3,29,33,40,41,42,43,44,45
28,3,4,5,9,12,16,22,27,34,41,19,35,49,30,38,29,40,45
29,3,6,7,9,10,12,13,15,18,19,24,26,27,28,16,31,40,20,45,36,39,42,38,2,33,41,5,21,37,44,50
30,1,3,5,10,12,13,15,18,20,23,26,28,7,24,44,38,45,19,16,4,40,35,49,2,36,47,41,33,34,42,43,46,48,50
31,2,3,5,10,13,16,18,22,24,29,23,17,48,12,19,15,8,37,4,46,21,39,36,34,20,35,47,1,14,32,40,41,42,43,45
32,1,3,4,5,6,10,12,18,23,39,48,44,34,33,14,43,41,11,9,47,38,20,35,22,40,7,15,31,46,25,36,37
33,1,5,6,9,10,11,13,17,20,23,26,27,29,32,39,40,15,7,21,44,49,25,18,8,48,37,46,24,47,35,30,22,19,16,42,43,45,50
34,1,3,4,7,9,12,13,21,22,24,26,28,31,32,37,35,8,49,39,42,10,48,23,30,6,47,36,40,20,43,44,45,46,50
35,1,5,9,13,17,22,24,26,28,30,31,32,33,34,16,7,15,42,41,43,47,48
36,1,3,5,9,11,12,13,17,18,22,23,24,29,30,31,32,34,42,40,43,47,48
37,1,3,4,5,6,9,10,13,17,18,20,22,23,25,31,33,34,12,24,32,19,40,8,49,7,29,14,42,21,46,41,45,48
38,3,9,12,13,15,18,23,24,28,29,30,32,41,44,42,43,45,46,48
39,3,4,9,12,18,22,23,24,29,31,32,33,34,7,41,43
40,1,3,9,15,17,18,25,29,30,32,33,34,36,37,23,4,27,28,31,20,41,44,46,47,48
41,3,12,13,15,17,18,22,28,29,30,32,38,1,37,6,5,8,27,31,40,20,39,10,46,35,42,43,45,47
42,1,3,9,15,16,17,18,20,22,24,29,34,35,36,37,33,49,41,30,31,27,14,13,5,38,44,45,47,48,50
43,1,3,4,5,6,7,13,15,18,22,23,32,12,10,47,46,17,36,33,34,39,45,35,27,38,41,31,30,14,49,44
44,1,3,9,10,13,15,16,18,19,22,25,26,30,32,33,38,34,45,24,8,21,42,27,43,29,4,2,46,40,48
45,5,9,10,12,13,15,17,18,22,23,29,30,43,44,38,4,33,11,21,37,27,31,46,34,20,2,28,49,47,41,42,3
46,1,5,9,13,17,18,19,22,23,24,27,31,32,33,37,41,43,44,45,30,38,3,2,14,8,34,15,25,40,50
47,5,9,12,16,17,22,23,26,30,31,32,33,34,43,45,35,41,4,8,15,19,40,42,24,36,21,48,18,7,6,11,13
48,1,3,4,9,12,13,17,18,22,23,24,25,31,32,33,34,47,11,42,40,36,38,16,44,30,19,35,37,50
49,1,2,4,6,11,13,15,23,28,30,33,34,37,42,43,45
50,46,12,29,34,21,5,48,2,42,33,30
```

Which when tested on my algoritm, should provide the following results:
```
1B
2K
3D
4C
5F
6E
7J
8I
9B
10M
11E
12C
13A
14C
15F
16D
17F
18A
19G
20L
21K
22D
23D
24G
25B
26B
27E
28A
29I
30E
31E
32G
33C
34F
35L
36K
37H
38L
39H
40M
41K
42J
43I
44H
45G
46J
47H
48I
49L
50A
```


## Troubleshooting

If you are facing any issues, Ensure that you have Python3 installed. Try to re-do all the instructions and steps mentioned above.

---

