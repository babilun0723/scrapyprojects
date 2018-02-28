# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ExhibitorPipeline(object):
    def process_item(self, item, spider):

        if item is not None:
             with open('htmlpages/%s.html' % item['title'], 'w') as f:
                 f.write(item['html_detail'])
                 f.close()
        return item
