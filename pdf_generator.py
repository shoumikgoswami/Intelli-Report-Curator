import pdfkit
import pandas as pd
import base64
import uuid
import glob
import os
import matplotlib.pyplot as plt

path_wkthmltopdf = r'C:\Users\Shoumik\Desktop\Jupyter\voice bot\Machine-learning-Voice-Assistant-master\Machine-learning-Voice-Assistant- v0.5\wkhtmltox\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'no-outline': None
}

def gen_image_64(plot):
	image_name = uuid.uuid4().hex
	plot.savefig('./temp/'+image_name+'.jpg')
	data_uri = base64.b64encode(open('./temp/'+image_name+'.jpg', 'rb').read()).decode('utf-8').replace('\n', '')
	img_tag = '<img src="data:image/png;base64,{0}";>'.format(data_uri)
	return img_tag

def write_to_html_file(df_list, image_list, title='Table'):
	'''
	Write an entire dataframe to an HTML file with nice formatting.
	'''

	result = '''
	<!doctype html>
	<html lang="en">
	   <head>
		  <meta charset="utf-8">
		  <link rel="stylesheet" href="./css/style.css">
	   </head>
	   <body>
		  <div id="ijx4">Report Created by : Intelli - Report Curator</div>
		  <!--<div id="ivtw">FundsNetwork</div>-->
		  <section class="bdg-sect">
			 <h1 class="heading">Data Report</h1>
			 <p class="paragraph">Dear user, here is your personalized report</p>
		  </section>
		  <style>
	
		h2 {
			text-align: center;
			font-family: Helvetica, Arial, sans-serif;
		}
		table { 
			margin-left: auto;
			margin-right: auto;
		}
		table, th, td {
			border: 1px solid black;
			border-collapse: collapse;
		}
		th, td {
			padding: 5px;
			text-align: center;
			font-family: Helvetica, Arial, sans-serif;
			font-size: 90%;
		}
		table tbody tr:hover {
			background-color: #dddddd;
		}
		.wide {
			width: 90%; 
		}

			</style>
		<br>
		<style>
		img {
			display: block;
			margin-left: auto;
			margin-right: auto;
			}
		</style>
	   </body>
	   <html>
	'''
	if len(df_list)>0:
		for i in df_list:
			result += '<h2> %s </h2>\n' % title
			result += i.to_html(classes='wide', escape=False)
			result += '<br>'
	result += '<br>'
	if len(image_list)>0:
		for i in image_list:
			result += i
			result += '<br>'
	result += '''
	</body>
	</html>
	'''
	save_path = './download/'
	filename = uuid.uuid4().hex
	filepath = os.path.join(save_path, filename+'.html')         
	with open(filepath, 'w') as f:
		f.write(result)

def gen_pdf(df_list, image_list):
	write_to_html_file(df_list,image_list,'Table')
	list_of_files = glob.glob('./download/*')
	latest_file = max(list_of_files, key=os.path.getctime)
	try:
		pdfkit.from_file(latest_file, './download/'+uuid.uuid4().hex+'.pdf',configuration=config, options = options)
	except:
		pass