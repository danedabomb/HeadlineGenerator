# (heads, descs, keywords)
# heads is a list of headline stirngs
# descs a list of article strings in same order and length as heads
# keywords is None

import pickle as pkl

fin = open("all_the_news_v2.csv", "r")

'''
lines = list(fin)#.read():
fin.close()
counter = 0
for line in lines:
    counter += 1
print counter
'''
counter = 0
articles = []
line = fin.readline() # header
print(line)
line = fin.readline()
while (line and counter < 96655):

    # error articles (skip)
    error_articles = [41876, 55042, 55043, 55044, 60492, 60493, 60494, 60827, 60828, 60829, 60886, 60887, 60888, 65220, 65221, 65222, 69606, 69607, 69608, 77757, 77758] + list(range(96508, 96517)) + list(range(96522, 96565)) + list(range(96596, 96596+39))
    if counter in error_articles:
        print(counter)
        line = fin.readline()
        counter += 1
        continue

    # 3 line article entries
    if counter >= 0 and counter < 142:
        title = ""
        title_space = line.split(",")
        num = int(title_space[0])
        for j in range(1, len(title_space)):
            title += title_space[j] + ","
        title = title[:-4]
        if title[0] == '"':
            title = title[1:]
        if title[-1] == '"':
            title = title[:-1]
        title = title.decode('utf-8').strip()


        line = fin.readline()
        author = line.decode('utf-8').strip()
        

        line = fin.readline()
        article_space = line.split(",")
        # date,content,year,month,publication,url,length
        date = article_space[1].split("-")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        publication = article_space[-3].decode('utf-8').strip()
        length = int(article_space[-1].decode('utf-8').strip())
        content = ""
        for i in range(2, len(article_space)-5):
            content += article_space[i]
        if content[0] == '"':
            content = content[1:]
        if content[-1] == '"':
            content = content[:-1]

        # check to make sure we're parsing correctly
        int(article_space[-1])


        article = {"num": num, "title": title, "author": author, "year": year, "month": month, "day": day, "publication": publication, "length": length, "content": content}
        articles.append(article)


        line = fin.readline()
        counter += 1


    # 1 line article entries
    else:

        '''
        if counter == 96596:
            print line
            for i in range(44):
                print "line"
                print fin.readline()
            import sys
            sys.exit()
        '''
        
        # odd 3 line formatting
        odd_3_line_formatting = [65547, 65548, 65706, 65774, 69587, 76904, 96434, 96469, 96489, 96496, 96501, 96504, 96566, 96574] 
        if counter in odd_3_line_formatting or (counter >= 65858 and counter < 65966):
            line1 = line.decode('utf-8').strip()
            line2 = fin.readline().decode('utf-8').strip()
            line3 = fin.readline().decode('utf-8').strip()
            if counter in [96434, 96501]:
                line2 = fin.readline().decode('utf-8').strip()
                line3 = fin.readline().decode('utf-8').strip()
            if "," not in line2:
                if line1[-1] == '"':
                    line1 = line1[:-1]
                if line3[0] == '"':
                    line3 = line3[1:]
            line = line1 + line2 + line3
        # odd 2 line formatting
        elif counter >= 69453 and counter != 73746:
            line1 = line.decode('utf-8').strip()
            line2 = fin.readline().decode('utf-8').strip()
            line = line1 + line2

        content_space = line.split(",")

        num = int(content_space[0])
        
        # check for commas in title (title with commas are enclosed in quotations marks)
        title_commas = False
        # list of edge case titles with quotation marks
        edge_titles = [3100, 3343, 5000, 5762, 6337, 6927, 8259, 9041, 9319, 9627, 19152, 19279, 20372, 21933, 22447, 22473, 24220, 24759, 25002, 26176, 26192, 28271, 28865, 29098, 30175, 32559, 33245, 33836, 34370, 35777, 37486, 37929, 38113, 38292, 60799, 61720, 62866, 65198, 66206, 66235, 71858, 71882, 71897, 72172, 72319, 75855, 78434, 79342, 79387]
        extra_edge_titles = [8259]
        if '"' in content_space[1] and counter not in edge_titles:
            title_commas = True
            title_length = 2
            while '"' not in content_space[title_length]:
                title_length += 1
            title = ""
            for i in range(1, title_length + 1):
                title += content_space[i] + ","
            title = title[:-1] # remove trailing comma
        # extreme edge case, quotes and commas in titles
        elif counter in extra_edge_titles:
            if counter == 8259:
                title = "Monday's TV highlights: 'Bones,\"\" 'The Maya Rudolph Show,\"\" and more - LA Times"
                title_length = 3
            elif counter == 65859:
                title = "If Trump Is a Fascist, Why Can't He Seize Power?"
                title_length = 2
            elif counter == 65863:
                title = "Sage, Ink: Identity Politics"
                title_length = 2
        else:
            title_length = 1
            title = content_space[1]
        if title[0] == '"':
            title = title[1:]
        if title[-1] == '"':
            title = title[:-1]
        title = title.strip()
        #if counter == 69586:
        #    print title, title_length

        # author 
        author_idx = 1 + title_length 
        # multiple author check
        if '"' in content_space[author_idx]:
            author_commas = True
            author_length = 2
            while '"' not in content_space[author_idx + author_length - 1]:
                author_length += 1
            author = ""
            for i in range(author_idx, author_idx + author_length):
                author += content_space[i] + ","
            author = author[:-1] # remove trailing comma
            if author[0] == '"':
                author = author[1:]
            if author[-1] == '"':
                author = author[:-1]
            author = author.decode('utf-8').strip()
        else:
            author_commas = False
            author_length = 1
            author = content_space[author_idx].strip()
        #if counter == 8259:
        #    print author

        # date (year, month, day)
        try:
            date_idx = 1 + title_length + author_length
            date = content_space[date_idx].split("-")
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        except:
            year = None
            month = None
            day = None

        # publication
        publication = content_space[-3].decode('utf-8').strip()

        # length
        length = int((content_space[-1].decode('utf-8').strip()))

        # content
        content_idx = 2 + title_length + author_length
        content = ""
        for i in range(content_idx, len(content_space)-5):
            content += content_space[i]
        if content[0] == '"':
            content = content[1:]
        if content[-1] == '"':
            content = content[:-1]

        # check to make sure we're parsing correctly
        int(content_space[-1])
        article = {"num": num, "title": title, "author": author, "year": year, "month": month, "day": day, "publication": publication, "length": length, "content": content}
        articles.append(article)

        '''
        if counter == 65547:
            print article
            import sys
            sys.exit()
        '''

        print(counter)
        line = fin.readline()
        counter += 1


fin.close()

print("done")
print(len(articles))

print("")

# create data structure
heads = []
descs = []
keywords = None
for article in articles:
    heads.append(article["title"])
    descs.append(article["content"])
data = (heads, descs, keywords)

print("writing to file")
fout = open("data.pkl", "w")
pkl.dump(data, fout)
fout.close()
print("complete")

#print counter
#for article in articles:
#    print article["num"]
