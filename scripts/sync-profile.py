"""Sync current biography and canonical entities into JSON-LD and llms.txt."""
from pathlib import Path
from html import unescape
import json,re
root=Path(__file__).resolve().parents[1]/'argelysoriach-site'
read=lambda p:json.loads((root/p).read_text())
write=lambda p,v:(root/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
home=(root/'biography/index.html').read_text()
bio=home.split('<section class="bio"',1)[1].split('<section class="writing-feature"',1)[0]
paragraphs=[unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'<p>(.*?)</p>',bio,re.S)]
assert len(paragraphs)>=6 and all(paragraphs), 'Expected complete biography page'
person=read('schema/person.json')
person['jobTitle']='Managing Principal'
person['worksFor']={'@id':'https://theangel.biz/#organization'}
person['affiliation']={'@id':'https://theangel.biz/#organization'}
person['hasOccupation']=[{'@type':'Occupation','name':name} for name in ['Angel Investor','Systems Architect','Artist','Performance Artist','Artistic Director','Multidisciplinary Artist','Actor','Vocalist','Writer','Engineer','Talent Architect','Developer','Angel Investor','Managing Principal']]
person['description']='Brooklyn-based angel investor, systems architect, and artist. Managing principal of Angel, an independent angel investment firm.'
person['mainEntityOfPage']={'@id':'https://gothamgay.com/#profilepage'}
person['alternateName']=['The Angel','Sam Oriach','Argelys Oriach']
person['homeLocation']={'@type':'Place','name':'Crown Heights, Brooklyn, New York'}
person['hasCredential']={'@type':'EducationalOccupationalCredential','name':'Bachelor’s degree in English','credentialCategory':'Bachelor’s degree','recognizedBy':{'@type':'CollegeOrUniversity','name':'Wesleyan University'}}
if not any(x.get('name')=='Northwestern University' for x in person['alumniOf']):
 person['alumniOf'].append({'@type':'CollegeOrUniversity','name':'Northwestern University','description':'National High School Institute (Cherubs) theatre program, 2010.'})
person['knowsAbout']=['Multidisciplinary art','Performance','Movement','Artistic direction','Artist development','Talent architecture','Systems architecture','Software development','Live production','Writing','Studio art','Critical theory','Alexander Technique']
write('schema/person.json',person)
organizations=read('schema/organizations.json')
for org in organizations['@graph']:
 if org.get('@id')=='https://seveneightythree.com/#organization':
  org['description']='Systems laboratory and venture foundry building zero-dependency digital infrastructure and the Universe API. An operating lab of Angel.'
  org['parentOrganization']={'@id':'https://theangel.biz/#organization'}
 if org.get('@id')=='https://wildlakestudio.com/#organization':
  org['name']='Wild Lake Studio';org['alternateName']='Wild-Lake'
  org['description']='Talent architecture and sovereign A&R operating lab of Angel, building operational, somatic, and digital infrastructure for independent artists with zero ownership or backend percentages.'
  org['parentOrganization']={'@id':'https://theangel.biz/#organization'}
write('schema/organizations.json',organizations)
website=read('schema/website.json');website['name']='Argelys Samuel Oriach | The Angel';website['alternateName']=['The Gotham Gay','Argelys Samuel Oriach'];website['description']='Angel (Angel Ventures, theangel.biz) is the angel investment firm of Argelys Samuel Oriach, housing operating labs Seven Eighty Three and Wild Lake Studio alongside eight internal portfolio assets.';write('schema/website.json',website)
summary='Brooklyn-based performance artist, artistic director, and systems architect. Principal of Seven Eighty Three (Lab 783) and founder of Wild Lake Studio (Wild-Lake).'
canonical={x['@id']:{k:v for k,v in x.items() if k!='@context'} for x in [person,website,*organizations['@graph']]}
canonical['https://gothamgay.com/#profilepage']={'@type':'ProfilePage','@id':'https://gothamgay.com/#profilepage','url':'https://gothamgay.com/','name':'Argelys Samuel Oriach | The Angel','description':website['description']}
story=next(w for w in read('schema/works.json')['@graph'] if w.get('name')=='This Is Not a Love Story (Yankees)')
canonical.update({node['@id']:node for node in read('schema/works.json')['@graph'] if node.get('@type') in ['SoftwareApplication','WebApplication']})
def sync(x):
 if isinstance(x,list):return [sync(v) for v in x]
 if not isinstance(x,dict):return x
 if x.get('name')=='This Is Not a Love Story (Yankees)' and x.get('@type')=='ShortStory':
  x={**x,'description':story['description'],'genre':story['genre']}
 if x.get('@type')=='Person' and (x.get('@id')==person['@id'] or x.get('name') in ['Argelys Samuel Oriach','Argelys Oriach']):
  x={**x,'alternateName':person['alternateName'],'description':person['description']}
 # Expand only existing entity definitions; keep ID-only relationships intact.
 if x.get('@id') in canonical and '@type' in x:
  return {**x,**canonical[x['@id']]}
 return {k:sync(v) for k,v in x.items()}
