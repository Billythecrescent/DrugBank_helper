from urllib.request import urlopen
import re
import os
import csv
import time
from sys import argv

#1.0 scratch the search result webpage for information about the indication and the drugs accociated, but only that single page.
#2.0 is able to get the total result and the all pages linked, and can scratch the linked result as well.
#3.0 can formulate the result pattern in the .txt file, and is able to put in different key words.
#4.0 Use argv to specify the search key word, and generate a txt/csv file report.

keyword = argv[1]
filetype = argv[2]
url = "https://www.drugbank.ca/unearth/q?utf8=%E2%9C%93&searcher=indications&query=" + '+'.join(keyword.split('_'))
print(url)
#url = "https://www.drugbank.ca/unearth/q?utf8=%E2%9C%93&query=Cancer&searcher=indications"

def FindPageLink(url):
    #获取url页面信息
    try:
        response = urlopen(url)
    except OSError:
        print("url open error")
    else:
        print("It is searching for %s" %url)
    
    if (response and response.getcode()==200):
        #print (response.read().decode('utf-8'))  
        content = response.read().decode('utf-8')
    else:
        print("url page error")
        return None
    #print(content)
    #匹配结果总个数
    PageInfoRegex = re.compile(r'''(
        <div\sclass=.page.info.>
        (.*?)
        <b>\d+&nbsp;-&nbsp;(\d+)</b>.*?<b>
        (\d+)
        </b>.*?</div>
    )''',re.VERBOSE)
    
    #print(PageInfoRegex.findall(content))
    restitle = PageInfoRegex.findall(content)[0][1] #'Displaying indication'
    eachpagenum = PageInfoRegex.findall(content)[0][2]
    totalnum = PageInfoRegex.findall(content)[0][3] # 193

    pagenum = int(totalnum)//int(eachpagenum)+1

    #匹配各个页面链接的url
    #link to the second page to find the page url pattern
    PageLinkRegex = re.compile(r'''(
        <a\srel=.next.\sclass=.page-link.\s
        href=
        "(.*?page=)2(.*?)">\d+?</a></li>
    )''',re.VERBOSE)

    #print(PageLinkRegex.findall(content))

    #将结果总个数和url链接返回
    #return values
    #(totolnum,pagenum,[links])
    
    links = []
    for i in range(2,pagenum+1):
        link = "https://www.drugbank.ca" + PageLinkRegex.findall(content)[0][1] + str(i) + PageLinkRegex.findall(content)[0][2]
        links.append(link)
    
    return(totalnum, pagenum, links)

#FindPageLink(url)

