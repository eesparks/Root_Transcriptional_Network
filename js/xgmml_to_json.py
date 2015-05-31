#pip install beautifulsoup4
### http://cytoscape.github.io/cytoscape.js/#notation/elements-json
### https://github.com/bendtherules/GSOC_13/blob/master/nnf_and_sif_to_json_py/result.json
from bs4 import BeautifulSoup
import json
import random
from collections import OrderedDict



def get_nstyle(xline):
    color_dic = { "#33ff00" : "KNA7 Root Coexpressed",
            "#0033ff" : "Cellulose Biosynthesis",
            "#33ccff" : "Cellulose Coexpressed",
            "#ff00cc" : "HD-ZIP III",
            "#ff0000" : "Lignin",
            "#9900ff" : "Secondary Cell Wall TF",
            "#ff9900" : "Xylan",
            "#cc99ff" : "None",
            "#ffff00" : "Xylan",
            "#0066ff" : "Secondary Cell Wall TF",
            "#00ccff" : "IDONTKNOW",
            "#ffcc00": "IDONTKNOW",
            "#ff0033" : "IDONTKNOW"
            }

    style = xline.find_all("graphics")
    faveColor = style[0].get("fill")
    faveShape = style[0].get("type")
    width = style[0].get("w")
    h =  style[0].get("h")
    x = style[0].get("x")
    y = style[0].get("y") 
    name = get_att(style,"NODE_LABEL")
    try:
	return float(x),float(y), faveColor, "notsure", faveShape.lower(), float(width), float(h), name
    except TypeError:
	return x,y,faveColor,"notsure", faveShape.lower(), float(width), float(h)


def get_att(style, att_name):
    d = {"T": "tee", "ARROW": "triangle", "NONE": "none","EQUAL_DASH": "dashed", "round_rectangle": "roundrectangle"}
    for att in style[0].find_all("att"):
        if att_name == att.get("name"):
            #print att.get("value")
            try:
                return d[att.get("value")]
            except KeyError:
                return att.get("value")



def get_estyle(xline):
    style = xline.find_all("graphics")
    faveColor = style[0].get("fill")
    targetarrow = get_att(style, "EDGE_TARGET_ARROW_SHAPE")
    sourcearrow = get_att(style, "EDGE_SOURCE_ARROW_SHAPE")
    linetype = get_att(style, "EDGE_LINE_TYPE")
    return faveColor, targetarrow, sourcearrow, linetype


def get_size(xline):
    atts = xline.find_all("att")
    size_line = atts[1].get("value")
    return size_line


class NodeLine(object):
    _slots_ = ("id","name","x","y","group","faveColor", "type")

    def __init__(self, xline):
        shapes = {"round_rectangle":"roundrectangle", "parallelogram": "diamond","ellipse":"ellipse","vee":"vee"}
        self.group = "nodes"
        self.cid = xline.get("id")
        #self.name = xline.get("label")
        self.x, self.y, self.faveColor, self.node_type, self.faveShape, self.w, self.h, self.name = get_nstyle(xline)
        shape = shapes[self.faveShape]
        print shape
        self.nodeline = {"data" : {"id": self.cid, "name": self.name, "faveColor": self.faveColor, "node_type": self.node_type,"faveShape": shape, "w": self.w, "h": self.h},  "position": {"x": self.x, "y": self.y}}
          

class EdgeLine(object):
    _slots_ = ("name","target","source","group","faveColor","classes","size")

    def __init__(self, xline):
        self.group = "edge"
        self.name = xline.get("label")
        self.source = xline.get("source")
        self.target = xline.get("target")
        self.faveColor, self.targetarrow, self.sourcearrow, self.linetype = get_estyle(xline)
        self.size = get_size(xline)
        self.edgeline = { "data": {"lineStyle": self.linetype.lower() ,"target": self.target ,"id": self.name, "source": self.source, "line-width": self.size,  "targetArrowShape": self.targetarrow.lower(), "sourceArrowShape" : self.sourcearrow.lower() , "faveColor" : self.faveColor , "fesign": 7, "naclsign": 7}}


class Element(object):

    def __init__(self,filename):
        self.filename = filename
        self.nodes = []
        self.edges = []

        fh = open(filename)
        xgmml = fh.read()
        soup = BeautifulSoup(xgmml)
        for nline in soup.find_all("node"):
            node = NodeLine(nline)
            self.nodes.append(node)

        for eline in soup.find_all("edge"):
            edge = EdgeLine(eline)
            self.edges.append(edge)


    def get_dic(self):
        n_dic = dict((n.cid, n.nodeline) for i,n in enumerate(self.nodes))
        e_dic = dict((e.name, e.edgeline) for i,e in enumerate(self.edges))
        return dict(n_dic.items() + e_dic.items())


def stress(key,stress,stress_dic):
        try:
           cytoid = key['data']['id']
           match_id = stress_dic[cytoid]
           key['data'][stress] = 1
           if '{0}sign'.format(stress) in list(match_id['data'].keys()):
               key['data']['{0}sign'.format(stress)] = int(match_id['data']['{0}sign'.format(stress)])
               return key
           else: return key
        except KeyError:
            key['data'][stress] = 0
            return key

def main(xgmml_file, outfh):
    outfile = open(outfh,"wb")
    cyto = Element(xgmml_file)
    nodelines = []
    edgelines = []
    cyto_d = cyto.get_dic()
    #fe_cyto = Element(fe_file)
    #fe_d = fe_cyto.get_dic()
    #nacl_cyto = Element(nacl_file)
    #nacl_d = nacl_cyto.get_dic()

    for cytoid in cyto_d:
        cyto_value = cyto_d[cytoid]
        if "position" in cyto_value.keys():
            nodelines.append(cyto_value)
        else:
            edgelines.append(cyto_value)

    jsonformat = {"nodes": nodelines, "edges": edgelines}
    jsonformated =  json.dumps(jsonformat,indent=4)
    outfile.write(jsonformated)

#main("/Users/gturco/Desktop/MallorieData_New/CytoscapeSession-2013_07_01-17_20//Sheet1.xgmml", "../Hazen_network.json")
main("/Users/gturco/Documents/code/Brady/esparks/data/xml/sparks_full_network_clusters.xml", "../clusters.json")
main("/Users/gturco/Documents/code/Brady/esparks/data/xml/full_network.xml", "../full_network.json")
main("/Users/gturco/Documents/code/Brady/esparks/data/xml/higher_order_sub.xml", "../higher_order_sub.json")
main("/Users/gturco/Documents/code/Brady/esparks/data/xml/light_network.xml", "../light_network.json")
main("/Users/gturco/Documents/code/Brady/esparks/data/xml/sub_network1.xml", "../sub_network1.json")
main("/Users/gturco/Documents/code/Brady/esparks/data/xml/sub_network2.xml", "../sub_network2.json")
main("/Users/gturco/Documents/code/Brady/esparks/data/xml/sub_network3.xml", "../sub_network3.json")
main("/Users/gturco/Documents/code/Brady/esparks/data/xml/sub_network4.xml", "../sub_network4.json")
main("/Users/gturco/Documents/code/Brady/esparks/data/xml/tf_motifs.xml", "../tf_motifs.json")




