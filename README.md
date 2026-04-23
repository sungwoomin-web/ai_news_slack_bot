# Weekly AI News Slack Bot

매주 `AI 전반 / STT·TTS / AICC` 관련 뉴스를 모아 Top 5를 선정하고 슬랙 채널에 자동 발행하는 MVP입니다.

## What It Does

- RSS 기반으로 공식 소스와 보조 소스를 수집합니다.
- Vertex AI의 Anthropic Claude로 Top 5를 고르고 3줄 요약을 만듭니다.
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
gcloud auth application-default login
python main.py --dry-run
```

## Environment Variables

```env
GOOGLE_CLOUD_PROJECT=
VERTEX_REGION=us-east5
ANTHROPIC_VERTEX_MODEL=claude-sonnet-4@20250514
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
- GCP에서는 Vertex AI API를 활성화해야 합니다.
- Anthropic 공식 Vertex AI 문서 기준으로 `AnthropicVertex` 클라이언트를 사용합니다.
- 기본 모델은 2026-04-23 기준 Vertex AI 문서에서 확인된 `claude-sonnet-4@20250514`로 설정했습니다.
