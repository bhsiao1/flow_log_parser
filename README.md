# Parser for Flow Log Data

Assumptions:
This only supports default log format, not custom and the only version that is supported is 2. This assumes only a few different protocols being put into the lookup_table. Can add more in the dictionary of map_flow_log method manually. Assumed that lookup table and flow log files are valid data.

How to Compile/Run the program:
- Use default lookup_table and flow_log or replace with own data for both.
- Run this command in the terminal to use the parser: python3 main/parser.py
- Run this command in the terinal to run the unit tests: python3 main/parser_test.py

Tests done: Manual Test given the existing lookup_table.csv and flow_log.txt but also wrote unit tests with mocking to test the methods written. 

