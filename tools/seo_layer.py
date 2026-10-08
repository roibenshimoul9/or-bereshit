"""Search engines and link previews, for the real site only (not the Claude preview).

Adds the title and description Google shows, the canonical address, the preview card used by
WhatsApp and Facebook, structured data that says "this is an online shop called אור בראשית",
and writes robots.txt and sitemap.xml next to index.html.

Google Search Console: paste the verification code (only the code, not the whole tag) into
tools/google-verification.txt and rebuild; the tag is then added to the page.
"""
import datetime
import json
import os

SITE = 'https://orbereshit.vercel.app'
NAME = 'אור בראשית'
TITLE = 'אור בראשית | יודאיקה ומוצרים לבית בהדפסת תלת־ממד'
DESC = ('אור בראשית: יודאיקה ומוצרים לבית בהדפסת תלת־ממד, לפי הזמנה. נרות זיכרון, מזוזות ונטלות '
        'בעיצוב אישי, פמוטים עם ברכה, שלטים לבית ומתנות עם הקדשה. משלוחים לכל הארץ.')
EMAIL = 'orbereshitt@gmail.com'
PHONE = '+972-54-684-3548'

LD = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': NAME,
     'alternateName': ['Or Bereshit', 'אור בראשית יודאיקה', 'orbereshit'],
     'inLanguage': 'he-IL', 'publisher': {'@id': SITE + '/#store'}},
    {'@type': 'OnlineStore', '@id': SITE + '/#store', 'name': NAME, 'alternateName': 'Or Bereshit',
     'url': SITE + '/', 'logo': SITE + '/apple-touch-icon.png', 'image': SITE + '/og.jpg',
     'description': DESC, 'email': EMAIL, 'telephone': PHONE,
     'areaServed': {'@type': 'Country', 'name': 'IL'},
     'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service',
                      'telephone': PHONE, 'email': EMAIL, 'availableLanguage': ['he']}},
]}


def apply(page, root):
    def rep(a, b, count=1):
        nonlocal page
        n = page.count(a)
        assert n == count, (a[:70], n)
        page = page.replace(a, b)

    tools = os.path.join(root, 'tools')
    code_file = os.path.join(tools, 'google-verification.txt')
    verify = ''
    if os.path.exists(code_file):
        code = open(code_file, encoding='utf-8').read().strip()
        if code:
            verify = '<meta name="google-site-verification" content="%s">\n' % code

    head = verify + '\n'.join([
        '<meta name="robots" content="index,follow,max-image-preview:large">',
        '<link rel="canonical" href="%s/">' % SITE,
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="%s">' % NAME,
        '<meta property="og:locale" content="he_IL">',
        '<meta property="og:url" content="%s/">' % SITE,
        '<meta property="og:title" content="%s">' % TITLE,
        '<meta property="og:description" content="%s">' % DESC,
        '<meta property="og:image" content="%s/og.jpg">' % SITE,
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<script type="application/ld+json">%s</script>' % json.dumps(LD, ensure_ascii=False),
    ]) + '\n'

    # the description Google prints under the link
    start = page.index('<meta name="description" content="')
    end = page.index('>', start) + 1
    page = page[:start] + '<meta name="description" content="%s">' % DESC + page[end:]
    rep('<meta name="theme-color"', head + '<meta name="theme-color"')

    # the tab title and the title Google shows; inner pages keep "<page> · אור בראשית"
    rep('<title>אור בראשית</title>', '<title>%s</title>' % TITLE)
    rep("`${TITLES[r]} · אור בראשית`:'אור בראשית';", "`${TITLES[r]} · אור בראשית`:'%s';" % TITLE)

    with open(os.path.join(root, 'robots.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: %s/sitemap.xml\n' % SITE)
    with open(os.path.join(root, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                '  <url><loc>%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
                '</urlset>\n' % (SITE, datetime.date.today().isoformat()))
    return page
