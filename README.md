# Weekly AI News Slack Bot

매주 `AI 전반 / STT·TTS / AICC` 관련 뉴스를 모아 Top 5를 선정하고 슬랙 채널에 자동 발행하는 MVP입니다.

## What It Does

- RSS 기반으로 공식 소스와 보조 소스를 수집합니다.
- OpenAI Responses API로 Top 5를 고르고 3줄 요약을 만듭니다.
- 슬랙 메시지 포맷으로 렌더링합니다.
- 원하면 바로 슬랙에 발행합니다.

## Quick Start

1. 가상환경 생성
2. 의존성 설치
3. `.env` 작성
4. 드라이런 확인
5. 슬랙 자동화 연결

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py --dry-run
```

## Environment Variables

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5
SLACK_BOT_TOKEN=
SLACK_CHANNEL_ID=
NEWS_LOOKBACK_DAYS=7
NEWS_MAX_PER_SOURCE=12
NEWS_TOP_K=5
```

## Run

드라이런:

```bash
python main.py --dry-run
```

실제 슬랙 발행:

```bash
python main.py
```

## Output Files

- `data/articles.json`
- `data/weekly_brief.json`
- `data/weekly_message.txt`

## Notes

- 현재 수집은 RSS 우선입니다.
- 일부 국내 사이트는 RSS가 약해서 향후 HTML 파서를 추가하는 식으로 확장하면 됩니다.
- 현재 MVP는 `chat:write` 권한만 있으면 됩니다.
