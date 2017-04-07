import requests
import csv
import itertools as _it
import operator as _op

from collections import Counter

PAGE_ITEMS = 50


def get_posts():
    posts_endpoint = (
        "http://eu-central-1.magazine.services.cs.stylight.net/"
        "site/de_DE/posts")
    data = requests.get(posts_endpoint).json()
    count = data['count']
    for i in range(int(count / PAGE_ITEMS)):
        params = {'page_items': PAGE_ITEMS, 'page': i}
        chunk = requests.get(posts_endpoint, params=params).json().get(
            'posts', [])
        yield chunk


def main():
    headers = [
        "posts.category.name",
        "posts.author.name",
        "posts.dateCreated",
        "posts.id",
        "posts.components",
        "posts.flexibleContent.component.ids",
        "posts.searchPageUrls",
        "posts.slug",
        "posts.seoTitle",
        "posts.title",
        "posts.sponsored"]

    filename = 'posts_data.csv'
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(headers)

        for posts in get_posts():
            for post in posts:
                try:
                    components = {
                        type_: len(list(group))
                        for type_, group in
                        _it.groupby(post['flexibleContent'],
                                    _op.itemgetter('type'))
                        }
                    ids = set([
                              id_ for component in post['flexibleContent'] if
                              component['type'] == 'products'
                              and component['component']['ids'] for id_ in
                              component['component']['ids']
                              ])
                except Exception as e:
                    print(post['flexibleContent'][-1])
                    print(post['id'])
                    raise

                writer.writerow([
                    post['category']['name'],
                    post['author']['name'],
                    post['dateCreated'],
                    post['id'],
                    str(components),
                    str(ids),
                    str(post['searchPageUrls']),
                    post['slug'],
                    post['seoTitle'],
                    post['title'],
                    post['sponsored'],
                ])


if __name__ == '__main__':
    main()