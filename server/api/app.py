import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import uuid
import json
import plantuml
import base64
from server.plantumlmodel import PlantUMLModel
from server.api.utils.authentication import HTTPHeaderAuthentication
from server.api.utils.interface import PlantumlGenerationQuery


logging_format = '[%(asctime)s] - [%(levelname)s] - %(message)s'
formatter = logging.Formatter(logging_format)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

for logger_name in ["gunicorn.error", "gunicorn.warning", "gunicorn.info", "gunicorn.access"]:
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()
    logger.addHandler(stream_handler)

gunicorn_error_logger = logging.getLogger("gunicorn.error")
logging.root.setLevel(gunicorn_error_logger.level)

log = logging.getLogger('uvicorn.info')
log.setLevel(logging.INFO)
log.addHandler(stream_handler)

load_dotenv()
app = FastAPI()


with open('utils/allowedOrigins.json', 'r') as file:
    data = json.load(file)
    origins = data['allowedOrigins']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log.info('API startup..')

authentication = HTTPHeaderAuthentication()

plantuml_model = PlantUMLModel(model_name=os.getenv('hugging_face_id'))


@app.get("/health", dependencies=[Depends(authentication)])
async def health_check():
    return 'api_running'


def plantuml_to_base64(plantuml_code):
    plantuml_object = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
    base64_bytes = plantuml_object.processes(plantuml_code)
    base64_string = base64.b64encode(base64_bytes).decode('utf-8')
    return base64_string


def create_response(data):
    payload_json = {'payload': data}
    return Response(json.dumps(payload_json), media_type='application/json')


@app.post("/uml/generator/", dependencies=[Depends(authentication)])
async def process_image_endpoint(query: PlantumlGenerationQuery) -> Response:
    call_uid = uuid.uuid4()
    log_extra = {'call_uid': call_uid}
    _log = logging.getLogger('uvicorn.info')
    call_log = logging.LoggerAdapter(_log, log_extra)
    call_log.info('plantuml_generator call')
    print(query.description)

    try:
        output_plantuml = plantuml_model.generate(query.description)
        print(output_plantuml)
    except Exception as e:
        call_log.info(f'Error while uml generation: {e}')
        raise HTTPException(status_code=500, detail=f"Server error:{e}")

    try:
        base64_image = plantuml_to_base64(output_plantuml)
        return create_response(base64_image)
    except Exception as e:
        call_log.info(f'The response is not a plantuml code: {e}')
        return create_response(output_plantuml)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8070)