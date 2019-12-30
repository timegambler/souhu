from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        self.crawler_process.crawl('souhuspider3')
        self.crawler_process.start()
        # spider_list = self.crawler_process.spiders.list()
        # print(spider_list)
        # for name in spider_list:
        #     self.crawler_process.crawl(name, **opts.__dict__)
        # self.crawler_process.start()