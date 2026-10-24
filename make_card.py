#!/usr/bin/env python3
"""One original fact-only screening graphic. No wallet/network mutation other than public logo GETs."""
import io,json,hashlib,datetime
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import requests
ROOT=Path(__file__).resolve().parent
snap=json.loads((ROOT/'research_snapshot.json').read_text())
LOGOS={
 'EKOS': 'https://raw.githubusercontent.com/alexeyban/EKOS/main/web/ui/public/token_logo_E_200.png',
 'MYC': 'https://www.myceliumfinance.com/brand/myc_logo.png'
}
def get_logo(name,url):
 p=ROOT/(name.lower()+'_official_logo.png')
 if not p.exists():
  r=requests.get(url,timeout=15,headers={'User-Agent':'VM5-OriginalResearch/1.0'});r.raise_for_status()
  test=Image.open(io.BytesIO(r.content));test.verify()
  p.write_bytes(r.content);p.chmod(0o600)
 return Image.open(p).convert('RGBA').copy(),p
images={n:get_logo(n,u) for n,u in LOGOS.items()}
W,H=1600,900
c=Image.new('RGB',(W,H),'#0e182a')
d=ImageDraw.Draw(c)
def F(n,bold=False):
 return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',n)
def rect(xy,fill,stroke=None,r=20,w=2):
 d.rounded_rectangle(xy,radius=r,fill=fill,outline=stroke,width=w)
d.rectangle((0,0,W,14),fill='#e9d5aa')
for y in range(14,H,51):
 d.line((W-350,y,W-2,y),fill='#25314a',width=1)
d.text((84,64),'SOURCE-CHECKED SOLANA RESEARCH',font=F(22,True),fill='#e9d5aa')
d.text((84,103),'ONE QUALIFYING CANDIDATE',font=F(58,True),fill='#f5f6fa')
d.text((86,183),'No partnership. No token-purchase recommendation.',font=F(24),fill='#b9c8d9')
rect((72,250,760,550),'#172840','#3a5268',25)
rect((798,250,1528,550),'#172840','#3a5268',25)
def logo_box(name,x,y):
 im,p=images[name]; im.thumbnail((183,183),Image.Resampling.LANCZOS)
 if im.width>0:
  # Keep original alpha; white tile ensures projects' transparent logos remain legible.
  back=Image.new('RGBA',(208,208),(246,248,252,255))
  back.alpha_composite(im,((208-im.width)//2,(208-im.height)//2))
  c.paste(back.convert('RGB'),(x,y))
  d.rounded_rectangle((x-2,y-2,x+210,y+210),radius=12,outline='#e9d5aa',width=3)
logo_box('EKOS',114,291)
logo_box('MYC',848,291)
d.text((353,322),'EKOS',font=F(56,True),fill='#faf2d7')
d.text((356,398),'$EKOS',font=F(27,True),fill='#e1e6f2')
d.text((356,450),'Open-source AI',font=F(23),fill='#cdd9e6')
d.text((356,483),'knowledge compiler',font=F(23),fill='#cdd9e6')
d.text((1093,321),'MYCELIUM',font=F(39,True),fill='#faf2d7')
d.text((1095,388),'$MYC',font=F(29,True),fill='#e1e6f2')
d.text((1095,437),'Research context only',font=F(22),fill='#cdd9e6')
d.text((1095,478),'NOT a collaboration',font=F(23,True),fill='#f2ae91')
metrics=[
 ('DEX CAP',f"${snap['marketCapDexUSd']/1000:,.0f}k"),
 ('24H VOLUME',f"${snap['volume24DexUsd']/1000:,.0f}k"),
 ('POOL LIQUIDITY',f"${snap['liquidityDexUsd']/1000:,.1f}k"),
 ('TRADING AGE',f"{snap['ageDays']:.1f} days")]
for i,(title,value) in enumerate(metrics):
 x=72+i*369
 rect((x,592,x+352,727),'#26364b',r=17)
 d.text((x+19,608),title,font=F(21,True),fill='#bcc9d9')
 d.text((x+19,650),value,font=F(43,True),fill='#ffffff')
d.text((77,761),f"TOP 10 TOKEN ACCOUNTS (excl. verified LP): {float(snap['topTenExcludingVerifiedLPPercentageOfTotalSupply']):.2f}%  |  MINT / FREEZE: REVOKED",font=F(23,True),fill='#e9d5aa')
d.text((77,808),"Snapshot 24 Oct 2026 01:35 UTC  •  market data: DexScreener  •  holders / LP: Rugcheck",font=F(19),fill='#a9bacf')
d.text((77,842),"Sources and caveats in companion article  •  no sponsor endorsement, audit or guarantee",font=F(18),fill='#a9bacf')
out=ROOT/'ekos_myc_research_original_20261024.png'
c.save(out,format='PNG',optimize=True);out.chmod(0o600)
manifest={'image':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'size':list(c.size),
 'originalArtwork':'Programmatically composed layout; issuer/official logos incorporated unaltered',
 'logoSources':{k:{'url':v,'sha256':hashlib.sha256(images[k][1].read_bytes()).hexdigest()} for k,v in LOGOS.items()},
 'snapshotUTC':snap['timestampUTC'],'marketSource':snap['sourceLinks']['dex'],'holderSource':snap['sourceLinks']['rugcheck'],
 'noAffiliationOrPromise':'not a Mycelium partnership, allocation, audit or investment recommendation'}
(ROOT/'image_source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'image':str(out),'bytes':out.stat().st_size,'sha256':manifest['sha256'],'logos':[(k,str(images[k][0].size)) for k in images]},ensure_ascii=False))
