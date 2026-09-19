"""Render verified species base stats; no network access required."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/base-stats-m6-2026-09-19.json').read_text())
FONT='/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'
BOLD='/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'
def font(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)
colors=['#1C8194','#C06832','#B79018','#6D65B9','#41956F','#AD5380']
# One shared zero-based scale for all six metrics and both figures.
ceiling=((max(max(r['stats']) for r in data['rows'])+19)//20)*20

def label(r):
 if r['form']=='通常':return r['name']
 if r['form'] in ['オス','シールド','ブレード']:return r['name']+'（'+r['form']+'）'
 return 'メガ'+r['name']+r['form'].replace('メガ','')

def render(group,title,file):
 rows=[r for r in data['rows'] if r['group']==group]
 w=1540;row_h=48;top=236;h=top+len(rows)*row_h+116
 im=Image.new('RGB',(w,h),'#FAFBFD');d=ImageDraw.Draw(im)
 d.text((32,24),title,font=font(32,True),fill='#172D41')
 d.text((32,78),'M-6 シングル｜使用率上位20種＋ウルガモス｜順位更新：2026/9/19 20:42',font=font(18),fill='#425A6C')
 note='通常姿の種族値。ギルガルドはシールド、イダイトウはオス。' if group=='base' else '順位は元の種族の使用率順位。メガ形態ごとの使用率ではありません。'
 d.text((32,111),note+' 画像は通常姿の識別用。',font=font(18),fill='#425A6C')
 d.text((32,177),'使用率順位 / ポケモン',font=font(19,True),fill='#172D41')
 x0=398;cw=163;barw=138
 for j,name in enumerate(data['stat_order']):
  x=x0+j*cw
  d.text((x,163),name,font=font(21,True),fill=colors[j])
  for tick in [0,90,180]:
   tx=x+tick/ceiling*barw
   d.text((tx,198),str(tick),font=font(13),fill='#65798A',anchor='lt' if tick==0 else ('rt' if tick==180 else 'mt'))
 d.text((1415,178),'合計',font=font(20,True),fill='#172D41')
 for i,r in enumerate(rows):
  y=top+i*row_h
  if i%2==0:d.rectangle((24,y-4,w-25,y+row_h-5),fill='#EFF3F7')
  d.text((32,y+5),str(r['rank']).rjust(2),font=font(19,True),fill='#526D81')
  sprite=ROOT/'assets/sprites'/f"{r['slug']}.png"
  if sprite.exists():
   sp=Image.open(sprite).convert('RGBA');sp.thumbnail((45,45));im.paste(sp,(69,y-3),sp)
  d.text((116,y+5),label(r),font=font(18,True),fill='#172D41')
  for j,v in enumerate(r['stats']):
   x=x0+j*cw
   d.line((x,y+28,x+barw,y+28),fill='#D6DFE6',width=1)
   d.rectangle((x,y+20,x+barw*v/ceiling,y+30),fill=colors[j])
   d.text((x+barw*v/ceiling,y-2),str(v),font=font(16,True),fill='#172D41',anchor='mt')
  d.text((1415,y+5),str(r['total']),font=font(20,True),fill='#172D41')
 y=top+len(rows)*row_h+20
 d.text((32,y),'全能力共通：0〜180。数値は種族値（実数値・勝率・総合的な強さではありません）。',font=font(18),fill='#425A6C')
 d.text((32,y+31),'順位：バトルデータベース Champions ／ 種族値：Serebii Champions Pokédex ／ 2026-09-19確認',font=font(16),fill='#425A6C')
 im.save(ROOT/'assets/charts'/file)
 return rows
base=render('base','使用率上位のポケモン ─ 6能力の種族値','base-stats-m6.png')
alt=render('alternate','メガシンカ・フォルム変化後の種族値','base-stats-m6-forms.png')
lines=['# 使用率上位の種族値グラフ','','**M-6（M-C）シングル／2026-09-19確認**','','[トップ](../README.md) ｜ [元データ](../data/base-stats-m6-2026-09-19.json)','','## 通常姿：上位20種＋ウルガモス','','![上位20種とウルガモスの種族値グラフ](../assets/charts/base-stats-m6.png)','','## メガ・フォルム変化後','','![メガとフォルム変化後の種族値グラフ](../assets/charts/base-stats-m6-forms.png)','','## 読み方','','- 全ての棒は同じ0〜180の尺度。各能力の棒の長さと数値を比べます。合計は右端。','- 順位は[バトルデータベースのM-6シングル](https://champs.pokedb.tokyo/pokemon/list?season=6&rule=0)、サイト表示の更新日時は2026/9/19 20:42。種族単位の順位を形態にも添えており、メガ形態別の順位ではありません。','- ウルガモスは上位20種外ですが、ユーザーの対策対象として28位を追加。以前の調査時からエースバーンは18→17位、ウルガモスは27→28位へ更新。短時間の順位差だけで流行の増減は断定しません。','- 種族値は種族・姿ごとの基礎数値です。性格・能力ポイント・レベル・持ち物・特性・技によって実戦の能力は変わります。素早さ種族値だけでスカーフや竜舞後の先後は決まりません。','- 防御と特防だけで耐久は決まりません。HP・タイプ相性・特性も含めて判断します。合計が高いほど必ず強いわけではありません。','- メガ後の値は別図。ギルガルドのシールド／ブレード、イダイトウのオスを明記し、異なる姿を混同しません。','','## 今の構築検討で注目したい点','','- エースバーン：攻撃116・素早さ119。物理攻撃と速度が特徴。','- ウルガモス：特攻135・特防105・防御65。ただし防御育成や蝶舞、回復で実戦の硬さは変わります。','- メガルカリオZ：特攻164・素早さ151。通常ルカリオの値を使って速度比較しないこと。','- メガグソクムシャ：防御175・特防120・素早さ40。高い耐久数値でも炎4倍という相性は別に考えます。','','## 数値表と出典','','種族値は各リンク先のChampions版「Base Stats」から確認。画像の通常姿スプライトは[画像出典](../assets/CREDITS.md)参照。全33形態の合計と6能力を照合済み。','','| 順位 | ポケモン・姿 | HP | 攻撃 | 防御 | 特攻 | 特防 | 素早さ | 合計 | 出典 |','| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
for r in base+alt:lines.append('| '+' | '.join([str(r['rank']),label(r),*map(str,r['stats']),str(r['total']),f"[図鑑]({r['source']})"])+' |')
(ROOT/'docs/base-stats.md').write_text('\n'.join(lines)+'\n')
print(len(base),len(alt),ceiling)
