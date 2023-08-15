import os 
import openai
import requests
import shutil

os.environ["OPENAI_API_KEY"] = 'YOUR OPENAI API KEY'
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_prompt(topic):
    prompt = f'''
    You are my personal assistant for daily blogs.
    I want you to write me a blog post for my blog. 
    The format will be like the following and the topic is {topic}.
    I want you to give a title and tags for the blog post.
    
    '''
    return prompt




def dalle2_prompt(topic):
    prompt = f' An image related to {topic}, Sigma 85 mm f/1.4 '
    return prompt





def save_image(image_url, file_name):
    image_res = requests.get(image_url, stream=True)
    
    if image_res.status_code == 200:
        with open(file_name, 'wb') as f:
            image_res.raw.decode_content = True
            shutil.copyfileobj(image_res.raw, f)
    else:
        print(f'Error on downloading image. Status code: {image_res.status_code}')
    
    return image_res.status_code , file_name

 

def get_blog_content_openai(topic):
    
    prompt  = create_prompt(topic)
    response = openai.Completion.create(engine = 'text-davinci-003',
                                   prompt = create_prompt(topic),
                                   max_tokens = 1000,
                                   temperature = 0.7)
    blog_content = response['choices'][0]['text']
    
    return blog_content







def get_cover_image(topic,save_path):

    image_prompt = dalle2_prompt(topic)
    image_response = openai.Image.create(prompt = image_prompt,
                              n = 1,size = '1024x1024')
    image_url = image_response['data'][0]['url']
    
    #get the statues code and the file name where the url of the image is saved
    status_code, file_name = save_image(image_url, save_path)
    
    return status_code, file_name