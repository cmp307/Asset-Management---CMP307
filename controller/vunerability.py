import urllib.request, json, pprint, ssl


def vunerabilitySearch(query):
    try:
        with urllib.request.urlopen("https://services.nvd.nist.gov/rest/json/cves/1.0?namingFormat=2.3&keyword="+query) as url:
            data = json.loads(url.read().decode())
        return data
    except:
        ssl._create_default_https_context = ssl._create_unverified_context
        with urllib.request.urlopen("https://services.nvd.nist.gov/rest/json/cves/1.0?namingFormat=2.3&keyword="+query) as url:
            data = json.loads(url.read().decode())
        return data


def format (data):
    desc = []
    rating = []
    for c in range(data['resultsPerPage']):
        desc.append(data['result']['CVE_Items'][c]['cve']['description']['description_data'][0]['value'])
        try:
            rating.append(data['result']['CVE_Items'][c]['impact']['baseMetricV3']['cvssV3']['baseSeverity'])
        except:
            rating.append('no rating avaliable')
    return data['resultsPerPage'], desc, rating



