import sys
from os import system
from urllib import request
import time
import codecs

import extract

BASE_URL = 'https://pgr21.com/%s/%d'
TARGETS = ['recommend', 'discuss', 'election', 'freedom', 'spoent', 'qna', 'humor']

INTERVAL = 2
THRES = 30

def download(url, filename):
	request.urlretrieve(url, filename)

	print("Download file from %s to %s" % (url, filename))


if __name__ == "__main__":
	for phase, target in enumerate(TARGETS):
		article_fn = '%s.txt' % target
		comment_fn = '%s_comments.txt' % target

		from_num = int(sys.argv[1 + (2 * phase)])
		to_num = int(sys.argv[2 + (2 * phase)])

		cnt = 0
		for index in range(from_num, to_num + 1):
			try:
				url = BASE_URL % (target, index)

				download(url, "./tmp.html")
				subject, writer, article, comments = extract.extract('./tmp.html')

				if len(comments) > 0:
					f = open(article_fn, 'a')
					f.write(("%d\t" % index) + subject + '\t' + writer + '\t' + article + '\n')
					f.close()

					f = open(comment_fn, 'a')
					for c_id in sorted(comments.keys()):
						p_id, depth, user_id, comment, time_stamp = comments[c_id]
						f.write("%s\t%d\t%s\t%s\t%d\t%s\t%s\n" % (time_stamp, index, c_id, p_id, depth, user_id, comment))
						print("%s\t%d\t%s\t%s\t%d\t%s\t%s\n" % (time_stamp, index, c_id, p_id, depth, user_id, comment))

					f.close()

					cnt = 0
				else:
					cnt += 1

					if cnt > THRES:
						break
			except Exception as e:
				print(e)
			time.sleep(INTERVAL)
