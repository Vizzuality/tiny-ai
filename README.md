# Tiny-AI

An easy-to-use interface for OpenAI's GPT-3.5-turbo model (upgradeable to GPT-4 if available). This API enables you to submit a question and context, receive an AI-generated response in the requested idiom, and optionally, returns the AI responses converted to audio files.

Highlights:

1. Multi-language support: You can set the language parameter, and the API will provide AI-generated responses in the requested language.
2. Audio file conversion: The API can convert AI-generated text responses into audio files, providing narration in the requested language.

While it's remarkably straightforward, it offers numerous potential use cases:

- Enhance data accessibility for individuals with visual impairments.
- Enhance data accessibility for small devices.
- Explain a visual representation with a preferred tone.
- Describe data extracted from a JSON object.
- Summarize, expand, or alter a text for each interaction.
- And much more; your imagination is the only limit. Explore the parameters 'context', 'question', and 'temperature' and **enrich them combined with your app logic**.

## Installation

1. Install Python 3.8 or higher
2. Clone the repository
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
1. Set this API secret token and OpenAI API key in the .env file:

```bash
SECRET_TOKEN=<your_secret_token>
OPEN_AI_TOKEN=<your_openai_api_key>
```

2. Start the FastAPI server:

```bash
uvicorn main:app --reload
```
3. Make a request to the API using cURL or any HTTP client (e.g., Postman) with the required parameters.

## parameters
- context: The data or text that the embeding app shows and must be sent to the AI as context. [str, Dict] (mandatory)
- question: The desired question related to the context sent. [str, Dict] (mandatory)
- temperature: A value from 0 to 1 for the amount of creativity in the AI response (optional, defaults to 0.5)
- audio: Whether an audio file for text-to-speech is required or not. [boolean] (optional, default: false)
- lang: The desired language following the [Google language codes](https://developers.google.com/admin-sdk/directory/v1/languages). [str] (optional, default: 'en')

There is a list of the available languages at the bottom. Not all of them were tested.

## Example
Send a request to the API using `Authorization: Bearer` with this JSON object:

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
  "temperature": 0,
  "audio":1,
  "lang": "zh-TW"
}
```

```bash
curl -X POST "https://example.com" -H "accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer <your_secret_token>" -d '{"context": {"data": {"Apples": "0.90 kg","Bananas": "1.43 kg","Barley": "0.24 kg","Beef": "36.44 kg"}}, "question": "Given this data of CO2 emissions per material, explain the impact in a concise way.", "temperature": 0, "audio":1, "lang": "zh-TW"}'
```

Response:

```json
{
    "response": "这些数据显示了不同材料的二氧化碳排放量。牛肉的排放量最高，是其他三种材料的数十倍。如果人们想要减少生态足迹，一种途径是减少高排放食物（如牛肉）的消费，增加低排放食物（如苹果和大麦）的摄入。",
    "audio_url": "https://example.com/audio/745ec180cc3344d58896199ef9e921d5.mp3"
}
```
## Supported languages
Disclaimer: Test before use, not all of them were tested

'af': Afrikaans, 'ar': Arabic, 'bg': Bulgarian, 'bn': Bengali, 'bs': Bosnian, 'ca': Catalan, 'cs': Czech, 'da': Danish, 'de': German, 'el': Greek, 'en': English, 'es': Spanish, 'et': Estonian, 'fi': Finnish, 'fr': French, 'gu': Gujarati, 'hi': Hindi, 'hr': Croatian, 'hu': Hungarian, 'id': Indonesian, 'is': Icelandic, 'it': Italian, 'iw': Hebrew, 'ja': Japanese, 'jw': Javanese, 'km': Khmer, 'kn': Kannada, 'ko': Korean, 'la': Latin, 'lv': Latvian, 'ml': Malayalam, 'mr': Marathi, 'ms': Malay, 'my': Myanmar (Burmese), 'ne': Nepali, 'nl': Dutch, 'no': Norwegian, 'pl': Polish, 'pt': Portuguese, 'ro': Romanian, 'ru': Russian, 'si': Sinhala, 'sk': Slovak, 'sq': Albanian, 'sr': Serbian, 'su': Sundanese, 'sv': Swedish, 'sw': Swahili, 'ta': Tamil, 'te': Telugu, 'th': Thai, 'tl': Filipino, 'tr': Turkish, 'uk': Ukrainian, 'ur': Urdu, 'vi': Vietnamese, 'zh-CN': Chinese (Simplified), 'zh-TW': Chinese (Mandarin/Taiwan), 'zh': Chinese (Mandarin).

## License

MIT License

Copyright (c) 2023 Vizzuality

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.