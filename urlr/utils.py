def determine_permalink(site, absolute_url):
    if len(site.domain) > 7:
        if site.domain.split('://')[0].startswith('http'):
            return '%s%s' % (site.domain, absolute_url)
    
    return 'http://%s%s' % (site.domain, absolute_url)
