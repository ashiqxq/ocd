from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from django.http import JsonResponse
import shutil, subprocess

# Create your views here.
RUN_URL = "https://api.hackerearth.com/v3/code/run/"


def index(request):
    return render(request, "compiler_app/ide.html", {})


def runCode(request):
    if request.is_ajax():
        source = request.POST["source"]
        lang = request.POST["lang"]
        if lang == "JAVA":
            _, _, after_keyword = source.split("public static void main")[0].partition(
                "class"
            )
            class_name = after_keyword.split(" ")[1]
            codefile = class_name
        # elif lang == "CSHARP":
        #     pass
        else:
            codefile = "main"
        inp = ""
        output = ""
        otp_html = ""
        if "input" in request.POST:
            inp = request.POST["input"]
        with open("codes.txt", "w") as cf, open("inputs.txt", "w") as snp:
            cf.write(source)
            snp.write(inp)
        file_ext = {
            "CPP": "cpp",
            "C": "c",
            "PYTHON": "py",
            "JAVA": "java",
            "JAVASCRIPT": "js",
            "CSHARP": "cs",
        }
        run_cmd = {
            "CPP": "g++",
            "C": "gcc",
            "JAVA": "javac",
            "JAVASCRIPT": "node",
            "CSHARP": "mcs",
        }
        shutil.copyfile("codes.txt", f"{codefile}.{file_ext[lang]}")
        open("codes.txt", "w").close()
        subprocess.run(["rm", "codes.txt"])
        if lang == "C" or lang == "CPP":
            with open("inputs.txt", "r") as inpt, open("outputs.txt", "w") as outpt:
                proc = subprocess.run(
                    [
                        run_cmd[lang],
                        f"{codefile}.{file_ext[lang]}",
                        "-o",
                        f"{codefile}",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                # print(proc.stderr, proc.stdout)
                subprocess.run(["rm", f"{codefile}.{file_ext[lang]}"])
                error = proc.stderr
                if error == "":
                    proc = subprocess.run(
                        [f"./{codefile}"],
                        stdin=inpt,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    inpt.close()
                    subprocess.run(["rm", f"{codefile}"])
                    output = proc.stdout
                    error = proc.stderr
                    if error == "":
                        outpt.write(output)
                    else:
                        outpt.write(error)
                else:
                    outpt.write(error)
                outpt.close()
            subprocess.run(["rm", "inputs.txt"])
        elif lang == "CSHARP":
            with open("inputs.txt", "r") as inpt, open("outputs.txt", "w") as outpt:
                proc = subprocess.run(
                    [
                        run_cmd[lang],
                        f"{codefile}.{file_ext[lang]}",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                subprocess.run(["rm", f"{codefile}.{file_ext[lang]}"])
                error = proc.stderr
                if error == "":
                    proc = subprocess.run(
                        ["mono", f"{codefile}.exe"],
                        stdin=inpt,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    inpt.close()
                    subprocess.run(["rm", f"{codefile}.exe"])
                    output = proc.stdout
                    error = proc.stderr
                    if error == "":
                        outpt.write(output)
                    else:
                        outpt.write(error)
                else:
                    outpt.write(error)
                outpt.close()
            subprocess.run(["rm", "inputs.txt"])
        elif lang == "PYTHON":
            with open("inputs.txt", "r") as inpt, open("outputs.txt", "w") as outpt:
                proc = subprocess.run(
                    ["python3", f"{codefile}.{file_ext[lang]}"],
                    stdin=inpt,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                subprocess.run(["rm", f"{codefile}.{file_ext[lang]}"])
                inpt.close()
                output = proc.stdout
                error = proc.stderr
                if error == "":
                    outpt.write(output)
                else:
                    outpt.write(error)
                outpt.close()
            subprocess.run(["rm", "inputs.txt"])
        elif lang == "JAVASCRIPT":
            with open("inputs.txt", "r") as inpt, open("outputs.txt", "w") as outpt:
                proc = subprocess.run(
                    [run_cmd[lang], f"{codefile}.{file_ext[lang]}"],
                    stdin=inpt,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                subprocess.run(["rm", f"{codefile}.{file_ext[lang]}"])
                inpt.close()
                output = proc.stdout
                error = proc.stderr
                if error == "":
                    outpt.write(output)
                else:
                    outpt.write(error)
                outpt.close()
            subprocess.run(["rm", "inputs.txt"])
        elif lang == "JAVA":
            with open("inputs.txt", "r") as inpt, open("outputs.txt", "w") as outpt:
                proc = subprocess.run(
                    [
                        run_cmd[lang],
                        f"{codefile}.{file_ext[lang]}",
                        # "-o",
                        # f"{codefile}",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                subprocess.run(["rm", f"{codefile}.{file_ext[lang]}"])
                error = proc.stderr
                if error == "":
                    proc = subprocess.run(
                        ["java", f"{class_name}"],
                        stdin=inpt,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    inpt.close()
                    subprocess.run(["rm", f"{codefile}.class"])
                    output = proc.stdout
                    error = proc.stderr
                    if error == "":
                        outpt.write(output)
                    else:
                        outpt.write(error)
                else:
                    outpt.write(error)
                outpt.close()
            subprocess.run(["rm", "inputs.txt"])
        with open("outputs.txt", "r") as f:
            output = f.read()
            otp_html = "<pre>" + output + "</pre>"
            f.close()
        subprocess.run(["rm", "outputs.txt"])
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
                "request_OK": "True",
            },
            "compile_status": "OK",
            "code_id": "42bb58K",
        }
        res["run_status"]["output_html"] = otp_html
        res["run_status"]["output"] = output
        return JsonResponse(res, safe=False)

    else:
        return HttpResponseForbidden()
