from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from django.http import JsonResponse
import requests
import sys
import shutil, subprocess

# Create your views here.
RUN_URL = "https://api.hackerearth.com/v3/code/run/"
def index(request):
    return render(request, 'compiler_app/ide.html', {})


def runCode(request):
    if request.is_ajax():
        source = request.POST['source']
        lang = request.POST['lang']
        print(lang)
        inp = ""
        output = ""
        otp_html = ""
        if 'input' in request.POST:
            inp = request.POST['input']
        with open('codes.txt', 'w') as cf, open('inputs.txt', 'w') as snp:
            cf.write(source)
            snp.write(inp)
        codefile = 'test'
        file_ext = {'CPP': 'cpp', 'C': 'c', 'PYTHON': 'py'}
        run_dict = {'CPP': [f'{codefile}'], 'C': [f'{codefile}'], 'PYTHON': ['python', f'{codefile}.{file_ext[lang]}']}
        shutil.copyfile('codes.txt', f'{codefile}.{file_ext[lang]}')
        open('codes.txt', 'w').close()
        if lang == 'C':
            subprocess.run(['gcc', f'{codefile}.c', '-o', f'{codefile}'])
        elif lang == 'CPP':
            subprocess.run(['g++', f'{codefile}.cpp', '-o', f'{codefile}'])
        with open('inputs.txt', 'r') as inpt, open('outputs.txt', 'w') as outpt:
            print(inpt, outpt)
            of = subprocess.run(run_dict[lang], stdin=inpt, stdout=outpt, text=True)
        with open('outputs.txt', 'r') as f:
            output = f.read()
            otp_html = "<pre>"+output+"</pre>"
        open('inputs.txt', 'w').close()
        open('outputs.txt', 'w').close()
        # if 'input' in request.POST:
        #     inp = request.POST['input']
        #     is_inp = 1
        #     with open('inputs.txt', 'w') as snp:
        # 	    snp.write(inp)
        #
        # output = ""
        # flag = 0
        # try:
        # 	# save original standart output reference
        #     oso = sys.stdout	 # change the standard output to the file we created
        #     osi= sys.stdin
        #     sys.stdin = open('inputs.txt', 'r')
        #     sys.stdout = open('outputs.txt', 'w')
        # 	# execute code
        #     exec(source)  # example =>   print("hello world")
        #     sys.stdout.close()
        #     sys.stdin.close()
        #     sys.stdin = osi
        #     sys.stdout = oso  # reset the standard output to its original value
        #
        # 	# finally read output from file and save in output variable
        #     with open('outputs.txt', 'r') as f:
        #     	output = f.read()
        #     otp_html = "<pre>"+output+"</pre>"
        #     flag = 1
        # except Exception as e:
        # 	# to return error in the code
        # 	sys.stdout = oso
        # 	sys.stdin = osi
        # 	output = e
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
        res["run_status"]["output_html"] = otp_html
        res["run_status"]["output"] = output
        return JsonResponse(res, safe=False)

    else:
        return HttpResponseForbidden()