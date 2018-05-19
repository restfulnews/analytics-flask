import os
from shutil import copytree, make_archive, rmtree
import jinja2
import re
import datarobot as dr
import pandas as pd

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
    
    #also need to change the result to use the appropriate things
    result = result.replace("vendor/bootstrap/css/bootstrap.min.css", "{{ url_for('static', filename='vendor/bootstrap/css/bootstrap.min.css') }}")
    result = result.replace("vendor/font-awesome/css/font-awesome.min.css", "{{ url_for('static', filename='vendor/font-awesome/css/font-awesome.min.css') }}")
    result = result.replace("vendor/devicons/css/devicons.min.css", "{{ url_for('static', filename='vendor/devicons/css/devicons.min.css') }}")
    result = result.replace("vendor/simple-line-icons/css/simple-line-icons.css", "{{ url_for('static', filename='vendor/simple-line-icons/css/simple-line-icons.css') }}")
    result = result.replace("css/resume.min.css", "{{ url_for('static', filename='css/resume.min.css') }}")

    result = result.replace("vendor/jquery/jquery.min.js", "{{ url_for('static', filename='vendor/jquery/jquery.min.js') }}")
    result = result.replace("vendor/bootstrap/js/bootstrap.bundle.min.js", "{{ url_for('static', filename='vendor/bootstrap/js/bootstrap.bundle.min.js') }}")
    result = result.replace("vendor/jquery-easing/jquery.easing.min.js", "{{ url_for('static', filename='vendor/jquery-easing/jquery.easing.min.js') }}")
    result = result.replace("js/resume.min.js", "{{ url_for('static', filename='js/resume.min.js') }}")

    with open(templateFilepath, 'w') as f:
        f.write(result)

def generate_source_data(name, path, data):
    newData = str(data)
    newData = re.sub("'", "\"", newData)
    tempJson = name + "temp.json"

    with open(tempJson, 'w') as f:
        f.write(str(newData))
    #load json into a pandas data frame


    json = pd.read_json(tempJson)
    #write the data to the csv file
    json.to_csv(path, index=False)

    os.remove(tempJson)
    
    print("generated data")


def generate_model(name, data):
    sourceData = 'modelData/' + name + ".csv"
    generate_source_data(name, sourceData, data)
    
    api_key = "apuu5rs3mpuIbAGGbadkMOQicY5btndS"
    dr.Client(token=api_key, endpoint='https://app.datarobot.com/api/v2')

    project = dr.Project.start(project_name=name,
                        sourcedata='test.csv',
                        target='target')

    
    return "model"


