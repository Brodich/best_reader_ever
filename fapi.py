from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from typing import Optional, Dict, Any
import json

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Читаем сырое тело запроса (raw body)
    raw_body = ""
    try:
        raw_body_bytes = await request.body()
        raw_body = raw_body_bytes.decode("utf-8")
    except Exception as e:
        raw_body = f"Ошибка при чтении тела запроса: {str(e)}"

    # Пытаемся прочитать JSON (если Content-Type: application/json)
    json_body = {}
    try:
        json_body = await request.json()
    except:
        pass

    # Пытаемся прочитать form-data (если Content-Type: multipart/form-data или application/x-www-form-urlencoded)
    form_data = {}
    try:
        form_data = await request.form()
        form_data = dict(form_data)
    except:
        pass

    # Собираем информацию о запросе
    client_host = request.client.host if request.client else "Unknown"
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)
    cookies = dict(request.cookies)
    query_params = dict(request.query_params)

    # Формируем HTML
    html_content = f"""
    <html>
        <head>
            <title>Информация о запросе</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; }}
                .section {{ margin-bottom: 20px; }}
                .request-type {{
                    display: inline-block;
                    padding: 5px 10px;
                    background: #{'4285f4' if method == 'GET' else '0f9d58'};
                    color: white;
                    border-radius: 3px;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h1>Информация о запросе <span class="request-type">{method}</span></h1>
            
            <div class="section">
                <h2>Основная информация</h2>
                <p><strong>Метод:</strong> {method}</p>
                <p><strong>URL:</strong> {url}</p>
                <p><strong>Клиентский IP:</strong> {client_host}</p>
            </div>
            
            <div class="section">
                <h2>Query параметры</h2>
                <pre>{pretty_dict(query_params)}</pre>
            </div>
            
            <div class="section">
                <h2>Сырое тело запроса (raw body)</h2>
                <pre>{raw_body if raw_body else "Пустое тело запроса"}</pre>
            </div>
            
            <div class="section">
                <h2>JSON данные (если есть)</h2>
                <pre>{pretty_dict(json_body)}</pre>
            </div>
            
            <div class="section">
                <h2>Form данные (если есть)</h2>
                <pre>{pretty_dict(form_data)}</pre>
            </div>
            
            <div class="section">
                <h2>Cookies</h2>
                <pre>{pretty_dict(cookies)}</pre>
            </div>
            
            <div class="section">
                <h2>Заголовки</h2>
                <pre>{pretty_dict(headers)}</pre>
            </div>
            
            <div class="section">
                <h2>Отправить тестовые данные</h2>
                <form method="POST" action="/" enctype="multipart/form-data">
                    <div>
                        <label>Текстовое поле: <input type="text" name="text_field" value="Тест"></label>
                    </div>
                    <div>
                        <label>Файл: <input type="file" name="file_field"></label>
                    </div>
                    <button type="submit">Отправить как form-data</button>
                </form>
                
                <p>Или отправьте JSON запрос (например, через curl):</p>
                <pre>curl -X POST -H "Content-Type: application/json" -d '{{"key":"value"}}' {url}</pre>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

def pretty_dict(data: Dict[str, Any]) -> str:
    """Форматирует словарь в читаемый вид"""
    if not data:
        return "Нет данных"
    return json.dumps(data, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)