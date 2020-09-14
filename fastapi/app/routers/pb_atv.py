# FastAPI modules
from fastapi import APIRouter, HTTPException, File, UploadFile 
import urllib.request
from pydantic import BaseModel

# Dependencies for saving uploaded file
import os
import shutil
from pathlib import Path

# Declare tuple with subtypes
from typing import Any, Dict

# import third party library
import importdir
import json
from collections import OrderedDict


router = APIRouter()


def append_keyvalue(event,output_field,steps_response):
    event[output_field] = str(steps_response)
    return event

def return_response(event):
    event2 = OrderedDict()
    event2["uuid"] = event["uuid"]
    if event["validDecrypt"] == True:
        event2["status"] = "validated"
    else:
        event2["status"] = "invalidated"
        #event2["status"] = event["validDecrypt"]
    return event2

def execute_step(event, function_name, function_input, function_output, function_args):
    importdir.do("/app/python_scripts", globals())
    try:
        function_mod,function_call = function_name.split('.',2)
        active_function = getattr(globals()[function_mod], function_call)
        event = active_function(event, function_input, function_output, function_args)
    except Exception as e:
        event = append_keyvalue(event,"status","failedinstep")
        #event = append_keyvalue(event,"status",str(e))
    return event

class ExecuteGoInputs(BaseModel):
    event: Dict
    rule: list

@router.post("/go/execute_go", tags=["go"])
def execute_go(item: ExecuteGoInputs):
    event=item.event
    steps=item.rule
    try:
        for step in steps:
            event = execute_step(event,step['function'],step['input'],step['output'],step['argument'])
    except Exception as e:
        event = append_keyvalue(event,"status","failedinloop")
        #event = append_keyvalue(event,"status",str(e))
    return return_response(event) #output after post

class ExecuteScriptInputs(BaseModel):
    module_name: str = "base"
    function_name: str
    event: Any
    function_input: list
    function_output: list
    function_args: list

@router.post("/go/execute_script", tags=["go"])
def execute_script(item: ExecuteScriptInputs):
    importdir.do("/app/python_scripts", globals())
    function_input = item.function_input
    try:
        active_function = getattr(globals()[item.module_name],item.function_name)
    except:
        return "module/function not found"
    try:
        function_result = active_function(item.event,item.function_input,item.function_output,item.function_args)
        return function_result
    except:
        return "error executing function"

# class Item(BaseModel):
#     mod: str = "base"
#     func: str
#     func_input: Any = None

# @router.post("/atv/execute_func", tags=["atv"])
# def execute_script(item:Item):
#     importdir.do("/app/python_scripts", globals())
#     function_input = item.func_input
#     try:
#         simple_function = getattr(globals()[item.mod],item.func)
#     except:
#         return "Module/Function not available to execute"
#     try:    
#         if len(function_input) == 1:
#             return str(simple_function(function_input[0]))
#         else:
#             return str(simple_function(*function_input))
#     except:
#         return "Error while executing function"


# #class Step(BaseModel):
# #    treat: str
# #    function: str
# #    func_input: Any = None
# #    command_output: Any = "Output"

# def atv_append_keyvalue(event,output_field,atv_steps_response):
#     event[output_field] = str(atv_steps_response)
#     return event

# def atv_return_response(treat_event):
#     event = json.loads(treat_event)
#     event2 = {}
#     event2["uuid"] = event["uuid"]
#     event2["status"] = event["status"]
#     return json.dumps(event2)

# def execute_step(event, function_name, function_input, function_output): 
#     importdir.do("/app/python_scripts", globals())
#     try:
#         event = json.loads(event)
#         simple_function = getattr(globals()["base"],function_name)
#         if len(function_input) == 1:
#             response = str(simple_function(event[function_input[0]]))
#         else:
#             response = str(simple_function(event[function_input[0]],function_input[1]))
#         event = atv_append_keyvalue(event,function_output[0],response)
#     except Exception as e:
#         event = atv_append_keyvalue(event,"status",str(e))
#     return json.dumps(event).strip('"').replace('\\','')
    
# class TreatandRule(BaseModel):
#     event: str
#     steps: list

# @router.post("/atv/execute_steps", tags=["atv"])
# def execute_atv(item: TreatandRule):
#     event = item.event # str
#     steps = item.steps # list
#     try:
#         for step in steps:
#             event = execute_step(event,step['function'],step['input'],step['output']) # to return event with updated info, last step to update status as output for step
#     except Exception as e:
#         event = atv_append_keyvalue(event,"status",str(e))
#     return atv_return_response(event) # str
