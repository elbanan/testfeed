import pandas, requests, re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def getJournalList(file:str):
    """
    Returns a list of journals from a file. The file is obtained from the PubMed and stored in static files. 
    """
    with open(file,'r') as file:
        data = file.read().split('\n')
    content = {'JrId':[], 'JournalTitle':[], 'MedAbbr':[], 'ISSN (Print)':[], 'ISSN (Online)':[], 'IsoAbbr':[], 'NlmId':[]}
    for i in data:
        for k, v in content.items():
            if k in i:
                v.append(i[len(k)+2:])   
    return pandas.DataFrame(content)  

def getPubmedIdList(journal_list:list, date_start:str, date_end:str, retmax:int=100):

    """
    Returns a list of PubMed IDs for a given journal list and date range.
    """
    if len(journal_list) > 1:
        journal_list = '[journal]+OR+'.join(str(item) for item in journal_list)+'[journal]'
    else:
        journal_list = journal_list[0]+'[journal]'
    query = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='+journal_list+'+AND+'+date_start+':'+date_end+'[pdat]'
    results = requests.get(query, params={'RetMax':retmax})
    content = BeautifulSoup(results.content, "xml")
    ids = [str(i)[4:-5] for i in content.find_all("Id")]
    return query, ids

def getPubmedIdInfo(idx:list):
    """
    Returns pandas dataframe containing detailed information for a given PubMed ID list. Information includes title, pubdate, journal, rid, and if it has abstract or not abstract.
    """
    article_list = ','.join(str(x) for x in idx)
    query = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id='+article_list
    results = requests.get(query)
    content = BeautifulSoup(results.content, "xml")
    index = ['Title', 'PubDate', 'Source', 'HasAbstract']
    output = {k:[i.text for i in content.find_all('Item', attrs={'Name':k})] for k in index}
    output['pubmed'] = [i.text for i in content.find_all('Item', attrs={'Name':'pubmed', 'Type': 'String'})]
    return query, pandas.DataFrame(output)

def getDatesFromToday(num_days:int=7):
    """
    Returns a tuple of dates from today to num_days in the future.
    """
    e = (datetime.today()).strftime("%Y/%m/%d")
    b = (datetime.today() - timedelta(days=num_days)).strftime("%Y/%m/%d")
    return b, e

def getAbstract(idx:list):
    """
    Returns a pandas dataframe containing abstracts for a given PubMed ID list.
    """
    idx_str = ','.join(idx) 
    query = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='+idx_str
    results = requests.get(query)
    results = BeautifulSoup(results.content, "xml")
    # abstracts = [str(x)[14:-15] for x in results.find_all('AbstractText')]
    abstracts = [cleanAbstract(x) for x in results.find_all('AbstractText')]
    return pandas.DataFrame(list(zip(idx, abstracts)), columns=['pubmed', 'abstract'])

def cleanAbstract(abstract:str):
    """
    Returns a cleaned abstract.
    """
    # abstract = str(abstract)[14:-15] #Removes 'AbstractText'
    # abstract = str(abstract).replace('<b>', '\n') #Removes bold tags with new lines
    # abstract = str(abstract).replace('</b>', '\n') #Removes bold tags with new lines
    clean = re.compile('<.*?>')
    return re.sub(clean, '', str(abstract))
    return abstract

def getIntervalUpdate(journal_list:list, start_date:str, end_date:str, retmax:int, abstract_only:bool=False):
    _, article_list = getPubmedIdList(journal_list,str(start_date), str(end_date), retmax=retmax)
    _, article_detail = getPubmedIdInfo(article_list)
    abstracts = getAbstract(article_detail[article_detail['HasAbstract']=='1'].pubmed.tolist())
    return pandas.merge(article_detail, abstracts, on='pubmed', how='outer')


def fix_date(str):
    str = str.replace(" " , "-")
    str = str.replace("Nov" , "11")
    str = str.replace("Dec" , "12")
    str = str.replace("Jan" , "01")
    str = str.replace("Feb" , "02")
    str = str.replace("Mar" , "03")
    str = str.replace("Apr" , "04")
    str = str.replace("May" , "05")
    str = str.replace("Jun" , "06")
    str = str.replace("Jul" , "07")
    str = str.replace("Aug" , "08")
    str = str.replace("Sep" , "09")
    str = str.replace("Oct" , "10")
    return str
    
