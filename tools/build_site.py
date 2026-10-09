from pathlib import Path
from copy import deepcopy
import json,re
from html import escape as h
from lxml import html as H,etree
BASE=Path(__file__).resolve().parents[1]
D=json.loads((BASE/'data/profile.json').read_text());SITE=BASE
T=(BASE/'tools/academic-template.txt').read_text()
def fragment(s):return H.fragment_fromstring(s)
def inner(el,s):
 for c in list(el):el.remove(c)
 el.text=None
 for c in H.fragments_fromstring(s):
  if isinstance(c,str):el.text=(el.text or '')+c
  else:el.append(c)
def one(root,s):return root.xpath(s)[0]
def section(id,title,content):return fragment(f'<section id="{id}" class="home-section wg-markdown"><div class="home-section-bg"></div><div class="container"><div class="row"><div class="section-heading col-12 col-lg-4 mb-3 mb-lg-0 d-flex flex-column align-items-center align-items-lg-start"><h1 class="mb-0">{title}</h1></div><div class="col-12 col-lg-8">{content}</div></div></div></section>')
for lang in ['en','zh']:
 zh=lang=='zh';url=D['website']+('zh/' if zh else '');x=H.fromstring(T);x.set('lang','zh-CN' if zh else 'en')
 title='胡书 | 复旦大学' if zh else 'Shu Hu | Fudan University'
 one(x,'//title').text=title
 for el in x.xpath('//meta[@name="description"]|//meta[@property="og:description"]|//meta[@name="twitter:description"]'):el.set('content',D['bio_'+lang])
 for el in x.xpath('//meta[@property="og:title"]|//meta[@name="twitter:title"]'):el.set('content',title)
 for el in x.xpath('//link[@rel="canonical"]'):el.set('href',url)
 for el in x.xpath('//meta[@property="og:url"]'):el.set('content',url)
 for el in x.xpath('//script[@type="application/ld+json"]'):el.text=json.dumps({'@context':'https://schema.org','@type':'Person','name':D['name_'+lang],'url':url,'email':D['email'],'affiliation':{'@type':'Organization','name':'Fudan University'},'sameAs':[D['scholar'],D['researchgate'],D['orcid'],D['github']]})
 for el in x.xpath('//*[@class="navbar-brand"]'):el.text=D['name_'+lang];el.set('href','/zh/' if zh else '/')
 nav=one(x,'//*[@id="navbar-content"]/ul')
 labels=['首页','论文','技能','经历','联系'] if zh else ['Home','Publications','Skills','Experience','Contact']
 inner(nav,''.join(f'<li class="nav-item"><a class="nav-link" href="#{id}" data-target="#{id}"><span>{lab}</span></a></li>' for id,lab in zip(['about','publications','skills','experience','contact'],labels)))
 icons=one(x,'//ul[contains(@class,"nav-icons")]')
 icons.insert(0,fragment(f'<li class="nav-item"><a class="nav-link" href="{"/" if zh else "/zh/"}" lang="{"en" if zh else "zh-CN"}" aria-label="Switch language">{"EN" if zh else "中文"}</a></li>'))
 # Legacy full-site search points to obsolete template entries; current page navigation is the primary path.
 for el in x.xpath('//li[a[contains(@class,"js-search")]]'):el.getparent().remove(el)
 prof=one(x,'//*[@id="profile"]')
 inner(one(prof,'.//div[@class="portrait-title"]'),f'<h2>{D["name_"+lang]}</h2><h3>{"微生物系博士研究生" if zh else "PhD Student in Microbiology"}</h3><h3><a href="https://www.fudan.edu.cn/" target="_blank" rel="noopener"><span>{"复旦大学" if zh else "Fudan University"}</span></a></h3>')
 socials=[('mailto:'+D['email'],'fas fa-envelope','Email'),(D['scholar'],'fas fa-graduation-cap','Google Scholar'),(D['researchgate'],'fab fa-researchgate','ResearchGate'),(D['orcid'],'fab fa-orcid','ORCID'),(D['github'],'fab fa-github','GitHub')]
 soc=one(prof,'.//ul[contains(@class,"network-icon")]');soc.attrib.pop('aria-hidden',None)
 inner(soc,''.join(f'<li><a href="{h(u)}" target="_blank" rel="noopener" aria-label="{label}"><i class="{ico} big-icon" aria-hidden="true"></i></a></li>' for u,ico,label in socials))
 about=one(x,'//*[@id="about"]');one(about,'.//h1').text='个人简介' if zh else 'Biography'
 bio='<p>'+h(D['bio_'+lang])+'</p>'
 bio+='<p class="cv-downloads">'+('简历下载：' if zh else 'Curriculum vitae: ')
 for code,label in [('EN','English'),('ZH','中文')]:
  bio+=f'<a href="/uploads/Shu_Hu_CV_{code}.pdf" target="_blank" rel="noopener">{label} PDF</a> · <a href="/uploads/Shu_Hu_CV_{code}.docx">Word</a> &nbsp; '
 bio+='</p>'
 inner(one(about,'.//div[@class="article-style"]'),bio)
 subs=about.xpath('.//div[@class="section-subheading"]');subs[0].text='研究兴趣' if zh else 'Interests';subs[1].text='教育背景' if zh else 'Education'
 interests=['病毒进化','基因组流行病学','计算生物学'] if zh else ['Viral evolution','Genomic epidemiology','Computational biology']
 inner(one(about,'.//ul[contains(@class,"ul-interests")]'),''.join(f'<li><i class="fa-li fa-solid fa-book-open"></i>{v}</li>' for v in interests))
 edu=''
 for e in D['education']:
  edu+=f'<li><i class="fa-li fa-solid fa-graduation-cap"></i><div class="description"><p class="course">{h(e["degree_"+lang])}</p><p class="institution">{h(e["institution_"+lang])}<br>{h(e["date_"+lang])}</p></div></li>'
 inner(one(about,'.//ul[contains(@class,"ul-edu")]'),edu)
 pubs='<ol class="academic-publications">'
 for p in D['publications']:
  authors=h(p['authors'].rstrip('.')).replace('Hu S','<strong>Hu S</strong>')
  pubs+=f'<li><div>{authors}.</div><div><a href="https://doi.org/{p["doi"]}" target="_blank" rel="noopener">{h(p["title"])}.</a></div><div><em>{h(p["venue"])}</em>. {p["year"]}{"; "+h(p["details"]) if p["details"] else ""}.</div><a class="pub-doi" href="https://doi.org/{p["doi"]}" target="_blank" rel="noopener">doi: {p["doi"]}</a></li>'
 pubs+='</ol>'
 about.addnext(section('publications','论文成果' if zh else 'Publications',pubs))
 skills=one(x,'//*[@id="skills"]')
 if zh:
  for e in skills.xpath('.//*'):
   if e.text and e.text.strip() in {'Skills':'技能与兴趣','Technical':'专业技能','Hobbies':'个人兴趣','Hiking':'徒步','Cats':'猫','Photography':'摄影','travel':'旅行','music':'音乐','docker':'Docker'}:e.text={'Skills':'技能与兴趣','Technical':'专业技能','Hobbies':'个人兴趣','Hiking':'徒步','Cats':'猫','Photography':'摄影','travel':'旅行','music':'音乐','docker':'Docker'}[e.text.strip()]
 exp=one(x,'//*[@id="experience"]');one(exp,'.//h1').text='研究与工作经历' if zh else 'Experience'
 container=one(exp,'.//div[@class="col-12 col-lg-8"]');examples=container.xpath('./div[contains(@class,"experience")]');template=deepcopy(examples[0])
 inner(container,'')
 phd={'institution_en':'Fudan University','institution_zh':'复旦大学','role_en':'PhD Student','role_zh':'博士研究生','date_en':'Sep 2025 – present · Expected Jun 2029','date_zh':'2025.09—至今 · 预计2029.06毕业','bullets_en':['Department of Microbiology, School of Life Sciences.','Research interests: viral evolution, genomic epidemiology and computational biology.'],'bullets_zh':['生命科学学院微生物系。','研究兴趣：病毒进化、基因组流行病学与计算生物学。']}
 ed={'institution_en':'The University of Edinburgh','institution_zh':'爱丁堡大学','role_en':'MSc Research','role_zh':'硕士阶段研究','date_en':'Feb – Sep 2022','date_zh':'2022.02—2022.09','bullets_en':[D['projects'][3]['text_en']],'bullets_zh':[D['projects'][3]['text_zh']]}
 for j,(e,logo,link) in enumerate([(phd,None,'https://www.fudan.edu.cn/'),(D['experience'][0],'gene','https://www.rightongene.com/'),(D['experience'][1],'hku','https://www.hku.hk/'),(ed,'uoe','https://www.ed.ac.uk/'),(D['experience'][2],'wo','https://www.scwwt.com/')]):
  card=deepcopy(template);one(card,'.//div[contains(@class,"exp-title")]').text=e['role_'+lang]
  inner(one(card,'.//div[contains(@class,"exp-company")]'),f'<a href="{link}" target="_blank" rel="noopener">{h(e["institution_"+lang])}</a>')
  inner(one(card,'.//div[contains(@class,"exp-meta")]'),h(e['date_'+lang]))
  ico=one(card,'.//div[@class="mr-2 mb-2"]')
  inner(ico,f'<img src="/media/icons/brands/{logo}.svg" width="56" height="56" alt="{h(e["institution_"+lang])}" loading="lazy">' if logo else '<span class="fas fa-graduation-cap fa-2x" style="width:56px" aria-hidden="true"></span>')
  inner(one(card,'.//div[@class="card-text"]'),'<ul>'+''.join('<li>'+h(b)+'</li>' for b in e['bullets_'+lang])+'</ul>')
  one(card,'.//span[contains(@class,"badge")]').set('class','badge badge-pill border'+(' exp-fill' if j==0 else ''))
  container.append(card)
 projects=''.join(f'<div class="mb-4"><h3>{h(p["name_"+lang])}</h3><p>{h(p["text_"+lang])}</p><p><a href="{h(p["url"])}" target="_blank" rel="noopener">{h(p["link_"+lang])} <i class="fas fa-external-link-alt" aria-hidden="true"></i></a></p></div>' for p in D['projects'][:4])
 exp.addnext(section('research','研究项目' if zh else 'Research Projects',projects))
 if zh:
  for e in x.xpath('//*[@id="section-markdown"]//h1'):e.text='珍藏时刻'
 contact=one(x,'//*[@id="contact"]');one(contact,'.//h1').text='联系方式' if zh else 'Contact'
 inner(one(contact,'.//div[@class="col-12 col-lg-8"]'),f'<ul class="fa-ul"><li><i class="fa-li fas fa-envelope fa-2x" aria-hidden="true"></i><span id="person-email"><a href="mailto:{D["email"]}">{D["email"]}</a></span></li><li><i class="fa-li fas fa-university fa-2x" aria-hidden="true"></i><span>{"复旦大学生命科学学院微生物系<br>中国上海" if zh else "Department of Microbiology, School of Life Sciences<br>Fudan University, Shanghai, China"}</span></li></ul>')
 foot=one(x,'//footer');inner(foot,f'<p class="powered-by">© 2026 {D["name_"+lang]} · <a href="{D["github"]}">GitHub</a></p><p class="powered-by">Published with <a href="https://hugoblox.com/" target="_blank" rel="noopener">Hugo Blox Builder</a></p>')
 for s in x.xpath('//script[contains(@src,"wowchemy-map")] | //script[contains(@src,"leaflet")]'):s.getparent().remove(s)
 head=one(x,'//head');head.append(fragment('<style>.academic-publications{padding-left:1.25rem}.academic-publications li{padding-left:.2rem;margin-bottom:1.7rem}.pub-doi{font-size:.85em;overflow-wrap:anywhere}.cv-downloads{font-size:.9em}.network-icon{flex-wrap:wrap}#profile .network-icon .big-icon{font-size:1.7rem}html[lang="zh-CN"] body{font-family:Roboto,"PingFang SC","Microsoft YaHei",sans-serif}html[lang="zh-CN"] h1,html[lang="zh-CN"] h2,html[lang="zh-CN"] h3{font-family:Montserrat,"PingFang SC","Microsoft YaHei",sans-serif}@media(max-width:575px){.academic-publications{padding-left:1rem}.home-section{padding:55px 0}.pub-doi{word-break:break-all}}@media(min-width:992px){#about{min-height:calc(100vh - 70px)}}</style>'))
 for l in ['en','zh-CN','x-default']:
  head.append(fragment(f'<link rel="alternate" hreflang="{l}" href="{D["website"]+("zh/" if l=="zh-CN" else "")}">'))
 result=H.tostring(x,encoding='unicode',doctype='<!DOCTYPE html>').replace('https://example.com/',D['website'])
 out=SITE/('zh/index.html' if zh else 'index.html');out.parent.mkdir(exist_ok=True,parents=True);out.write_text(re.sub(r'\n{3,}', '\n\n', '\n'.join(line.rstrip() for line in result.splitlines())).strip()+'\n')
print('Restored original Academic layout and generated English / Chinese homepages.')
