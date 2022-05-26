# Instructions

## How te get started

1. Sample data to work with is provided in file `sample-data.json` in folder `data`. I can add additional files if needed
2. the code is tested on python 3.9.11 installed through `pyenv` + `pyenv-virtualenv` (https://realpython.com/intro-to-pyenv/#virtual-environments-and-pyenv)
3. once we have installed python and sourced the environment, we can install packages with: `pip install -r requirements.txt`
4. we then run the code by just typing `python v1.py`. This would fetch the sample data, stick it in the function, run and display results in the terminal. 

## Other Notes
1. I have written a v1. Maybe it makes sense to leave it as is and just create v2, v3 with respective changes described in the comment
2. in reality there are two groups of ingredients - over 2% and optionally under 2%. The difference is that ingredients over 2% are always sorted according to the quantity starting with what is most of. However this rule does not apply to products under 2% if such are listed by the manufacturer on the nutrition label. I have not implemented this logic yet. 
3. please excuse some of the camelCase variables in python, they come from the Javascript code. 

## Cheetos sample target
From laboratory testing we know for sure the following numbers:
fat - 39%
protein - 0.3%
carbs - 56%
sugar - 2.7%
carbs = starch + fiber + sugars
