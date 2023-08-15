from git import Repo
from pathlib import Path
import shutil
from bs4 import BeautifulSoup as Soup
import os
import re

github_access_token = 'YOUR GITHUB ACCESS TOKEN'


#update the blog 
def update_blog(PATH_TO_BLOG_REPO,commit_message = 'Update on blog'):
    #GitPython Repo Location
    repo = Repo(PATH_TO_BLOG_REPO)
    #git add command
    repo.git.add(all=True)
    #git commit -m 'updates blog'
    repo.index.commit(commit_message)
    #git push
    origin = repo.remote(name = 'origin')
    
   
    
    #the following commented part is for cleaning the url 
    '''
    # The modified URL with tokens
    url = #write the url does not work here with access token in it
    

    # Use regular expression to replace tokens
    cleaned_url = re.sub(r'https://(ghp_[^@]+@)+', 'https://', url)
    
    print(cleaned_url)
    
    origin.config_writer.set("url", cleaned_url)
    '''
    
    # Update the remote URL to include the access token
    remote_url = origin.config_reader.get("url")
    print(f'\n original url is {remote_url}')
    remote_url_with_token = remote_url.replace("https://", f"https://{github_access_token}@")
    print(f'\n final url with token is {remote_url_with_token}')
    origin.config_writer.set("url", remote_url_with_token)


    try:
        origin.push()
        print('\n update completed')
    finally:
        # Revert back to the original URL after push
        origin.config_writer.set("url", remote_url)
    

#create a blog post with true html format given title image and content
def create_new_blog(PATH_TO_CONTENT,title, content, cover_image):
    
    cover_image = Path(cover_image)

    
    new_title = f"{title.replace(' ','_')}.html"
    path_to_new_content = PATH_TO_CONTENT/new_title
    
    #copy the image folder to the pwd
    shutil.copy(cover_image, PATH_TO_CONTENT)
    
    if not os.path.exists(path_to_new_content):
        with open(path_to_new_content, "w") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write(f"<title> {title} </title>\n")
            f.write("</head>\n")
            
            f.write("<body>\n")
            f.write(f"<img src='{cover_image.name}' alt='Cover Image'> <br />\n")
            f.write(f"<h1> {title} </h1>")
            #openai format to html format
            f.write(content.replace("\n", "<br />\n"))
            f.write("</body>\n")
            f.write("</html>\n")
            print("Blog created")
            return path_to_new_content
    else:
        raise FileExistsError("File already exist! Abort")
        
        
        

#checking duplicate links inside path to new content
def check_for_duplicate_links(path_to_new_content,links):
    #list of the links
    urls = [str(link.get('href')) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    check = content_path in urls
    return check
    
    
    
        
# write the blog post link      
def write_to_index(PATH_TO_BLOG,path_to_new_content):
   with open(PATH_TO_BLOG/'index.html') as index:
       soup = Soup(index.read())
   
   links = soup.find_all('a')
   last_link = links[-1]
   
   if check_for_duplicate_links(path_to_new_content,links):
       raise ValueError('Link already exists')
   
   link_to_new_blog = soup.new_tag('a',href = Path(*path_to_new_content.parts[-2:]))
   link_to_new_blog.string = path_to_new_content.name.split('.')[0]
       
   # Find the last link and add a new line before appending the new link
   last_link = links[-1]
   new_line = soup.new_tag('br ') 
   last_link.insert_after(link_to_new_blog)
   last_link.insert_after(new_line)
 
   
   with open(PATH_TO_BLOG/'index.html','w') as f:
       f.write(str(soup.prettify(formatter='html')))
              
       
       
       
       
         