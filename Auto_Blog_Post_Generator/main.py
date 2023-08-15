from pathlib import Path
import openai_utils
import html_utils

topic = input('Write a topic on for your blog post generation: ')



PATH_TO_BLOG_REPO = Path('/Users/apple/Documents/GitHub/doruktarhan.github.io/.git') #Replace this with the Path of Github on your Local Repo
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
PATH_TO_CONTENT = PATH_TO_BLOG/'content'
PATH_TO_CONTENT.mkdir(exist_ok = True, parents = True)


blog_content = openai_utils.get_blog_content_openai(topic)


blog_content_remaining = blog_content[blog_content.find('Tags')+6:]
image_name = blog_content_remaining.split(' ')[0][:-1]


_,cover_image_saved_path = openai_utils.get_cover_image(topic, image_name )

path_to_new_content = html_utils.create_new_blog(PATH_TO_CONTENT,topic, blog_content, cover_image_saved_path)
html_utils.write_to_index(PATH_TO_BLOG,path_to_new_content)



html_utils.update_blog(PATH_TO_BLOG_REPO)


























