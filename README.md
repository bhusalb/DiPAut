<h1 align="center">
  DiPAut
</h1>

<p align="center">
  DiPAut is a software tool built in Python that checks the differential privacy of online randomized algorithms. It computes a bound "d" for the weight of the automaton, ensuring differential privacy for all privacy budgets "ε".
</p>


<div align="center">
  <a href="#installation"><b>Installation</b></a> |
  <a href="#usage"><b>Usage</b></a> |
  <a href="#writing_your_own_algorithm"><b>Writing Your Own Algorithm</b></a>
</div>

## Installation

### Install Via Docker

To install DiPAut via Docker, navigate to the project root directory and run the following commands:

```bash
docker build . -t dipaut
docker run --rm -it dipaut
```

### Install without Docker

If you prefer to install without Docker, make sure you have Python3 installed and run the following command in your
terminal:

```bash
  
 pip install -r requirements.txt
```

These commands will install all the necessary dependencies for DiPAut to run properly. You can then run the tool by
executing the main script.

## Usage

```
usage: main.py [-h] [-i FILE] [-g]

-i FILE, -input FILE

Provide input file path

-g, --show-graph 

This parameter determines whether or not to display the graph, 
and its default value is set to False.
```

If you're using the tool via Docker, graph visualization won't be available (`-g` or `--show-graph` won't work).

To start analyzing a file, run `python main.py -i [FILE]`.

Here is an example output of using DiPAut. The program is analyzing the file "examples/leaking_cycle/example_4.dipa"

```bash

root@6f6dd6e61a7e:/usr/src/dipAut# python main.py -i examples/leaking_cycle/example_4.dipa 
----------------------------------------------------------------------------
                    Result of examples/leaking_cycle/example_4.dipa                   
┌────────────────────────────────────────────────┬──────────────────────────────────┐
│ Test                                           │ Detected?                        │
├────────────────────────────────────────────────┼──────────────────────────────────┤
│ Leaking Cycle                                  │ Yes                              │
└────────────────────────────────────────────────┴──────────────────────────────────┘
                       Automata is not differentially private.
```

The output will display whether the test was detected or not. In the provided example, "Leaking Cycle" was detected and
the automata was not differentially private.

## Writing Your Own Algorithm

Introducing Dipa, a simple new language with two parts: State and Statement.

State has 5 parameters:

- State Name (required): Begins with 'q' followed by a number (regex: q\d+), e.g., q1, q2, q3, q4. Generally starts from q1. By default, it is an input state. To mark it as non-input, add ':non-input', e.g., q1:non-input, q10:non-input.
- Scaling Factor (d) (required): Scaling factor d for the Laplacian distribution. Can be fractions (¼, ⅛) or integers.
- Mean (μ) (required): Mean for the Laplacian distribution. Can be fractions (¼, ⅛) or integers.
- Scaling Factor (d') (optional): Scaling factor d' for the Laplacian distribution for insample'. Can be fractions (¼, ⅛) or integers. Not required if the statement doesn't use insample'.
- Mean (μ') (optional): Mean prime for the Laplacian distribution for insample'. Can be fractions (¼, ⅛) or integers. Not required if the statement doesn't use insample'.


Dipa supports various types of statements, each with an assignment or control block, output, and a next step.

Assignment Statements include variable assignment to insample or insample', output, and a goto directive. Outputs can be insample/insample' or anything following 'o' (regex: o[a-z]+, e.g., obot, otop, oread).

Examples:

```bash
r4:= insample; output obot; goto q9
l3:= insample; output obot; goto q6
```
Control Statements support if and elseif blocks. Expressions follow a pattern with variables, comparison operators, and insample or insample'. Expressions can use an AND gate (&&) for chaining.

Examples:

```bash
insample >= l1
insample >= l1 && insample < r1
insample <= l2 && insample > r1
```

Overall Program Examples:

**SVT:**

```bash 
(q1:non-input,1/4,0): x:= insample; output oinput; goto q2
(q2,1/2,0): if (insample<= x) then output obot; goto q2 elseif (insample >= x) then output otop; goto q3

```
**Numeric Range:**

```bash
(q1:non-input,1/4,0): x:= insample; output oinput; goto q2
(q2,1/2,0, 1/2, 0): if (insample<= x) then output obot; goto q2 elseif (insample >= x) then output insampleprime; goto q3
```

**Leaking Cycle:**

```bash 
(q1:non-input,1/2,0): x1:= insample; output obot; goto q2
(q2:non-input,1/2,10): x2:= insample; output obot; goto q3
(q3,1/6,0): if (insample < x2 && insample >= x1) then output obot; goto q4
(q4,1/6,0): if (insample < x2) then x2:= insample; output obot; goto q3
```

**Leaking Pair:**

```bash
(q1:non-input,1/4,0): u:= insample; output obot; goto q2
(q2:non-input,1/4,1): v:= insample; output obot; goto q3
(q3:non-input,1/4,2): w:= insample; output obot; goto q4
(q4,1/4,0): if (insample >= u && insample < v) then output ocontinue; goto q4 elseif (insample < u) then output obot; goto q6 elseif (insample > v && insample < w) then output otop; goto q5 elseif (insample >v && insample > w) then output otop; goto q6
(q5,1/4,0): if (insample >= v && insample < w) then output ocontinue; goto q5 elseif (insample < v) then output obot; goto q6  elseif (insample > w) then output otop; goto q6
```

More examples can be found in the `examples` directory of the repository.


## Running the Benchmark and Plot Generation Scripts
In this repository, we provide examples used in our paper, organized into three folders:

- `m_range_examples/`
- `k_min_max_examples/`
- `simple_examples/`

**Benchmark Script**

To run the DipAut benchmark on all examples within a specific folder, use the provided benchmark.py script as follows:

```bash
python3 scripts/benchmark.py --folder <folder_name>
```

Replace <folder_name> with the desired folder (e.g., m_range_examples, k_min_max_examples, or simple_examples). The results will be saved as a CSV file in the results/ folder, named <folder_name>_result.csv.

**Plot Generation Script**

To generate plots from the benchmark results, use the plot_generator.py script:

```bash
python3 scripts/plot_generator.py
```
This script will process the CSV files in the results/ folder and generate corresponding plots, which will be stored in the plots/ folder.




