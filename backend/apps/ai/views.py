from django.http import HttpRequest, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.validators import validate_post_request_with_fields
from apps.ai.core.agents.general_agent import GeneralAgent
from common.logger import logger
import json


@validate_post_request_with_fields(["prompt"])
@csrf_exempt
def ask_policy_assitant(request: HttpRequest):
    body_params = json.loads(request.body.decode('utf-8'))
    prompt = body_params["prompt"]

    user_id = request.user_id

    try:
        policy_assistant = GeneralAgent(user_id=user_id)
        response = policy_assistant.prompt(message=prompt)
        return JsonResponse({"status": 200, "message": response})

    except Exception as e:
        return JsonResponse({"status": 500, "message": f"An error ocurred: {e}"})


@validate_post_request_with_fields(["prompt"])
@csrf_exempt
def experimental_streaming_assistant(request: HttpRequest):
    body_params = json.loads(request.body.decode('utf-8'))
    prompt = body_params["prompt"]
    user_id = request.user_id

    try:
        policy_assistant = GeneralAgent(user_id=user_id)

        def response_generator():
            for part in policy_assistant.stream_prompt(message=prompt):
                logger.info(f"Stream part: {part}")
                yield part

        return StreamingHttpResponse(response_generator(), content_type='application/json')

    except Exception as e:
        def error_generator():
            logger.error(f"An error ocurred: {e}")
            yield json.dumps({"status": 500, "message": "An internal error occured while processing your request. Please try again."})

        return StreamingHttpResponse(error_generator(), content_type='application/json')


@validate_post_request_with_fields(["query"])
@csrf_exempt
def quick_search(request: HttpRequest):
    body_params = json.loads(request.body.decode('utf-8'))
    query = body_params["query"]

    general_agent = GeneralAgent()
    results = general_agent.hybrid_title_search(
        title=query, result_type="JSON")

    return JsonResponse({"status": 200, "message": results})
