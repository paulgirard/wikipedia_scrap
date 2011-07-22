# coding=utf-8
import MySQLdb.cursors
import networkx as nx
import pprint
import json
import csv
from datetime import datetime,timedelta

conn1 = MySQLdb.connect (host = "localhost",
						user='controversy_user',
						passwd='controversy_pass',
						db='wikipediaControversies',
						cursorclass = MySQLdb.cursors.SSCursor)

select_cursor = conn1.cursor ()
pp = pprint.PrettyPrinter(indent=4)	
		
################# PARAMETERS ###############

articles={}
select_cursor.execute("SELECT pageid,language from article WHERE pageid!=0")
for article in select_cursor.fetchall() :
	articles[article[0]]={"pageid":article[0],"language":article[1]}


pp.pprint(articles)
#load csv
templates_references={}
for agg_template in ["protected","bias","splitting","dispute"] :
	csv_dict=csv.DictReader(open(agg_template+".csv"))
	templates_references[agg_template]={}
	for field in csv_dict.fieldnames:
			templates_references[agg_template][field]=[]
	for row in csv_dict :
		for field in csv_dict.fieldnames:
			if row[field] is not None and row[field]!="" : 
				templates_references[agg_template][field].append(row[field].lower())
	

#templates={"vandalism":["pp-semi-vandalism"],"pp-dispute":["pp-dispute","Pp-disputed","Protect days","Protect-ex","Protectdays","Protect","Protected","محافظت","حماية_نزاع"]}


################################

def format_date_to_week(timestamp) :
	#transform dates in monday | sunday as a week represetnation formated like this : 2005-11-06 | 2005-11-12
	monday=timestamp-timedelta(days=timestamp.weekday())
	sunday=timestamp+timedelta(days=6-timestamp.weekday())
	return monday.strftime("%Y-%m-%d")+" | "+sunday.strftime("%Y-%m-%d")


########
periods_by_page={}
# for article in
for pageid in articles.keys() :
	print "treating "+str(pageid)
	periods={}
	# for templates in
	for agg_template,temps_refs in templates_references.iteritems() :
		periods[agg_template]={}
		for template_title,templates in temps_refs.iteritems() :
			template_periods=[]
			# load chain of revid
			G=nx.Graph()
			listinsertion = ','.join(['%s'] * len(templates))
			select_cursor.execute("select r1.revid,r1.parentid,r1.timestamp,r2.timestamp from revision r1, revision r2, template t where r1.revid = t.revid and r1.parentid=r2.revid and t.pageid=%s and LOWER(t.template) in (%s)"%(pageid,listinsertion,),tuple(templates))
			row=select_cursor.fetchone()
			# add edge to network
			while row is not None :
				#pp.pprint(row)
				if row[0]!="" and row[1]!="":
					G.add_node(row[0],timestamp=row[2],revid=row[0])
					G.add_node(row[1],timestamp=row[3],revid=row[1])
					# G[row[0]]["revid"]=row[0]
	# 				G[row[0]]["parentid"]=row[1]
	# 				G[row[0]]["timestamp"]=row[2]
	# 				G.add_node(row[1])
	# 				G[row[1]]["revid"]=row[1]
	# 				G[row[1]]["parentid"]=""
	# 				G[row[1]]["timestamp"]=""
					G.add_edge(row[0],row[1])
					#print "add edge "+str(row[0])+" "+str(row[1])
					# fetch a new link
				row=select_cursor.fetchone()
				
			# find connected components
			components_graphs=nx.connected_components(G)#_subgraphs(G)
			for template_chain in components_graphs : 
				# get min and max timestamp. min should equal min(indegree=0) / max should be max(outdegree=0)
				#candidates=template_chain.degree(1)
				#pp.pprint([G.node[n] for n in template_chain])
				startingnode=min(template_chain,key=lambda n: G.node[n]["timestamp"])
				#candidates_enddate=template_chain.out_degree(1)
				endingnode=max(template_chain,key=lambda n: G.node[n]["timestamp"])
				#print str(G.node[startingnode]["timestamp"])+" "+str(G.node[endingnode]["timestamp"])
				template_periods.append({"template":agg_template+"/"+template_title,"startdate":format_date_to_week(G.node[startingnode]["timestamp"]),"startrevi":G.node[startingnode]["revid"],"enddate":format_date_to_week(G.node[endingnode]["timestamp"]),"endrevid":G.node[endingnode]["revid"]})
			
			# agregated same week periods and counting occurencies
			agg_template_periods={}
			for p in template_periods :
				pkey=p["startdate"]+" - "+p["enddate"]
				if pkey in agg_template_periods.keys() :
					agg_template_periods[pkey]["occurences"]+=1
				else :
					p.update({"occurences":1})
					agg_template_periods[pkey]=p
					
				
			periods[agg_template][template_title]=agg_template_periods.values()
		periods_by_page[pageid]=periods
	

for pageid,periods in periods_by_page.iteritems() :	
	# one file by language page_id
	outputfile=open("template_periods_"+articles[pageid]["language"]+"_"+str(pageid)+".json","w+")		
	outputfile.write(json.dumps(periods,sort_keys=True, indent=4))
	outputfile.close()
			
	
		
		