deployments=read('schema/deployments.json')
deployment_ids=[entry['item']['@id'] for entry in deployments['itemListElement']]
biography_graph=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',home,re.S)[1])['@graph']
deployment_definitions={node['@id']:node for node in biography_graph if node.get('@id') in deployment_ids}
deployment_definitions.update({key:value for key,value in canonical.items() if key in deployment_ids})
def sync_deployments(data,relative_path):
 if relative_path not in ['index.html','biography/index.html'] or '@graph' not in data:return data
 graph=data['@graph']
 definitions={**deployment_definitions,**{node['@id']:node for node in graph if node.get('@id') in deployment_ids}}
 indices=[i for i,node in enumerate(graph) if node.get('@id') in deployment_ids]
 slot=min(indices) if indices else len(graph)
 remaining=[node for node in graph if node.get('@id') not in deployment_ids and node.get('@id')!=deployments['@id']]
 ordered=[definitions[key] for key in deployment_ids]
 graph=remaining[:slot]+ordered+remaining[slot:]
 refs=[{'@id':key} for key in deployment_ids]
 page_id='https://gothamgay.com/#profilepage' if relative_path=='index.html' else 'https://gothamgay.com/biography/#page'
 page=next((node for node in graph if node.get('@id')==page_id),None)
 if page is None:
  page={'@type':'WebPage','@id':page_id,'url':'https://gothamgay.com/biography/','name':'Argelys Samuel Oriach | Biography','isPartOf':{'@id':'https://gothamgay.com/#website'}}
  graph.append(page)
 page['mentions']=refs
 parts=page.get('hasPart',[])
 if isinstance(parts,dict):parts=[parts]
 page['hasPart']=[item for item in parts if item.get('@id')!=deployments['@id']]+[{'@id':deployments['@id']}]
 graph.append({k:v for k,v in deployments.items() if k!='@context'})
 return {**data,'@graph':graph}
pattern=r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)'
for path in root.rglob('*.html'):
 source=path.read_text()
 def replace(m):
  data=json.loads(m[2]);updated=sync_deployments(sync(data),path.relative_to(root).as_posix())
  if data==updated:return m[0]
  return m[1]+'\n'+json.dumps(updated,ensure_ascii=False,indent=2)+'\n'+m[3]
 result=re.sub(pattern,replace,source,flags=re.S)
 if path in [root/'index.html',root/'biography/index.html']:
  for attr,key in [('name','description'),('property','og:description'),('name','twitter:description')]:
   result=re.sub(rf'(<meta {attr}="{key}" content=")[^"]*',lambda m:m[1]+(website['description'] if path==root/'index.html' else summary),result)
 if path==root/'index.html':
  result=re.sub(r'<title>.*?</title>',lambda m:'<title>Argelys Samuel Oriach | The Angel - Performance Artist, Systems Architect &amp; Angel Investor</title>',result)
  for attr,key in [('property','og:title'),('name','twitter:title')]:
   result=re.sub(rf'(<meta {attr}="{key}" content=")[^"]*',lambda m:m[1]+'Argelys Samuel Oriach | The Angel',result)
 if result!=source:path.write_text(result)
llms=root/'llms.txt';text=llms.read_text();text=text.replace('Systems architecture, art, and talent infrastructure.','Systems Architect & Performance Artist.')
text=re.sub(r'\n## Biography\n.*?(?=\n## |\Z)','',text,flags=re.S)
text=text.replace('\n## Current practice','\n## Biography\n\n'+'\n\n'.join(paragraphs)+'\n\n## Current practice',1)
text=text.replace('Talent architecture, structural mentorship, and development of artistic work.','Research laboratory of Seven Eighty Three (Lab 783), guiding developing and independent artists. Structural stewardship, physical carrying capacity, and live production architecture.')
llms.write_text(text)
