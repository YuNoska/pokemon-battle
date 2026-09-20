"""Generate one A4 landscape page per team from the complete team records."""
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[1]
font='/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
pdfmetrics.registerFont(TTFont('JP',font))
W,H=landscape(A4)
output=ROOT/'docs/baxcalibur-team-sheets.pdf';output.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(output),pagesize=(W,H));c.setTitle('セグレイブ構築・一枚資料 / 2026-09-20')
data=json.loads((ROOT/'data/baxcalibur-teams-2026-09-20.json').read_text())
def txt(x,y,s,size=10,color='#24384B'):
 c.setFillColor(HexColor(color));c.setFont('JP',size);c.drawString(x,y,s)
def wrap(s,width,size):
 lines=[];line=''
 for ch in s:
  if pdfmetrics.stringWidth(line+ch,'JP',size)>width:lines.append(line);line=ch
  else:line+=ch
 if line:lines.append(line)
 return lines
for t in data:
 c.setFillColor(HexColor('#F3F7FA'));c.rect(0,0,W,H,fill=1,stroke=0)
 txt(24,H-34,t['id']+'  '+t['title'],21,'#102E49')
 txt(24,H-54,'Champions / M-C シングル / 2026-09-20  |  '+t['status'],9)
 txt(24,H-70,'配分順 H=HP / A=攻撃 / B=防御 / C=特攻 / D=特防 / S=素早さ（各32以下・合計66）',8.5)
 margin=24;gap=12;cw=(W-margin*2-gap*2)/3;ch=172;top=H-86
 for i,m in enumerate(t['members']):
  col=i%3;row=i//3;x=margin+col*(cw+gap);y=top-row*(ch+gap)-ch
  c.setFillColor(HexColor('#FFFFFF'));c.setStrokeColor(HexColor('#D8E2E9'));c.roundRect(x,y,cw,ch,7,fill=1,stroke=1)
  sprite=ROOT/'assets/sprites'/f"{m['sprite']}.png"
  if sprite.exists():c.drawImage(str(sprite),x+cw-55,y+ch-53,44,44,mask='auto')
  txt(x+12,y+ch-23,m['name'],11)
  txt(x+12,y+ch-43,m['item'],10,'#237D87')
  txt(x+12,y+ch-61,m['nature'],8.8)
  txt(x+12,y+ch-77,'特性：'+m['ability'],8.6)
  txt(x+12,y+ch-94,'配分：'+'/'.join(map(str,m['points'])),10)
  for j,mv in enumerate(m['moves']):txt(x+12+(j%2)*(cw/2-2),y+ch-113-(j//2)*16,mv,9.3)
  txt(x+12,y+13,m['role'],8.7,'#527184')
 bottom=top-2*ch-gap
 txt(24,bottom-24,t['selection'],12,'#102E49')
 yy=bottom-43
 for s in t['notes']:
  for line in wrap('・'+s,W-48,9):txt(24,yy,line,9);yy-=13
 assert yy>43,(t['id'],yy)
 txt(24,32,'詳細・出典：docs/baxcalibur-teams.md  |  公開例の不足項目は未確認。新案の勝率・確定耐えは未検証。',8)
 txt(24,18,'画像：PokéAPI/sprites（通常姿の識別用。メガの姿ではありません）  |  '+t['id']+' / 3',7.5)
 c.showPage()
c.save()
print(output)
