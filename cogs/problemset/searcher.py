'''
    @author : Nghi Gia
    this is an open-source project so everyone can read, edit and use this code for another program

    == love u my crushhhhh :3 ==
'''
import os
import requests
import lxml
import bs4
import re
import random
import regex as re
import urllib
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import json

# Đường link của các trang web cần sử dụng (được chia làm nhiều đoạn để tiện ghép nối với các tham số phụ)
URL = {'google': ['https://www.google.com/search?q=typefile%3Apdf+', '&rlz='],
            'springer' : ['https://link.springer.com/search?query=', ''],
            'codeforces' : ['https://codeforces.com/problemset?tags=', ''],
            'codeforces_contest' : ['https://codeforces.com/contests'],
            'codechef': ['https://www.codechef.com/get/tags/problems/', ''],
            'codechef_contest' : ['https://www.codechef.com/api/list/contests/all?sort_by=START&sorting_order=asc&offset=0&mode=premium'],
            'hackerrank': ['https://www.hackerrank.com/rest/contests/master/tracks/', '/challenges?offset=', '&track_login=true', '']
    }

# Class này chứa tất cả lệnh trả về ngẫu nhiên bài tập trên codeforces, codechef và hackerrank (bỏ luyencode vì số lượng bài
#tập quá ít và leetcode vì phải trả phí). Tương lai có thể update thêm vnoi, codelearn... (hên xui:v)

