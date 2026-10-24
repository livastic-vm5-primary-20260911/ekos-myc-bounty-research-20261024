"""Offline confirmation that quoted public-source values, exclusions, and time agree."""
import json, pathlib, datetime
from decimal import Decimal
root=pathlib.Path(__file__).resolve().parent
snap=json.loads((root/'research_snapshot.json').read_text())
rug=json.loads((root/'rugcheck_public_raw.json').read_text())
dex=json.loads((root/'dex_market_raw.json').read_text())
myc=json.loads((root/'mycelium_allocation_public_raw.json').read_text())
mint=snap['mint']
assert rug['mint']==mint and dex[0]['baseToken']['address']==mint
m=dex[0];assert m['marketCap']==snap['marketCapDexUSd']
assert m['volume']['h24']==snap['volume24DexUsd']
assert m['liquidity']['usd']==snap['liquidityDexUsd']
assert rug['token']['mintAuthority'] is None and rug['token']['freezeAuthority'] is None
pool=rug['markets'][0]
assert pool['pubkey']==snap['pool']
vault=pool['liquidityA']
assert vault in snap['excludedTokenAccounts']
top=[h for h in rug['topHolders'] if h['address'] not in snap['excludedTokenAccounts']][:10]
assert len(top)==10
calculated=sum(Decimal(str(h['pct'])) for h in top)
assert abs(calculated-Decimal(snap['topTenExcludingVerifiedLPPercentageOfTotalSupply']))<Decimal('0.00000000001')
assert pool['lp']['lpLockedPct']==100
assert not any(a.get('symbol')=='EKOS' for a in myc['allocations'])
created=datetime.datetime.fromtimestamp(m['pairCreatedAt']/1000,datetime.timezone.utc)
observed=datetime.datetime.fromisoformat(snap['timestampUTC'])
age=(observed-created).total_seconds()/86400
assert age>=60 and abs(age-snap['ageDays'])<0.01
assert m['marketCap']<1e6 and m['volume']['h24']>=1e4 and m['liquidity']['usd']>=5e4
print('PASS 13 first-party crosschecks; top10 excl LP {:.4f}%, age {:.2f} days, source snapshot {}'.format(calculated,age,observed.isoformat()))
