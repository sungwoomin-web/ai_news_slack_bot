from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    name: str
    kind: str
    category_hint: str
    url: str
    feed_url: str | None = None


SOURCES: list[Source] = [
    Source(
        name="OpenAI Newsroom",
        kind="official",
        category_hint="AI 전반",
        url="https://openai.com/newsroom",
        feed_url="https://openai.com/news/rss.xml",
    ),
    Source(
        name="Anthropic News",
        kind="official",
        category_hint="AI 전반",
        url="https://www.anthropic.com/news",
        feed_url="https://www.anthropic.com/news/rss.xml",
    ),
    Source(
        name="Google DeepMind",
        kind="official",
        category_hint="AI 전반",
        url="https://deepmind.google/discover/blog/",
        feed_url="https://deepmind.google/discover/blog/rss.xml",
    ),
    Source(
        name="Qwen / Alibaba Cloud",
        kind="official",
        category_hint="AI 전반",
        url="https://www.alibabacloud.com/en/solutions/generative-ai/qwen",
        feed_url="https://www.alibabacloud.com/blog/rss",
    ),
    Source(
        name="Deepgram Learn",
        kind="official",
        category_hint="STT·TTS",
        url="https://deepgram.com/learn",
        feed_url="https://deepgram.com/learn/rss.xml",
    ),
    Source(
        name="ElevenLabs Blog",
        kind="official",
        category_hint="STT·TTS",
        url="https://elevenlabs.io/blog",
        feed_url="https://elevenlabs.io/blog/rss.xml",
    ),
    Source(
        name="AssemblyAI Blog",
        kind="official",
        category_hint="STT·TTS",
        url="https://www.assemblyai.com/blog",
        feed_url="https://www.assemblyai.com/blog/rss.xml",
    ),
    Source(
        name="Cartesia Blog",
        kind="official",
        category_hint="STT·TTS",
        url="https://cartesia.ai/blog",
        feed_url="https://cartesia.ai/blog/rss.xml",
    ),
    Source(
        name="AWS Contact Center",
        kind="official",
        category_hint="AICC",
        url="https://aws.amazon.com/blogs/contact-center/",
        feed_url="https://aws.amazon.com/blogs/contact-center/feed/",
    ),
    Source(
        name="Google Cloud Contact Center",
        kind="official",
        category_hint="AICC",
        url="https://cloud.google.com/solutions/contact-center-ai-platform",
        feed_url="https://cloud.google.com/blog/rss/",
    ),
    Source(
        name="LG U+ Newsroom",
        kind="official",
        category_hint="AICC",
        url="https://news.lguplus.com/tag/agenticaicc",
    ),
    Source(
        name="Kakao Enterprise Press",
        kind="official",
        category_hint="AICC",
        url="https://kakaoenterprise.com/press/",
    ),
    Source(
        name="NAVER Cloud",
        kind="official",
        category_hint="AICC",
        url="https://www.navercloudcorp.com/",
    ),
    Source(
        name="GeekNews",
        kind="community",
        category_hint="AI 전반",
        url="https://news.hada.io/",
        feed_url="https://news.hada.io/rss",
    ),
]
