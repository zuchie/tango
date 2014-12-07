'''
    Scrape and format from cedit.txt in text,translation format
    into dict_db.txt.
'''
# Import regular expression.
import re

f_input = open('cedit.txt', 'r')
f_output = open('dict_db.csv', 'w')

for i in range(34): f_input.next() # Skip firt 34 lines.
for line in f_input:
    # Non-greedy((.+?)stop search at first match) search any char between 2 whitespaces.
    match_text = re.search(r'\s(.+?)\s', line)
    # Greedy((.+)stop search at last match) search any char between 1st and last '/'.
    match_translation = re.search(r'\/(.+)\/', line)
    # Search successful?
    if match_text and match_translation:
        # Strip surrounding whitespaces.
        match_text_trimed = re.sub(r'\s', r'', match_text.group())
        # Strip 1st and last '/'.
        match_translation_trimed = re.sub(r'^\/|\/$', r'', match_translation.group())
        # Escape '"', or sqlite3 would blame when importing into db. 
        match_translation_escaped = re.sub(r'\"', r'\\"', match_translation_trimed)
        # Make a list and join by '@' delimiter, since there might have ','sin translation context. Those extra ','s would be treated as delimiters when importing into db.
        dict_entry = [match_text_trimed, match_translation_escaped]
        dict_entry_joined = '@'.join(dict_entry)
        # Write to file.
        f_output.write(dict_entry_joined) 
        f_output.write('\n') 

f_input.close()
f_output.close()
