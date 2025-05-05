# few-and-far supporter donations developer test #


# Brief #
As the document states, we're not looking for an implementation in any particular language or framework, so please use what you're most comfortable with. The goal is for you to demonstrate your technical ability and problem solving skills. There are no fixed requirements for the code, instead I'm more interested in your decision making and attention to detail.

These are some considerations, all of which we are not expecting to see at once:
- Data persistence 
- Unique statistics 
- Feature and/or Unit Tests
- User interface to inspect data (graphical or otherwise) 
Feel free to email your code, including a README, or if you are using a private GitHub repo grant me collaborator access with me, if you'd prefer: nadinengland


# My Implementation ##

## Description ##
I have built a text based UI in python

Based on the brief, I have considered the following
- Data persistence ✅ - Can save an export of the generated data and load it to view
- Unique statistics ✅ - Gave some simple and effective statstics in relation to the data
- Feature and/or Unit Tests ✅
- User interface to inspect data (graphical or otherwise) ✅ - Generated 3 graphs in relation to the generated statistics

Option 1 Creates a new export after reading the JSON files. I decided to implement with then endpoints /supporters and /donations. This export is saved as a JSON sump in the dir /donation_output

Option 2 Reads a JSON dump of a previously created and saved report, in the dir /donation_output

Option 3 Generates Unique Statistics of the data and outputs them in the console. It exports 3 graphs to the dir /donation_output, to be viewed as pngs.

## Usage ##
NOTE: please be patient when creating a new export, it takes no more than 1 minute.

Run the program in the termial by navigating to workspaces/few-and-far and then execute the command 'python3 main.py'

Run the unit tests in the terminal by navigating to workspaces/few-and-far and then execute the command 'python3 unit_tests.py'
If they all pass, you will be prompted with the response 'OK'

## Tree ##
run 'tree' in the terminal or see below: 
.
├── README.md\n
├── __pycache__\n
│   └── config.cpython-312.pyc\n
├── config.py\n
├── donation_output\n
│   ├── all_donations.png\n
│   ├── donation_export.json\n
│   ├── supporter_donations.png\n
│   └── top_10_supporters.png\n
├── main.py\n
└── unit_tests.py\n