#create a function to analyse the url, the output is a tuple ([(),()],[[(),()][()]]), in which respectivelys the indication and the drug
def DrugOfUrl(url):
    #obtain url content
    try:
        response = urlopen(url)
    except OSError:
        print("url open error")
    else:
        print("It is searching for %s" %url)
    
    if (response and response.getcode()==200):
        #print (response.read().decode('utf-8'))  
        content = response.read().decode('utf-8')
    else:
        print("url page error")
        return None

    ###  for test   ###
    #fo = open(outFile,'w')
    #fo.write(content)
    #string = 'mb-sm-2"><h2 class="hit-link"><a href="/indications/DBCON0034613">Malignancies</a></h2><div class="search-highlights"><small class="text-muted">Matched Synonyms: &hellip; <em>Cancer</em> ... <em>Cancer</em> NOS ... <em>Cancer</em> (NOS) &hellip; <br /></small></div><h3>Drugs:</h3><div class="db-matches"><a href="/drugs/DB01234">Dexamethasone</a> / <a href="/drugs/DB14104">Linoleic acid</a> / <a href="/drugs/DB13200">Lipegfilgrastim</a> / <a href="/drugs/DB00351">Megestrol acetate</a> / <a href="/drugs/DB00959">Methylprednisolone</a> / <a href="/drugs/DB01141">Micafungin</a> / <a href="/drugs/DB00745">Modafinil</a> / <a href="/drugs/DB00620">Triamcinolone</a> / <a href="/drugs/DB00577">Valaciclovir</a></div></div></div><div class="unearth-search-hit my-1"><div class="search-result pathway-search-result p-2 mb-4 p-sm-3 mb-sm'
    ###   for test  ###

    #create regex
    indicationRegex = re.compile(r'''(
        <h2\sclass=.hit-link.><a\shref=./
        (indications/[A-Z0-9]+)
        .>(.*?)</a></h2>
    )''',re.VERBOSE)

    drugRegex = re.compile(r'''(
        <h3>Drugs:</h3><div\sclass=.db-matches.>
        <a\shref=./drugs/[A-Z0-9]+.>.*?</a>
        #(\s/\s<a\shref=./(drugs/[A-Z0-9]+).>(.*?)</a>)*
        </div>
    )''',re.VERBOSE)

    #find matches in content
    #print(indicationRegex.findall(content))
    #print("-------------------------------------")
    #print(drugRegex.findall(content))

    indication,drugs = [],[]
    ##store the indication information into the list with the format of (num,name)
    for groups in indicationRegex.findall(content):
        indication.append((groups[1],groups[2]))

    #二次匹配药物信息
    #store the grug information as indication with the format of ((num,name),(num,name)...)
    drugpRegex = re.compile(r'''(
        <a\shref=./drugs/([A-Z0-9]+).>(.*?)</a>
    )''',re.VERBOSE)
    for drugsinfo in drugRegex.findall(content):
        druglist = drugpRegex.findall(drugsinfo)
        #print("#################")
        #print(druglist)
        lst = []
        for i in druglist:
            temp = (i[1],i[2])
            lst.append(temp)
        drugs.append(lst)
    
    #print("indication")
    #print(indication)
    #print("drugs")
    #print(drugs)

    return indication,drugs 
    

#write matches into .csv file
def WriteIntoCSV(csvpath, indication, drugs):
    csvFile = open(csvpath, "w")
    writer = csv.writer(csvFile)
    fileHeader = ['indication','drug']
    # 写入的内容都是以列表的形式传入函数
    writer.writerow(fileHeader)
    result = []
    for i in range(len(indication)):
        row = ["%s %s" %(indication[i][1], "https://www.drugbank.ca/"+indication[i][0])]
        for j in drugs[i]:
            row.append("%s %s" %(j[1],"https://www.drugbank.ca/"+j[0]))
        result.append(row)
    #print(result)
    for i in result:
        writer.writerow(i)
    csvFile.close()
    print(csvpath+" file is generated")
    

#write matches into .txt file
def WriteIntoTxt(url, txtpath, indication, drugs):
    txtFile = open(txtpath,'w')
    total_num, page_num, search_links = FindPageLink(url)
    local_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    description = "Created by MC.Hou's program at %s.\nThere are %s search results about %s by DrugBankSpider.\n\n" %(local_time,total_num,keyword)
    print(description,file = txtFile)
    for i in range(len(indication)):
        print("Indication:",file=txtFile)
        print("%s %s" %(indication[i][1], "https://www.drugbank.ca/"+indication[i][0]),file = txtFile)
        print("Drugs:",file = txtFile)
        for j in drugs[i]:
            print("%s %s" %(j[1],"https://www.drugbank.ca/"+j[0]),file = txtFile)
        print("\n",file = txtFile)
    txtFile.close()
    print(txtpath+" file is generated")
    



total_num, page_num, search_links = FindPageLink(url)
#print(total_num,page_num,search_links)

total_indication, total_drugs = DrugOfUrl(url)
for i in range(page_num-1):
    temp = DrugOfUrl(search_links[i])
    total_indication += temp[0]
    total_drugs += temp[1]

#print(total_indication)
#print(total_drugs)
csvpath = os.path.join(os.getcwd(),"drugresult_"+keyword+".csv")
txtpath = os.path.join(os.getcwd(),"drugresult_"+keyword+".txt")
if filetype == 'csv':
    WriteIntoCSV(csvpath,total_indication,total_drugs)
elif filetype == 'txt':
    WriteIntoTxt(url, txtpath, total_indication, total_drugs)
else:
    print("output error!")

#txtpath = "C://Users/mxdwa/Documents/file/drugresult_cancer.txt"
#WriteIntoTxt(url, txtpath, total_indication, total_drugs)