The Tokenizer is encapsulated as a Tokenizer object
to use it, just create an instance
tk = Tokenizer()

it is supposed to provide two functions
tk.read(inputString) # string -> [token]
tk.read_file(path)   # string -> [token]

The Token definition is under ./tokenizer/Token.py. I've tried to keep it straightforward and intuitive
I've included a sample_code.txt as a sample program, and a sample_output.txt as an expected token output
I've changed the indentation a little bit so you can read it clearly and compare it to the original code
Spaces are ignored on purpose