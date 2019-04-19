from django.utils.safestring import mark_safe

"""分页工具"""
class Pagination:


    def __init__(self,page_num,all_count,params,per_num=10, max_show_page=11):
        # 初始值
        try:
            self.page_num = int(page_num)
            if self.page_num <= 0:
                self.page_num = 1
        except Exception as e:
            self.page_num = 1
        #URL参数
        self.params = params  #一个字典urlencode()
        # 总得数据量
        self.all_count = all_count
        # 每页显示数据条数
        self.per_num = per_num
        # 总的页码数
        self.total_page_num, more = divmod(all_count, per_num)
        if more:
            self.total_page_num += 1

        # 最大显示页数
        self.max_show_page = 11
        self.half_show_page = max_show_page // 2

    @property   #方法改成属性
    def start(self):
        '''
        数据切片的起始值
        :return:
        '''
        return (self.page_num-1) *self.per_num

    @property
    def end(self):
        '''
        数据切片的终止值
        :return:
        '''
        return self.page_num * self.per_num

    @property
    def page_html(self):

        if self.total_page_num < self.max_show_page:
            page_start = 1
            page_end = self.total_page_num
        elif self.page_num <= self.half_show_page:
            page_start = 1
            page_end = self.max_show_page
        elif self.page_num + self.half_show_page > self.total_page_num:
            page_start = self.total_page_num - self.max_show_page + 1
            page_end = self.total_page_num
        else:
            # 起始的页面
            page_start = self.page_num - self.half_show_page

            # 终止的页面
            page_end = self.page_num + self.half_show_page

        page_list = []

        # 首页
        if self.page_num:
            self.params['page'] = 1
            page_list.append('<li><a href="?{}">首页</a></li>'.format(self.params.urlencode()))
        # 上一页
        if self.page_num == 1:
            page_list.append('<li class="disabled"><a>上一页</a></li>')
        else:
            self.params['page'] = self.page_num-1  #{page:上一页的页码,query:'xxx'}  #page=1&query=xxx
            page_list.append('<li><a href="?{}">上一页</a></li>'.format(self.params.urlencode()))
            # page_list.append('<li><a href="?page={}">上一页</a></li>'.format(self.page_num - 1))

        for i in range(page_start, page_end + 1):
            self.params['page'] = i
            if i == self.page_num:
                page_list.append('<li class="active"><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
            else:
                page_list.append('<li><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))

        # 下一页
        if self.page_num == self.total_page_num:
            page_list.append('<li class="disabled"><a>下一页</a></li>')
        else:
            self.params['page'] = self.page_num + 1
            page_list.append('<li><a href="?{}">下一页</a></li>'.format(self.params.urlencode()))

        # 尾页
        if self.page_num:
            self.params['page'] = self.total_page_num
            # page_list.append('<li><a href="?page={}">尾页</a></li>'.format(self.total_page_num))
            page_list.append('<li><a href="?{}">尾页</a></li>'.format(self.params.urlencode()))
        return mark_safe(''.join(page_list))