class get_link():

    def __init__(self):
        '''
        Do nothing here
        '''
        pass

    # ====== Codeforces ======

    def cf_searching_problem(tag = '', be_diff = 600, en_diff = 3600, num = 1):
        '''
        Hàm này dùng để lấy ngẫu nhiên [num] bài toán trên codeforces dựa trên tag và khoảng độ khó

        == PARAMETERS ==
        tag: tag của bài tập cần tìm
        be_diff: độ khó tối thiểu cần tìm
        en_diff: độ khó tối đa cần tìm
        num: số lượng bài tập trả về

        == STEPS ==
        - vào server codeforces và tìm số lượng trang bài tập bằng cách tìm thẻ các thẻ <span> nằm ở cuối trang hiển
        thị thanh < 1 2 3 ... 5 > (ví dụ) và đếm xem có bao nhiêu thẻ có chứa 'page-index' cũng chính là số lượng trang
        bài tập.
        - chọn ngẫu nhiên 1 trang bài tập
        - tạo [_link] dựa vào các parameters
        - vào [_link] và tìm các thẻ <a> có href chứa '/problemset/problem/' cũng chính là prefix của link dẫn đến trang
        bài tập và đếm số lượng bài tập có trong đó (đề phòng trường hợp trang có ít bài tập hơn [num])
        - lấy ngẫu nhiên [num] bài tập trong trang và trả về kết quả

        '''
        #_url là biến chứa link trang codeforces problemset được xây dựng dựa trên tag, be_diff, en_diff và num
        _url = URL['codeforces'][0] + tag + ',' + str(be_diff) + '-' + str(en_diff) 

        response = requests.get(_url)
        soup = BeautifulSoup(response.text, 'lxml')

        # Lấy số lượng trang bài tập
        page_num = 0
        pages = soup.find_all('span')
        for page in pages:
            _page = page.get('class', [])
            if ('page-index' in _page):
                page_num += 1
        
        # Lấy ngẫu nhiên 1 trang bài tập
        use_page_num = random.randint(0, page_num)

        if (use_page_num > 1):
            _link = 'https://codeforces.com/problemset/page/' + str(page_num) +'?tags=' + tag + ',' + str(be_diff) + '-' + str(en_diff)

        response = requests.get(_url)
        soup = BeautifulSoup(response.text, 'lxml')

        num_problem = 0
        problems = soup.find_all('a', href = True)

        problem_list = []

        # Lấy số lượng bài tập trong trang đồng thời lưu lại các link dẫn tới bài tập đó
        for problem in problems:
            _href = problem.get('href', [])
            if ('/problemset/problem/' in _href and str(_href) not in problem_list):
                num_problem += 1
                problem_list.append(str(_href))

        # Biến trả về 
        res = []
        if (num > num_problem):
             num = num_problem

        # Lấy random [num] bài tập sau đó append vào [res]
        # Mỗi phần tử trong res có dạng [<link bài tập>, <tựa bài>]
        for i in range(num):
            _problem = random.randint(1, num_problem)
            _problem_url = 'https://codeforces.com' + problem_list[_problem - 1]
            st = str(_problem_url).split('/')
            _problem_title = 'Problem - '+ str(st[5]) + str(st[6]) +' - Codeforces'
            res.append([_problem_url, _problem_title])

        return res

    def cf_tags():
        '''
        Hàm này trả về tất cả tag có thể dùng để lọc problem trong codeforces problemset

        == STEPS ==
        - vào server codeforcse tìm tất cả thẻ <option>, thẻ này sẽ chứa giá trị 'value' là giá trị của tag
        '''
        _url = URL['codeforces'][0][:-6]
        req = Request(_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = webpage = urlopen(req)
        soup = BeautifulSoup(webpage,'html.parser')
        tags = soup.find_all('option')

        res = []

        for tag in tags:
            res.append(str(tag.get('value', [])))
        
        return res[1:]
            
            



    # ====== Code Chef ======

    def cc_searching_problem(tag = '', num = 1):
        '''
        Hàm này dùng để lấy ngẫu nhiên [num] bài toán trên codechef dựa trên tag và số lượng bài
        // sau này có thể sẽ thêm độ khó
        
        == PARAMETERS ==
        tag: tag của bài tập cần tìm
        num: số lượng bài tập trả về

        == STEPS ==
        - vào server của codechef để lấy bài tập, để lấy được bài tập phải thông qua 1 trang có dạng json 
        // Lúc code hàm này em chưa biết vụ pamameters trong json nên code chay :>
        - sau khi tách được các bài tập trong file json, loop qua và lấy bài tập kèm tags và số lượng người giải được bài đó (để sau này xếp lại
        theo số lượng người giải được // chưa làm)
        - Lấy ngẫu nhiên [num] bài tập và trả về

        '''
        _url = URL['codechef'][0] + tag
        req = Request(_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)

        # load link json
        data_json = json.loads(webpage.read())
        # phân tách xâu [st] (là link json đã được convert sang string)
        st = str(data_json).split('}, ')
        st[0] = st[0][18:]
        st[-1] = ''
        
        problem_list = []

        # Loop qua toàn bộ phần tử tách được để tìm bài tập
        for data in st:
            if (data == ''):
                continue
            temp_items = re.split("'", data)
            items = []
            for i, item in enumerate(temp_items):
                if (i > 1 and 'solved_by' in temp_items[i-1]):
                    items.append(item)
                elif (',' not in item and ':' not in item and "\\" not in item and ')' not in item):
                    items.append(item)

            # item[1] là mã bài tập
            # item[5] là tựa bài tập
            problem_tags = []
            problem_code = items[1]
            problem_name = items[5]
            problem_solve = 0


            intag = 0
            for item in items:
                if (item == 'author'):
                    intag = 0
                elif (intag == 1):
                    problem_tags.append(item)
                elif (item == 'tags'):
                    intag = 1
                elif (':' in item):
                    problem_solve = int(item[2:-2])

            # Mỗi phần tử trong problem_list có dạng [problem_code, problem_name, problem_tags, problem_solve (số lượng người giải được)]
            problem_list.append([problem_code, problem_name, problem_tags, problem_solve])
        
        res = []

        # Lặp qua [num] lần và lấy ngẫu nhiên [num] bài tập để trả về
        # Mỗi phần tử trong res có dạng [<Tựa bài tập>, <link bài tập>]
        for i in range(num):
            idx = random.randint(0, len(problem_list)-1)
            _title = problem_list[idx][1]
            _link = 'https://www.codechef.com/problems/' + problem_list[idx][0]
            res.append([_title, _link])

        return res

    def cc_tags(type = ''):
        '''
        Hàm này trả về tất cả tag có thể dùng để lọc problem trong codechef
        Trong codechef tags được chia làm 4 loại theo độ khó, topics, tác giả, người chỉnh sửa và contests nhưng ở đây hàm chỉ trả về 
        theo 1 trong 2 loại là độ khó và topics.
        
        == PARAMETERS == 
        type: loại tags, hàm chỉ hoạt động đúng khi 1 type là trong 2 loại là độ khó và topics.

        == STEPS ==
        - Codechef lưu trữ tất cả tag trong 1 trang kiểu json
        // Lúc code hàm này em chưa biết vụ pamameters trong json nên code chay :>
        - Lần lượt tách data_json để đến cuối cùng thu được các tags có từ 10 bài tập trở lên
        '''
        _url = 'https://www.codechef.com/get/tags/problems'
        req = Request(_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        data_json = json.loads(webpage.read())
        all_tags = str(data_json).split('}, {')
        used_tags = []
        for tag in all_tags:
            tmp = tag[22:]
            if ('difficulty' in tag):
                used_tags.append(tag)
            elif ('actual_tag' in tag and int(tmp[tmp.find("count':")+8:]) >= 10): # chỉ lấy tags có số lượng bài tập >= 10
                used_tags.append(tag)
        tags = [re.split("': '|', '|': ", tag) for tag in used_tags]
        res = []
        # Mỗi phần tử trong res là 1 tag
        if (type == 'topics'):
            type = 'actual_tag'
        for tag in tags:
            if (tag[3] == type):
                res.append(tag[1])
        
        return res



    # ====== hackerrank ======

    def hr_searching_problem(skill = '', status = [], skills = [], difficulty = [], subdomains = [], num = 1):
        '''
        Hàm này dùng để lấy ngẫu nhiên [num] bài toán trên codechef dựa trên các tham số và số lượng bài yêu cầu
        
        == PARAMETERS ==
        skill: là một skill muốn lấy bài tập (ví dụ cpp, c, python, mathematics...)
        status: là trạng thái của bài tập, có 2 trạng thái là solved và unsolved tương ứng với đã làm và chưa làm
        skills: là kỹ năng cần có để giải bài tập, hackerrank thường sẽ phân biệt theo một kỹ năng nào đó được phân thành Basic, Advanced và Intermediate
        difficulty: là độ khó của bài tập, thường được chia làm 3 mức: easy, medium và hard
        subdomains: là dạng bài tập yêu cầu
        num: là số lượng bài tập trả về

        == STEPS ==
        - Đầu tiên là xây dựng link dựa trên các tham số đầu vào
        - Hackerrank lưu tất cả bài tập dưới dạng json
        // lần này kinh nghiệm hơn rùi :>
        - Đọc file json và lấy tất cả giá trị của 'slug' trong 'models'
        - Lấy ngẫu nhiên [num] bài tập để trả về

        '''
        # Cấu trúc đường link của hackerrank khá rườm rà và được chia thành nhiều dạng tham số đầu vào
        # Thứ tự các tham số đầu vào không quan trọng
        _url_1 = URL['hackerrank'][0] + skill + URL['hackerrank'][1]
        _url_2 = ''
        if (len(status) > 0):
            for item in status:
                _url_2 += '&filters%5Bstatus%5D%5B%5D=' + str(item.replace(' ', '%20').replace('(', '%28').replace(')', '%29'))
        if (len(skills) > 0):
            for item in skills:
                _url_2 += '&filters%5Bskills%5D%5B%5D=' + str(item.replace(' ', '%20').replace('(', '%28').replace(')', '%29'))
        if (len(difficulty) > 0):
            for item in difficulty:
                _url_2 += '&filters%5Bdifficulty%5D%5B%5D=' + str(item.replace(' ', '%20').replace('(', '%28').replace(')', '%29'))
        if (len(subdomains) > 0):
            for item in subdomains:
                _url_2 += '&filters%5Bsubdomains%5D%5B%5D=' + str(item.replace(' ', '%20').replace('(', '%28').replace(')', '%29'))
        problem_list = []

        # Mỗi trang hackerrank sẽ có 10 bài tập và muốn lấy một số lượng bài tập lớn hơn (để random hiệu quả hơn), vòng lặp sau sẽ lặp tối đa 20
        #lần và thêm tham số page để có thể lấy tối đa 200 bài tập
        for i in range(20):
            _url = _url_1 + str(i*10) + _url_2 + URL['hackerrank'][2]
            req = Request(_url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req)
            soup = BeautifulSoup(html,'html.parser')
            site_json=json.loads(soup.text)

            # lấy tất cả giá trị của 'slug' chứa mã bài tập trong 'models'
            tmp = [d.get('slug') for d in site_json['models'] if d.get('slug')]
            if (len(tmp) == 0):
                break
            problem_list += tmp

        if (num > len(problem_list)):
            num = len(problem_list)
        
        res = []

        # Lấy ngẫu nhiên [num] bài tập để trả về
        # Mỗi phần tử trong res có dạng [<tựa bài (xây dựng dựa trên mã bài)>, <link bài>]
        for i in range(num):
            idx = random.randint(0, len(problem_list)-1)
            _title = problem_list[idx]
            _link = 'https://www.hackerrank.com/challenges/' + _title + '/problem'
            res.append([_title.replace('-', ' '), _link])

        return res

    def hr_skills():
        '''
        Hàm này trả về tất cả các skill có trong hackerrank

        == STEPS ==
        - Vào trang của hackerrank và tìm tất cả thẻ <div> có class = 'track-name', lấy giá trị của 'data-automation'
        '''
        _url = 'https://www.hackerrank.com/dashboard'
        req = Request(_url, headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        soup = BeautifulSoup(webpage, 'html.parser')
        skills = soup.find_all('div', class_ = 'track-name')

        res = []

        # Mỗi phần tử trong res là một skill trên hackerrank
        for skill in skills:
            res.append(str(skill.get('data-automation', [])))

        return res

    def hr_tags(skill = ''):
        '''
        Hàm này trả về tất cả các tags có trong skill trên hackerrank 

        == PARAMETERS ==
        - skill: skill cần lấy tags

        == STEPS ==
        - Vào trang của skill trong hackerrank tìm tất cả thẻ <input> có class = 'checkbox-input'
        - Phân loại tag dựa trên cách phân loại trong hackerrank:
            + status: là trạng thái của bài tập, có 2 trạng thái là solved và unsolved tương ứng với đã làm và chưa làm
            + skills: là kỹ năng cần có để giải bài tập, hackerrank thường sẽ phân biệt theo một kỹ năng nào đó được phân thành Basic, Advanced và Intermediate
            + difficulty: là độ khó của bài tập, thường được chia làm 3 mức: easy, medium và hard
            + subdomains: là dạng bài tập yêu cầu
        '''
        _url = 'https://www.hackerrank.com/domains/' + skill
        req = Request(_url, headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        soup = BeautifulSoup(webpage, 'html.parser')
        tags = soup.find_all('input', class_ = 'checkbox-input')

        # Phân chia tags
        # res là 1 biến kiểu từ điển
        res = {'status' : [], 'skills' : [], 'difficulty' : [], 'subdomains' : []}
        for tag in tags:
            st = str(tag.get('value', []))
            if ('solved' in st):
                res['status'].append(st)
            elif ('(' in st):
                res['skills'].append(st.replace(' ', '+'))
            elif  ('easy' in st or 'medium' in st or 'hard' in st):
                res['difficulty'].append(st)
            else:
                res['subdomains'].append(st)

        return res



# Class này chứa tất cả lệnh tìm kiếm và trả về các contest sắp diễn ra trên codeforces, codechef
# // sau có thể mở rộng thêm ..

class get_contest():

    def __init__(self):
        '''
        do nothing here
        '''
        pass

    def codechef_contest():
        '''
        Hàm này sẽ đi tìm contest sắp diễn ra gần nhẩt trên codechef

        == STEPS ==
        - codechef lưu các contest sắp diễn ra, đã diễn ra hoặc đang diễn ra trong 1 link dạng json, do đó bước đầu tiên
        là load link json đó
        - Lấy 'contest_code' và 'contest_name' trong 'present_contests', tương ứng với code và tên của contest sắp diễn ra (gần nhất), 
        các contest xa hơn có thể sẽ bị lỗi hoặc chưa có image nên không lấy
        - Lấy url của banner contest sắp tới
        '''
        _url = URL['codechef_contest'][0]
        req = Request(_url, headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        data_json = json.loads(webpage.read())
        contest_code = data_json['present_contests'][0].get('contest_code')
        contest_name = data_json['present_contests'][0].get('contest_name')
        # url file chứa link banner
        _url = 'https://www.codechef.com/api/contests/' + str(contest_code)
        req = Request(_url, headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        data_json = str(json.loads(webpage.read()))
        # lấy mã của banner để xây dựng link file banner dưới dạng png
        _link = data_json[data_json.find('banner')+10:data_json.find('rules')-4]
        return [_link, 'https://www.codechef.com/' + str(contest_code), contest_name]

    def codeforces_contest():
        '''
        Hàm này sẽ đi tìm contest sắp diễn ra gần nhẩt trên codeforces

        == STEPS ==
        - vào server codeforces tìm tất cả thẻ <a> có class = 'red-link', 'red-link' là class codeforces dùng để hiển thị
        [Register >>], các contest cho register tương đương với việc sắp diễn ra trong thời gian gần.
        - để vào được trang register yêu cầu phải đăng nhập, do đó thay vì vào trang để lấy title h3 thì sẽ ở lại để crawl tiếp
        - Tìm tất cả thẻ <tr> có tham số 'data-contestid' để lấy contest ID rồi trong thẻ <tr> lại crawl tiếp tìm thẻ <td> để lấy
        tên contest và thời gian diễn ra contest
        '''
        _url = URL['codeforces_contest'][0]
        req = Request(_url, headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        soup = BeautifulSoup(webpage, 'html.parser')
        red_links = soup.find_all('a', class_ = 'red-link')

        contests_url = []

        for link in red_links:
            st = str(link.get('href', []))
            if ('Registration' in st):
                contests_url.append('https://codeforces.com/' + st)

        contest_id = [item[-4:] for item in contests_url]
        used_tr = []

        for tr in soup.find_all('tr'):
            st = str(tr.attrs)
            if ('data-contestid' in st and st[-6:-2] in contest_id):
                used_tr.append(tr)

        res = []
        # Mỗi phần tử trong res có dạng [<tên contest>, <link contest>, <thời gian diễn ra>]
        for i, tr in enumerate(used_tr):
            _title = str(tr.find_next('td'))
            st = _title.split('\n')
            _time = str(tr.find_next('span'))
            _time = _time[_time.find('>')+1:_time.find('</')]
            res.append([st[1][:-1], contests_url[i], _time])

        return res


# Test code
if __name__ == '__main__':
    #tmp = get_link.hr_searching_problem(skill = 'python', status = [], skills = [], difficulty = ['easy'], subdomains = [], num = 3)
    #for item in tmp:
    #    print(f'{item[0]} {item[1]}')
    tmp = get_contest.codeforces_contest()
    for item in tmp:
        print(f'{item[0]} | {item[1]} | {item[2]}')

