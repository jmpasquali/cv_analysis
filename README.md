# cv_analysis

Calculate anodic and cathodic peak curents from cyclic voltammetry experimental data file list. 
Plots cyclic voltammetry, anodic and cathodic peaks and linear regression of capacitive backgroud calculated for each set. Produces output text file with anodic and cathodic peak information (current and potential). Developed for one cycle only and IUPAC's convention of direction. 

### How to run: 
1) Open a terminal/command window.
2) Change directories to the location where this file is saved.
3) Run the program file
```python cv_analysis.py```
4) When solicited, type the name of txt or csv file containing file names, x (potential) column label and y (current) column label.

### How to produce your input file list:
1) Open a terminal/command window.
2) Change directories to the location where your data is saved.
3) For mac/linux type this command: ``` ls > input.txt``` or
``` ls |grep "search string" > input.txt```
4) For Windows type:
```dir > input.txt``` or see more [detailed instructions](https://support.microsoft.com/en-us/help/196158/how-to-create-a-text-file-list-of-the-contents-of-a-folder) 

 ### Calculations based on the following articles: 
 1. [Theory and Application of Cyclic Voltammetry for Measurement of Electrode Reaction Kinetics](https://pubs.acs.org/doi/10.1021/ac60230a016)
 2. [A Practical Beginner’s Guide to Cyclic Voltammetry](https://pubs.acs.org/doi/10.1021/acs.jchemed.7b00361)
