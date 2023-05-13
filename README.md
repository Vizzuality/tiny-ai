# Tiny-AI

An easy-to-use interface for OpenAI's GPT-3.5-turbo model (upgradeable to GPT-4 if available). This API enables you to submit a question and context and receive an AI-generated response. While it's remarkably straightforward, it offers numerous potential use cases:

- Explaining a visual representation with a preferred tone.
- Describing data extracted from a JSON object.
- Summarizing, expanding, or altering a text with each interaction.
- And much more; your imagination is the only limit. Explore the parameters 'context', 'question', and 'temperature' and enrich them combined with your app logic.

## Installation

1. Install Python 3.8 or higher
2. Clone the repository
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
1. Set your API secret token and OpenAI API key in the .env file:

```bash
SECRET_TOKEN=<your_secret_token>
OPEN_AI_TOKEN=<your_openai_api_key>
```

2. Start the FastAPI server:

```bash
uvicorn main:app --reload
```
3. Make a request to the API using cURL or any HTTP client (e.g., Postman) with the following parameters:

- question: The question you want to ask the AI (mandatory)
- context: The context provided to the AI (mandatory)
- temperature: The temperature value for the AI response (optional, defaults to 0.5)

## Example
Send a request to the API using the following JSON object:

```json
{
  "context": {
    "data": {
      "Apples": "0.90 kg",
      "Bananas": "1.43 kg",
      "Barley": "0.24 kg",
      "Beef": "36.44 kg"
    }
  },
  "question": "Given this data of CO2 emissions per material, explain the impact in a concise way.",
  "temperature": 0
}
```

```bash
curl -X POST "http://127.0.0.1:8000/" -H "accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer <your_secret_token>" -d '{"context": {"data": {"Apples": "0.90 kg","Bananas": "1.43 kg","Barley": "0.24 kg","Beef": "36.44 kg"}}, "question": "Given this data of CO2 emissions per material, explain the impact in a concise way.", "temperature": 0}'
```

Response with temperature 0:

```json
{
  "response": "The data shows the amount of CO2 emissions per unit of material produced. Beef production has the highest CO2 emissions per unit, while barley has the lowest."
}
```

Response with temperature 1:

```json
{
  "response": "The data shows the amount of CO2 emissions per kilogram of production for certain materials. Beef production has a much higher impact on CO2 emissions compared to apple, banana, and barley production."
}
```

License
MIT License

Copyright (c) 2023 Vizzuality

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.