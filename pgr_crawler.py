import sys
from os import system
import urllib
import time
import codecs

import extract

ARTICLE_FN = ['articles.txt', 'questions.txt']
COMMENT_FN = ['comments.txt', 'answers.txt']
URL = ["http://www.pgr21.com/pb/pb.php?id=freedom&no=%d", 'http://pgr21.com/pb/pb.php?id=qna&no=%d']
INTERVAL = 2
THRES = 30

def download(url, filename):
	f = urllib.urlopen(url)

	print "Download file from %s to %s" % (url, filename)
	data = f.read()

	f_ = open(filename, "w")
	f_.write(data)
	f_.close()

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')

	for phase in xrange(0, len(URL)):
		url = URL[phase]
		from_num = int(sys.argv[1 + (2 * phase)])
		to_num = int(sys.argv[2 + (2 * phase)])

		cnt = 0
		for index in xrange(from_num, to_num + 1):
			try:
				url_ = url % index
				download(url_, "./tmp.html")
				subject, writer, article, comments = extract.extract('./tmp.html')

				if len(comments) > 0:
					f = codecs.open(ARTICLE_FN[phase], 'a', 'utf-8')
					f.write(("%d\t" % index) + subject.decode('utf-8') + '\t' + writer.decode('utf-8') + '\t' + article.decode('utf-8') + '\n')
					f.close()

					f = codecs.open(COMMENT_FN[phase], 'a', 'utf-8')
					for c_id in sorted(comments.keys()):
						p_id, depth, user_id, comment, time_stamp = comments[c_id]
						f.write("%s\t%d\t%s\t%s\t%d\t%s\t%s\n" % (time_stamp, index, c_id, p_id, depth, user_id.decode('utf-8'), comment.decode('utf-8')))
						print "%s\t%d\t%s\t%s\t%d\t%s\t%s\n" % (time_stamp, index, c_id, p_id, depth, user_id, comment)

					f.close()

					cnt = 0
				else:
					cnt += 1

					if cnt > THRES:
						break
			except Exception, e:
				pass
			time.sleep(INTERVAL)
