# Quorum's Challenge

![](https://img.shields.io/badge/version-v0.1.0-gold)  
![](https://img.shields.io/badge/python-v3.10.1-blue)
![](https://img.shields.io/badge/flake8-v5.0.4-purple)

![](https://img.shields.io/badge/pytest-v7.1.2-black)
![](https://img.shields.io/badge/passed_tests-9-brightgreen)
![](https://img.shields.io/badge/failed_tests-0-red)

![](https://img.shields.io/badge/coverage-97%25-brightgreen)

This repository handles the solution for Quorum's Software Development challenge.

## Project Structure
```
src                                ----- Sources Root
|__ main.py                        ----- Runs the application
|__ controllers                    ----- App main features
    |__ bills_details.py           ----- Generates the bills tasks solution
    |__ file_handler.py            ----- Read and write the csv files
    |__ legislators_votes.py       ----- Generates the legislators tasks solution
|__ dataset                        ----- CSV files data
    |__ bills.csv                  ----- All the bills
    |__ legislators.csv            ----- All the legislators
    |__ vote_results.csv           ----- All the vote results
    |__ votes.csv                  ----- All the votes
|__ tests                          ----- Test cases for the application
    |__ test_bills_details.py      ----- Test cases for bills details features
    |__ test_file_handler.py       ----- Test cases for file handler features
    |__ test_legislators_votes.py  ----- Test cases for legislators votes features
```

## How To Run Locally
Requirements:
- [Git](https://git-scm.com/downloads)
- [Python3.10](https://www.python.org/downloads/)

1. Clone the repository  
`git clone https://github.com/salatiel6/quorum_challenge.git`


2.  Open the challenge directory  
Widows/Linux:`cd quorum_challenge`  
Mac: `open quorum_challenge`


3. Create virtual environment (recommended)  
`python -m venv ./venv`


4. Activate virtual environment (recommended)  
Windows: `venv\Scripts\activate`  
Linux/Mac: `source venv/bin/activate`


5. Install every dependencies  
`pip install -r requirements.txt`


6. Open the source directory  
Windows/Linux: `cd src`  
Mac: `open src`


7. Run tests  
Without coverage: `pytest`  
With coverage: `pytest -vv --cov=. --cov-report=term-missing --cov-config=.coveragerc`


8. Run the application  
`python main.py`


9. Access the CSV result files directory (the `deliverables` folder will only be available after runnig the application once)  
Widows/Linux:`cd deliverables`  
Mac: `open cd deliverables`


10. The results will be encountered at:  
`legislators-support-oppose-count.csv`  
`bills.csv`
