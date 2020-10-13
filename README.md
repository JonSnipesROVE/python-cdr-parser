# python-cdr-parser
python-cdr-parse takes an argument as a CSV file or SQLite3 DB file and allows queries to be run against the resulting DB as standard queries.  Not limited to only CDR data but useful for needing to quickly parse through CSV style tables.  All fields are imported as characters to simplify import process.

Usage:<br> 
<br>
#: parse-cdr.py -f CDRFile.csv <br>
#: parse-cdr.py -db CDRFile.csv.db <br>
<br>
sql> config tab #sets output as Tab delimited (default)<br>
sql> config csv #sets output as csv delimited<br>
sql> select * from cdr where callingPartyNumber = "555" limit 5<br>
sql> quit
