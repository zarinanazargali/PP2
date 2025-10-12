#1. Match a string that has an 'a' followed by zero or more 'b's
import re
pattern = r'ab*'
test_strings = ['a', 'ab', 'abb', 'ac', 'b', 'aab']
for s in test_strings:
    if re.fullmatch(pattern, s):
        print(s)
#2. Match a string that has an 'a' followed by two to three 'b's
import re
pattern = r'ab{2,3}'
test_strings = ['a', 'ab', 'abb', 'abbb', 'abbbb']
for s in test_strings:
    if re.fullmatch(pattern, s):
        print(s)
#3. Find sequences of lowercase letters joined with an underscore
import re
pattern = r'[a-z]+_[a-z]+'
test_strings = ['hello_world', 'Hello_World', 'abc_def_ghi']
for s in test_strings:
    print(re.findall(pattern, s))
#4. Find sequences of one uppercase letter followed by lowercase letters
import re
pattern = r'[A-Z][a-z]+'
test_strings = ['Hello', 'Python', 'java', 'HiThere']
for s in test_strings:
    print(re.findall(pattern, s))
#5. Match a string that has an 'a' followed by anything, ending in 'b'
import re
pattern = r'a.*b$'
test_strings = ['aab', 'axb', 'a123b', 'ab', 'abc']
for s in test_strings:
    if re.fullmatch(pattern, s):
        print(s)
#6. Replace all occurrences of space, comma, or dot with a colon
import re
text = "Hello, world. This is Python regex"
result = re.sub(r'[ ,.]', ':', text)
print(result)
#7. Convert snake case string to camel case string
import re
def snake_to_camel(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])
print(snake_to_camel('hello_world_example'))
#8. Split a string at uppercase letters
import re
text = "HelloWorldPython"
result = re.split(r'(?=[A-Z])', text)
print(result)
#9. Insert spaces between words starting with capital letters
import re
text = "HelloWorldPython"
result = re.sub(r'([A-Z])', r' \1', text).strip()
print(result)
#10. Convert camel case string to snake case
import re
def camel_to_snake(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
print(camel_to_snake('HelloWorldPython'))