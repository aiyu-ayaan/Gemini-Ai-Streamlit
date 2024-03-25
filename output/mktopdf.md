
To run a command like `mdpdf -o output.pdf .\input.md` in code, you can use a programming language that allows you to execute shell commands. Here's an example using Python:

```python
import subprocess

# Define the command
command = ["mdpdf", "-o", "output.pdf", "./input.md"]

# Execute the command
try:
    subprocess.run(command, check=True)
    print("PDF generation successful!")
except subprocess.CalledProcessError as e:
    print("Error:", e)
```

Make sure you have Python installed on your system. This script will execute the `mdpdf` command with the specified arguments. If the command is successful, it will print "PDF generation successful!". If there's an error, it will print the error message.
