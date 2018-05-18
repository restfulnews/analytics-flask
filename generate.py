import os
from shutil import copytree, make_archive, rmtree
import jinja2

def generate_website(name, data):

    #make a new folder based on the new websites name
    currentDir = os.getcwd()
    genericWebsite = currentDir + '/website'
    newpath = currentDir + "/" + name
    if not os.path.exists(newpath):
        copytree(genericWebsite , newpath)

    #now need to make the website customized
    customize_website(newpath, name, data)

    #zip the file
    make_archive(newpath, 'zip', newpath)
    #remove the old files as they are now zipped
    rmtree(newpath)
    #return the link to the zipfile so that the user can download
    ziplink = newpath + '.zip'
    return ziplink

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)


def customize_website(filepath, name, data):
    print("customizing the new website")
    htmlFilepath = filepath + '/index.html'
    result = render(htmlFilepath, data)

    with open(htmlFilepath, 'w') as f:
        f.write(result)

    #also want to write the result in templates
    templateFilepath = os.getcwd() + '/templates/' + name + '.html'

    with open(templateFilepath, 'w') as f:
        f.write(result)


'''
news = []
graphs = []
models = []
newsInfo = {
    'title': 'Trump',
    'tags' : 'tags go here',
    'snippet' : 'snippet here',
    'date' : 'date here'
}
news.append(newsInfo)

context = {
'title': 'Trump and aircraft',
'description': 'DESCRIPTION GOES HERE WOOHOOO',
'news' : news,
'email' : 'dummy@email.com',
'pn' : '04imahooker'
}
if news is not []:
    context['news'] = news

if graphs is not []:
    context['graphs'] = graphs

if models is not []:
    context['models'] = models
'''

    
    
