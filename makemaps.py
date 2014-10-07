import cairosvg
from lxml import etree as ET

# portions of code from
# * http://stackoverflow.com/questions/6589358/convert-svg-to-png-in-python

def sethighlight(e):
    e.attrib["style"] = 'fill:#ff0000;fill-opacity:1;stroke:#000000;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none'

def unsethighlight(e):
    e.attrib["style"] = 'fill:#c1f0f6;fill-opacity:1;stroke:#000000;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none'

roomlist = {"huxley-level-1.svg": ["101", "102", "103", "104", "105", "105a", "106", "106a", "107", "107a", "108", "109", "110", "112", "113", "113a", "114", "115", "117", "119", "119a", "119b", "120", "121", "122", "123", "127", "128", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141a", "142", "144", "145", "147", "148", "160"], 
"huxley-level-2.svg": ["clore", "201", "202", "206", "212", "212b", "214", "215", "217", "218", "219", "220", "220a", "221", "224", "225", "226", "227", "228"], 
"huxley-level-3.svg": ["301", "302", "303", "304", "304a", "305", "305a", "306", "307", "308", "309", "310", "311", "312", "315", "316", "316a", "317", "339", "340", "341", "342", "344", "344a", "344b", "345", "346", "347", "348", "351", "353", "354", "355", "356", "357", "358", "359", "360", "361", "370", "371", "372", "373", "374", "375", "376", "377", "378", "379", "380", "390", "393"], 
"huxley-level-4.svg": ["403", "406", "406a", "407", "408", "410", "418", "420", "421", "422", "423", "424", "425", "426", "427", "428", "429", "431", "432", "433", "434", "435", "436", "436a", "436b", "440", "441", "442", "443", "444", "444a", "446", "447", "448", "449", "450", "452", "453", "454", "455"], 
"huxley-level-5.svg": ["502", "503", "504", "505", "507", "508", "509", "510", "511", "512", "512a", "512b", "513", "514", "515", "517", "517a", "519", "520", "521", "522", "523", "524", "525", "526", "527", "528", "529", "530", "531", "542", "543", "544", "545", "546", "547", "548", "551", "552", "553", "554", "555", "556", "557", "559", "566", "568", "569", "571", "572", "572a", "573", "574", "575", "583", "583a"]}

# create index page
html = ET.Element("html")
head = ET.SubElement(html, "head")
title = ET.SubElement(head, "title")
styles = ET.SubElement(head, "link")
styles.set("rel","stylesheet")
styles.set("type","text/css")
styles.set("href","css/style.css")
body = ET.SubElement(html, "body")
div = ET.SubElement(body, "div")
h1 = ET.SubElement(div,"h1")
h1.text = title.text = "Huxley building map index"
pintro = ET.SubElement(div,"p")
pintro.text = "Select the room to see it highlighted on the relevant floor."
list = ET.SubElement(div,"ul")
list.set("id","ten")
for floorfile in sorted(roomlist):
    for roomid in roomlist[floorfile]:
        room = ET.SubElement(list,"li")
        aroom = ET.SubElement(room,"a")
        aroom.set("href","huxley-" + roomid + ".html")
        aroom.text = roomid

fout = open("output/index.html","w")
fout.write(ET.tostring(html,pretty_print=True))
fout.close()

for floorfile in roomlist:
    # load floor
    tree = ET.parse(floorfile)
    root = tree.getroot()

    for roomid in roomlist[floorfile]:
        # search rect elements
        elts = root.findall('*/*[@id="' + roomid + '"]')
        if len(elts) > 0:
            # highlight room
            sethighlight(elts[0])
            svg_code = ET.tostring(root)

            # save png
            fout = open("output/huxley-" + roomid + ".png","w")
            cairosvg.svg2png(bytestring=svg_code,write_to=fout)
            fout.close()

            # remove highlight
            unsethighlight(elts[0])
            
            # create html page
            html = ET.Element("html")
            head = ET.SubElement(html, "head")
            title = ET.SubElement(head, "title")
            styles = ET.SubElement(head, "link")
            styles.set("rel","stylesheet")
            styles.set("type","text/css")
            styles.set("href","css/style.css")
            body = ET.SubElement(html, "body")
            div = ET.SubElement(body, "div")
            h1 = ET.SubElement(div,"h1")
            h1.text = title.text = "Huxley building: " + roomid
            img = ET.SubElement(div,"img")
            img.set("src","huxley-" + roomid + ".png")
            pindex = ET.SubElement(div,"p")
            aindex = ET.SubElement(pindex,"a")
            aindex.set("href","index.html")
            aindex.text = "Return to index"

            # save html page
            fout = open("output/huxley-" + roomid + ".html","w")
            fout.write(ET.tostring(html,pretty_print=True))
            fout.close()
