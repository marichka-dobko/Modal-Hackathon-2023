import re

def get_file_content(input_file):

	contexts = []
	context = ""
	fullPage = ""
	with open(input_file, 'r') as file:
		for line in file:
			if "{Benefit}" in line:
				if len(context) != 0:
					contexts.append(context)
					context = ""

			# start = re.escape("Pages: ")
			# end=re.escape("}")
			# res = re.search('%s(.*)%s' % (start, end), line).group(1)
			# line = line.replace(res, '').replace('Pages:', '')

			context = context + line
			fullPage = fullPage + line

		contexts.append(context)

	contents = []
	for context in contexts:
		content = {}
		content['Context'] = context
		content['Filename'] = input_file
		content['FullPage'] = fullPage

		contents.append(content)


	return contents





	# 			if 
	# 			content = 
	# 			if content

    #         print(line, end='')  # 'end' parameter to avoid double spacing between lines
	# 	for i in range(len(reader.pages)):
	# 		page = i
	# 		policy = input_file
	# 		page = reader.pages[i]
	# 		text = page.extract_text()
	# 		content={'Page': i, "Policy": policy, "Context":text}
	# 		contents.append(content)


	# return contents