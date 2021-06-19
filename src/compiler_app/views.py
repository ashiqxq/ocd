from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from django.http import JsonResponse
import requests
import sys

# Create your views here.
RUN_URL = "https://api.hackerearth.com/v3/code/run/"
def index(request):
    return render(request, 'compiler_app/ide.html', {})


def runCode(request):
    if request.is_ajax():
	    is_inp = 0
	    source = request.POST['source']
	    lang = request.POST['lang']
	    if 'input' in request.POST:
		    inp = request.POST['input']
		    is_inp = 1
		    with open('inputs.txt', 'w') as snp:
			    snp.write(inp)

	    output = ""
	    flag = 0
	    try:
			# save original standart output reference
		    oso = sys.stdout	 # change the standard output to the file we created
		    osi= sys.stdin
		    sys.stdin = open('inputs.txt', 'r')
		    sys.stdout = open('outputs.txt', 'w')
			# execute code
		    exec(source)  # example =>   print("hello world")
		    sys.stdout.close()
		    sys.stdin.close()
		    sys.stdin = osi
		    sys.stdout = oso  # reset the standard output to its original value

			# finally read output from file and save in output variable
		    with open('outputs.txt', 'r') as f:
		    	output = f.read()
		    otp_html = "<pre>"+output+"</pre"
		    flag = 1
	    except Exception as e:
			# to return error in the code
	    	sys.stdout = oso
	    	sys.stdin = osi
	    	output = e
	    res = {
	    	"run_status": {
	    		"memory_used": "2744",
	    		"time_limit": 5,
	    		"output_html": "Hello&nbsp;world<br>",
	    		"memory_limit": 262144,
	    		"time_used": "1.402842",
	    		"signal": "OTHER",
	    		"exit_code": "0",
	    		"status_detail": "NA",
	    		"status": "AC",
	    		"stderr": "",
	    		"output": "Hello world\n",
	    		"async": 0,
	    		"request_NOT_OK_reason": "",
	    		"request_OK": "True"
	    	},
	    	"compile_status": "OK",
	    	"code_id": "42bb58K"
	    	}
	    if flag:
	    	res["run_status"]["output_html"] = otp_html
	    	res["run_status"]["output"] = output
	    return JsonResponse(res, safe=False)

    else:
    	return HttpResponseForbidden()