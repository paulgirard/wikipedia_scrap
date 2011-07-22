

import re
import MySQLdb.cursors

conn1 = MySQLdb.connect (host = "localhost",
						user='controversy_user',
						passwd='controversy_pass',
						db='wikipediaControversies',
						cursorclass = MySQLdb.cursors.SSCursor)
conn2 = MySQLdb.connect (host = "localhost",
						user='controversy_user',
						passwd='controversy_pass',
						db='wikipediaControversies',
						cursorclass = MySQLdb.cursors.SSCursor)
select_cursor = conn1.cursor ()
insert_cursor = conn2.cursor ()

#dump template table
select_cursor.execute ("DELETE FROM template;")
print "querying"

# get contents from revisions
select_cursor.execute ("SELECT revid, content,language,pageid from revision");#	where pageid=5042951");
row=select_cursor.fetchone()
templates=[]
while row is not None:
	if row[1] is not None :
		# parse content
		revid=row[0]
		content=row[1]
		language=row[2]
		pageid=row[3]
		# template item
		wikitemplates=re.findall("\{\{(.*?)\}\}",content)
		
		for template in wikitemplates :
	# 			print template
			 
			if "|" in template : 
			    templateparts=template.split("|")
			    template=templateparts[0]
			    templatemetadata="|".join(templateparts[1:])
			else :
			    templatemetadata=""
			
			
			
			tmp=[]
			tmp.append(template)
	 		tmp.append(templatemetadata)
	 		tmp.append(revid)
	 		tmp.append(pageid)
	 		tmp.append(language)
	 		templates.append(tmp)
	 			
	 	if len(templates)>50000 :
		 	print "inserting "+str(len(templates))+" templates"
		 	insert_cursor.executemany("insert into template (template,metadata,revid,pageid,language) values (%s,%s,%s,%s,%s)",templates)
		 	templates=[]
			#store templates
			# template` VARCHAR(512) NOT NULL,
			# 			`metadata` TEXT,
			# 			`revid` INT NOT NULL,
			# 			`pageid` INT NOT NULL,
			# 			`language` VARCHAR(8) NOT NULL 
		
	row=select_cursor.fetchone()

print "done"	
	
select_cursor.close()
insert_cursor.close()
conn1.close ()
conn2.close ()
