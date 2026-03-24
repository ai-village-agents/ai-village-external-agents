with open("A2A-INTERACTIONS.md", "r") as f:
    content = f.read()

import re

# Simple auto-resolve by keeping both changes
def auto_resolve(content):
    pattern = re.compile(r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [a-f0-9]+', re.DOTALL)
    
    def replacement(match):
        return match.group(1) + "\n" + match.group(2)
        
    resolved = pattern.sub(replacement, content)
    return resolved

resolved_content = auto_resolve(content)

with open("A2A-INTERACTIONS.md", "w") as f:
    f.write(resolved_content)

print("Conflicts resolved.")
