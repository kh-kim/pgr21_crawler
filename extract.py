import re
import codecs
from bs4 import BeautifulSoup as bs

def remove_tags(line):
	line = " ".join(line.strip().split("\n")).strip()
	line = re.sub('<[^>]+>', '', line)

	return line.strip()

def concat_lines(line):
	line = re.sub('(\\r)?\\n', ' ', line)
	line = re.sub('\\r', ' ', line)
	line = re.sub('\\s\\s+', ' ', line)

	return line.strip()

def remove_postfix(line, postfix=['수정', '삭제', '해시', '아이콘']):
	tokens = line.split(' ')
	tokens.reverse()
	ret = []

	flag_on = False
	for t in tokens:
		if t not in postfix or flag_on:
			ret += [t]
			flag_on = True

	ret.reverse()

	return ' '.join(ret)

def extract(filename):
	f = codecs.open(filename, 'r', 'utf-8')
	d = f.read()
	f.close()

	s = bs(d, 'html.parser')

	writer = ''
	subject = ''
	article = ''
	comments = {}
	tmp_comments = {}
	tmp_structures = {}

	for td in s.find_all('td'):
		if td.get('id') != None and td.get('id') == 'view_writer':
			writer = concat_lines(td.get_text())
		if td.get('style') != None and td.get('style') == 'border-bottom:1px solid #e5e5e5;':
			subject = concat_lines(td.get_text())

	for div in s.find_all('div'):
		comment_content = None

		if div.get('class') != None and div.get('class')[0] == 'articleArea':
			article = concat_lines(div.get_text())
		if div.get('class') != None and div.get('class')[0] == 'aReply':
			comment_id = div.a['name']
			user_id = remove_postfix(concat_lines(div.get_text()))
		if div.get('class') != None and div.get('class')[0] == 'vc_right':
			time_stamp = remove_postfix(concat_lines(div.get_text()))

			if time_stamp[:2] != "20":
				time_stamp = '20' + time_stamp
			time_stamp = time_stamp + ":00"
			time_stamp = re.sub('/', '-', time_stamp)
		if div.get('class') != None and div.get('class')[0] == 'cmemo':
			comment_content = concat_lines(div.get_text())

		if comment_content != None:
			tmp_comments[comment_id] = (user_id, comment_content, time_stamp)

	for sc in s.find_all('script'):
		if 'comment_step_proc' in str(sc) and remove_tags(str(sc))[-2:] == ');':
			comment_id = remove_tags(str(sc))[len('comment_step_proc('):-2].split(',')[1]
			parent_id = remove_tags(str(sc))[len('comment_step_proc('):-2].split(',')[0]
			depth = int(remove_tags(str(sc))[len('comment_step_proc('):-2].split(',')[2])

			tmp_structures[comment_id] = (parent_id, depth)

	for key in tmp_comments.keys():
		comments[key] = tuple(tmp_structures[key] + tmp_comments[key])

	return subject, writer, article, comments

if __name__ == "__main__":
	print(extract('./tmp_.html'))
