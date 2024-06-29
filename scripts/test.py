import re

# Example Markdown content
markdown_content = """
Check out these repositories:
- [Example Repo 1](https://github.com/user1/repo1)
- [Example Repo 2](https://github.com/user2/repo2)
Visit the main GitHub page: https://github.com
"""

# Regex pattern for GitHub repository links
pattern = r"https:\/\/github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+"

# Find all matches in the content
matches = re.findall(pattern, markdown_content)

# Print all matches
for match in matches:
    print(match)
