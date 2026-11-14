"""Sync current biography and canonical entities into JSON-LD and llms.txt."""
from pathlib import Path
from html import unescape
import json,re
root=Path(__file__).resolve().parents[1]/'argelysoriach-site'
read=lambda p:json.loads((root/p).read_text())
write=lambda p,v:(root/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
home=(root/'index.html').read_text()
bio=home.split('<section class="bio"',1)[1].split('<section class="writing-feature"',1)[0]
paragraphs=[unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'<p>(.*?)</p>',bio,re.S)]
assert len(paragraphs)>=6 and all(paragraphs), 'Expected complete homepage biography'
person=read('schema/person.json')
person['jobTitle']='Systems Architect & Performance Artist'
person['hasOccupation']=[{'@type':'Occupation','name':name} for name in ['Systems Architect','Performance Artist','Multidisciplinary Artist','Artistic Director','Actor','Vocalist','Writer','Engineer','Talent Architect','Developer']]
person['description']='Brooklyn-based artist, writer, and systems architect. Principal of Seven Eighty Three, founder of Wild Lake Studio.'
person['alternateName']='Argelys Oriach'
person['homeLocation']={'@type':'Place','name':'Brooklyn, New York'}
person['hasCredential']={'@type':'EducationalOccupationalCredential','name':'Bachelor’s degree in English','credentialCategory':'Bachelor’s degree','recognizedBy':{'@type':'CollegeOrUniversity','name':'Wesleyan University'}}
if not any(x.get('name')=='Northwestern University' for x in person['alumniOf']):
 person['alumniOf'].append({'@type':'CollegeOrUniversity','name':'Northwestern University','description':'National High School Institute (Cherubs) theatre program, 2010.'})
person['knowsAbout']=['Multidisciplinary art','Performance','Movement','Artistic direction','Artist development','Talent architecture','Systems architecture','Software development','Live production','Writing','Studio art','Critical theory','Alexander Technique']
write('schema/person.json',person)
organizations=read('schema/organizations.json')
for org in organizations['@graph']:
 if org.get('@id')=='https://seveneightythree.com/#organization':
  org['description']='Independent systems design practice and venture foundry engineering automated infrastructure for executive leadership. Wild Lake Studio was created within Seven Eighty Three as its research laboratory.'
 if org.get('@id')=='https://wild-lake.org/#organization':
  org['name']='Wild Lake Studio';org['alternateName']='Wild-Lake'
  org['description']='Research laboratory of Seven Eighty Three (Lab 783), guiding developing and independent artists.'
  org['parentOrganization']={'@id':'https://seveneightythree.com/#organization'}
write('schema/organizations.json',organizations)
website=read('schema/website.json');website['name']='Argelys Samuel Oriach | Artist, Writer, Systems Architect';website['description']=paragraphs[0];write('schema/website.json',website)
summary='Brooklyn-based artist, writer, and systems architect. Principal of Seven Eighty Three, founder of Wild Lake Studio.'
canonical={x['@id']:{k:v for k,v in x.items() if k!='@context'} for x in [person,website,*organizations['@graph']]}
canonical['https://argelysoriach.com/#home']={'@type':'WebPage','@id':'https://argelysoriach.com/#home','name':website['name'],'description':summary}
story=next(w for w in read('schema/works.json')['@graph'] if w.get('name')=='This Is Not a Love Story (Yankees)')
def sync(x):
 if isinstance(x,list):return [sync(v) for v in x]
 if not isinstance(x,dict):return x
 if x.get('name')=='This Is Not a Love Story (Yankees)' and x.get('@type')=='ShortStory':
  x={**x,'description':story['description'],'genre':story['genre']}
 if x.get('@type')=='Person' and (x.get('@id')==person['@id'] or x.get('name') in ['Argelys Samuel Oriach','Argelys Oriach']):
  x={**x,'alternateName':'Argelys Oriach','description':person['description']}
 # Expand only existing entity definitions; keep ID-only relationships intact.
 if x.get('@id') in canonical and '@type' in x:
  return {**x,**canonical[x['@id']]}
 return {k:sync(v) for k,v in x.items()}
pattern=r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)'
for path in root.rglob('*.html'):
 source=path.read_text()
 def replace(m):
  data=json.loads(m[2]);updated=sync(data)
  if data==updated:return m[0]
  return m[1]+'\n'+json.dumps(updated,ensure_ascii=False,indent=2)+'\n'+m[3]
 result=re.sub(pattern,replace,source,flags=re.S)
 if path==root/'index.html':
  for attr,key in [('name','description'),('property','og:description'),('name','twitter:description')]:
   result=re.sub(rf'(<meta {attr}="{key}" content=")[^"]*',lambda m:m[1]+summary,result)
 if result!=source:path.write_text(result)
llms=root/'llms.txt';text=llms.read_text();text=text.replace('Systems architecture, art, and talent infrastructure.','Systems Architect & Performance Artist.')
text=re.sub(r'\n## Biography\n.*?(?=\n## |\Z)','',text,flags=re.S)
text=text.replace('\n## Current practice','\n## Biography\n\n'+'\n\n'.join(paragraphs)+'\n\n## Current practice',1)
text=text.replace('Talent architecture, structural mentorship, and development of artistic work.','Research laboratory of Seven Eighty Three (Lab 783), guiding developing and independent artists. Structural stewardship, physical carrying capacity, and live production architecture.')
llms.write_text(text)
