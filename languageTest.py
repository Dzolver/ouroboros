import grammar_check
tool = grammar_check.LanguageTool('en-GB')
text = '.'
matches = tool.check(text)
print(grammar_check.correct(text,matches))
