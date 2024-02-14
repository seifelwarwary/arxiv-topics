# %%
# RO - Robotics
# LG - Machine Learning
# CV - Computer Vision
# CL - Computational Linguistics
# AI - Artificial Intelligence

# %%
import urllib, urllib.request
import xml.etree.ElementTree as ET

def parse_data(xml_string):
    # Define the namespace
    ns = {'default': 'http://www.w3.org/2005/Atom'}
    
    root = ET.fromstring(xml_string)
    entries = root.findall('default:entry', ns)
    
    res=[]
    for entry in entries:
        res.append({
            'title': entry.find('default:title', ns).text if entry.find('default:title', ns) is not None else None,
            'id': entry.find('default:id', ns).text if entry.find('default:id', ns) is not None else None,
            'authors': [author.find('default:name', ns).text for author in entry.findall('default:author', ns)],
            'abstract': entry.find('default:summary', ns).text if entry.find('default:summary', ns) is not None else None,
            'categories': [category.attrib['term'] for category in entry.findall('default:category', ns)],
            'published': entry.find('default:published', ns).text if entry.find('default:published', ns) is not None else None,
            'pdf_link': [ link.attrib['href']  for link in entry.findall('default:link', ns) if 'pdf' in link.attrib['href']] if entry.find('default:link', ns) is not None else None,
        })
    return res



# %%
all_data=[]
for i in range(0, 1000):
    print(i,end=',')
    try:    
        url = f'http://export.arxiv.org/api/query?search_query=cat:cs.LG+OR+cat:cs.AI+OR+cat:cs.CV+OR+cat:cs.CL&start={1000*i}&max_results=1000&sortBy=submittedDate&sortOrder=descending'
        data = urllib.request.urlopen(url).read().decode('utf-8')
    except:
        continue
    all_data.extend(parse_data(data))
    print(i,' ended')
import pickle
with open('./data/arxiv_data.pkl', 'rb') as f:
    pickle.dump(all_data, f)    
    


