import requests
import os
import sys
import json
import bs4

# Clears the screen in python.
os.system('clear')			

# Creates/opens info.tx in open mode.
status=open('info.txt','a')		



def info_movie():
		
	name = raw_input("\n Enter the title of the movie: ")
	
	# Replaces all whitespaces with string '%20'.
	t = name.replace(' ','%20')	
	
	# The url is stored inside the variable and python can open the url using request module. We need a unique api_key to extract data from domain.	
    url = 'https://api.themoviedb.org/3/search/movie?api_key=ffb07b773769d55c36ccd83845385205&language=en-US&query='+str(t)+'&page=1&include_adult=false'
    response = requests.get(url)
	
	# The response cannot be printed directly as it contains data in dictionary form which is json type.  Python has inbuit library json which takes care of 
	# data files being exchanged between web server and browser.		
    u = json.loads(response.text)
	
	
	# The above variable u stores the result of your search and next two lines extracts the topmost movie and its unique id.
	results  = u['results']
    id = results[0]['id']
	
	# The below url2 variable stores the link which contains complete information of our movie.	
    url2 = 'https://api.themoviedb.org/3/movie/'+str(id)+'?api_key=ffb07b773769d55c36ccd83845385205&language=en-US'
    response = requests.get(url2)
    w = json.loads(response.text)
	
	# w now contains all our information in list with dictionary elements . We can extract our information by referring to the keys.
    try:
	
		# Variables point towards the keys and have our desired results.
		title = w['title']
		imdb_id = w['imdb_id']
		year = w['release_date']
		genre = w['genres']
		language = w['spoken_languages']
		duration = w['runtime']
		plot = w['overview']
		
		
		# The rating value needs to be extracted from the html of the movie page and thus we open the page with url3 which is a normal url and not opened using
		# api_key.This response is of text type and HTML code.		
		url3 = 'http://www.imdb.com/title/'+str(imdb_id)
		response = requests.get(url3)
		html = response.text
		
		# We use beautiful soup and lxml modules to extract the rating of movie and now we are done with all the information.
		soup = bs4.BeautifulSoup(html,"lxml")
		data = soup.select('.ratingValue')
		rating = data[0].get_text('',strip=True)
		
		

		print ("\n\n----------------------------MOVIE INFORMATION-------------------------\n")
		print ("\n\t TITLE       : \t\t"+title)
		print ("\n\t IMDB RATING : \t\t"+rating)
		print ("\n\t RELEASED ON : \t\t"+year)
		print ("\n\t DURATION    : \t\t"+str(duration)+" mins")
		print ("\n\t GENRE       : \t\t"+genre[0]['name'])
		print ("\n\t PLOT        : \t\t"+plot)
		
		
		# Below comands appends the data to txt file which we opened in append mode.
		status.write ("\n\n--------------------------------------MOVIE INFORMATION---------------------------------\n")
		status.write ("\n\t TITLE       : \t\t"+title)
		status.write ("\n\t IMDB RATING : \t\t"+rating)
		status.write ("\n\t RELEASED ON : \t\t"+year)
		status.write ("\n\t DURATION    : \t\t"+str(duration)+" mins")
		status.write ("\n\t GENRE       : \t\t"+genre[0]['name'])
		status.write ("\n\t PLOT        : \t\t"+plot)

    except KeyError:
        print "\nNo such movie titled '"+name+"' found!\n"
        status.write ("\nNo such movie titled '"+name+"' found!\n")
    
    
def top_movies():
    x = input("\nEnter n, to display Top 'n' movies: " )
    url = 'http://www.imdb.com/chart/top'
    response = requests.get(url)
    html = response.text
	
	# Stores the complete webpage html code
    soup = bs4.BeautifulSoup(html,"lxml")			
    rows = soup.select('.lister-list tr')				
    print ("\n"+"----------------------------------TOP "+str(x)+" MOVIES ACCORDING TO IMDB RATINGS---------------------------------"+"\n\n")
    print (" \t   TITLE\t\t\t\t\t\t\t\t\t\t   IMDB RATING\n\n")
    status.write ("\n"+"---------------------------TOP "+str(x)+" MOVIES ACCORDING TO IMDB RATINGS-----------------------------"+"\n\n")
    status.write (" \t   TITLE\t\t\t\t\t\t\t\t\t\t   IMDB RATING\n\n")
    
    for row in range(0,x):
        tdata=rows[row].select('td')
		# Extracts name of movie
        name=tdata[1].get_text(' ',strip=True)
		# Extracts rating of movie
        rating=tdata[2].get_text(' ',strip=True)			 					
        ans=("\n "+name.ljust(75,' ')+"\t\t\t\t"+rating+"\n")
        ans=ans.encode('ascii','ignore')
        print ans
		# Appends data in file info.txt 
        status.write (ans)											 					
        
        
def folder():
    path = raw_input("\n\nEnter the complete path of the directory where your movies are present: ")
    dirs = os.listdir(path)
    print "Showing results for the path: "+path+"\n"
    status.write ('Showing results for the path: '+path+'\n')
	
	# The process is similar to the one encountered in method info_movie.   
    for i in range(len(dirs)):
		x = dirs[i]
		t = x.replace(' ','%20')
		url = 'https://api.themoviedb.org/3/search/movie?api_key=ffb07b773769d55c36ccd83845385205&language=en-US&query='+str(t)+'&page=1&include_adult=false'
		response = requests.get(url)
		u = json.loads(response.text)
		results  = u['results']
		id = results[0]['id']
		url2 = 'https://api.themoviedb.org/3/movie/'+str(id)+'?api_key=ffb07b773769d55c36ccd83845385205&language=en-US'
		response = requests.get(url2)
		w = json.loads(response.text)

		try:
			title = w['title']
			year = w['release_date']
			imdb_id = w['imdb_id']

			url3 = 'http://www.imdb.com/title/'+str(imdb_id)
			response = requests.get(url3)
			html = response.text
			soup = bs4.BeautifulSoup(html,"lxml")
			data = soup.select('.ratingValue strong span')
			rating = data[0].get_text('',strip=True)

			x = x.encode('ascii','ignore')
			y = "["+rating+"] "+title+" ("+year+")"
			y = y.encode('ascii','ignore')
			print "\n"+y
			status.write ("\n"+y)
			os.rename(os.path.join(path, x), os.path.join(path, y))			
			print "Renaming Done\n"
			status.write ('Renaming Done\n')
		except KeyError:
			print "\nNo such movie titled '"+x+"' found or else read the instructions before using this feature!\n"
			status.write ("\nNo such movie titled '"+x+"' found else read the instructions before using this feature!\n")


def driver():
    print "\n\n\t\t\t\t\t----------------IMDB PORTAL--------------------"
    status.write("\\\n\n\t\t\t\t\t---------------------IMDB PORTAL----------------------")
    choice=input('Enter your choice:\n\n1) Search movie information by title\n2) Show top rated movies\n3) Rename folder with IMDB rating and year of release added to it\n\nInput: ')
    
    if(choice == 1):
        info_movie()
    elif(choice == 2):
        top_movies()
    else:
            folder()
            
        
driver()
while (1>0) :
    repeat = raw_input("\n\nDo you want to try again?(type 'Yes'/'Y'/'y' or else press anything) ")
    if (repeat == 'Yes') or (repeat == 'Y') or (repeat == 'y'):
        os.system('clear')
        driver()
    else:
        print "\nThank you for using!"
        status.write("\nThank you for using!")
        break
# Closes the text file 
status.close()
