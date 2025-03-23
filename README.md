# SIMPLEX Program

This program was developed as an application for implementing the SIMPLEX method, used to solve linear programming problems. The main goal is to understand and practice the concepts of the SIMPLEX method, with a focus on the computational implementation of the iterative steps. The code allows for the maximization of linear functions and handles various situations that may arise during the algorithm's execution, such as degeneration issues and undefined boundaries.

## Objective

The main objective of this program is to consolidate the knowledge acquired about the SIMPLEX method through active programming.

## Program Requirements

### 1. Implement Maximization
The program focuses on the maximization of linear functions, which is the simplest case and serves as a test or debugging technique during the program’s development.

### 2. User Interface
The program has an interface that allows the user to input the coefficients of the matrix (or load a file with the data). This facilitates validation and use of the program in different situations. The user should be able to easily provide the coefficients for the calculations.

### 3. Display Iteration Count
At each step of the algorithm, the program displays the status of the coefficients in the table or matrix, allowing the user to follow the progress of execution. The number of iterations is indicated, allowing the user to validate each step of the process.

### 4. Identify the Optimal "Z" or "C" and Basic Variable Values
The program displays the solution to the problem, indicating the optimal value of "Z" (objective function) or "C" (decision variables), along with the values of the basic variables. If the algorithm is interrupted due to mathematical accidents or issues in the method, this interruption will be clear to the user.

### 5. Detect Degeneration Issues
The program identifies whether the linear programming problem has degeneration issues, which may affect the convergence of the algorithm. The software signals these cases, allowing the user to make informed decisions about how to proceed.

### 6. Indicate if the Problem Has an Undefined Boundary
The program checks if the linear programming problem has an undefined boundary in any dimension, which can occur in specific scenarios. This check is important to ensure that the problem has a valid solution.

### 7. Identify Redundant Constraints
The software checks for redundant constraints in the linear programming model, which may be unnecessary and affect the efficiency of the algorithm. If any are found, the program will notify the user.

## How to Use

1. **Initializing the Program:**
--- Visual Studio Terminal:
Type in the terminal `python -u “the path to the file: SIMPLEX.py”` and press enter.

2. **Input Data for Problems in Canonical Maximization Form:**
   - Step 1: Indicate whether the objective function is Z or C.
     Type "Z" or "C" and press enter.
   - Step 2: Indicate the number of variables.
     Type the number of variables and press enter.
   - Step 3: Indicate the number of constraints.
     Type the number of constraints and press enter.
   - Step 4: Provide the coefficients of the objective function; if any constraint has fewer variables, enter the coefficient 0.
     Enter each coefficient of the objective function, pressing enter after each number.
   - Step 5: Provide the data for the constraints.
     Enter each coefficient of the constraints, pressing enter after each number.

3. **Running the Algorithm:**
   - The SIMPLEX algorithm will run based on the data provided.
   - After each iteration, the program will display the updated matrix or table, along with the iteration number and values of the variables.

4. **Results:**
   - The program will display the optimal value of "Z" (objective function) or "C" (decision variables) along with the values of the basic variables.
   - If the algorithm encounters issues such as degeneration or lack of a boundary, the program will notify the user.

## Conclusion

This program serves as an educational tool for active learning of the SIMPLEX method.
