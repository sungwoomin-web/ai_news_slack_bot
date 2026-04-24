from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    name: str
    kind: str
    category_hint: str
    url: str
    feed_url: str | None = None
    priority: int = 0


SOURCES: list[Source] = [
    Source(
        name="OpenAI Newsroom",
        kind="official",
        category_hint="AI 전반",
        url="https://openai.com/newsroom",
        feed_url="https://openai.com/news/rss.xml",
        priority=2,
    ),
    Source(
        name="Anthropic News",
        kind="official",
        category_hint="AI 전반",
        url="https://www.anthropic.com/news",
        feed_url="https://www.anthropic.com/news/rss.xml",
        priority=2,
    ),
    Source(
        name="Google DeepMind",
        kind="official",
        category_hint="AI 전반",
        url="https://deepmind.google/discover/blog/",
        feed_url="https://deepmind.google/discover/blog/rss.xml",
        priority=2,
    ),
    Source(
        name="Qwen / Alibaba Cloud",
        kind="official",
        category_hint="AI 전반",
        url="https://www.alibabacloud.com/en/solutions/generative-ai/qwen",
        feed_url="https://www.alibabacloud.com/blog/rss",
        priority=1,
    ),
    Source(
        name="Deepgram Learn",
        kind="official",
        category_hint="STT·TTS",
        url="https://deepgram.com/learn",
        feed_url="https://deepgram.com/learn/rss.xml",
        priority=2,
    ),
    Source(
        name="ElevenLabs Blog",
        kind="official",
        category_hint="STT·TTS",
        url="https://elevenlabs.io/blog",
        feed_url="https://elevenlabs.io/blog/rss.xml",
        priority=2,
    ),
    Source(
        name="AssemblyAI Blog",
        kind="official",
        category_hint="STT·TTS",
        url="https://www.assemblyai.com/blog",
        feed_url="https://www.assemblyai.com/blog/rss.xml",
        priority=2,
    ),
    Source(
        name="Cartesia Blog",
        kind="official",
        category_hint="STT·TTS",
        url="https://cartesia.ai/blog",
        feed_url="https://cartesia.ai/blog/rss.xml",
        priority=1,
    ),
    Source(
        name="AWS Contact Center",
        kind="official",
        category_hint="AICC",
        url="https://aws.amazon.com/blogs/contact-center/",
        feed_url="https://aws.amazon.com/blogs/contact-center/feed/",
        priority=2,
    ),
    Source(
        name="Google Cloud Contact Center",
        kind="official",
        category_hint="AICC",
        url="https://cloud.google.com/solutions/contact-center-ai-platform",
        feed_url="https://cloud.google.com/blog/rss/",
        priority=2,
    ),
    Source(
        name="Google Cloud Blog",
        kind="official",
        category_hint="챗봇",
        url="https://cloud.google.com/blog",
        feed_url="https://cloud.google.com/blog/rss/",
        priority=1,
    ),
    Source(
        name="Azure AI Blog",
        kind="official",
        category_hint="챗봇",
        url="https://techcommunity.microsoft.com/category/azure-ai/blog/azure-ai-services-blog",
        feed_url="https://techcommunity.microsoft.com/gxcuf89792/rss/board?board.id=AzureAI",
        priority=1,
    ),
    Source(
        name="Kakao Enterprise Press",
        kind="official",
        category_hint="챗봇",
        url="https://kakaoenterprise.com/press/",
        priority=1,
    ),
    Source(
        name="LG U+ Newsroom",
        kind="official",
        category_hint="AICC",
        url="https://news.lguplus.com/tag/agenticaicc",
        priority=2,
    ),
    Source(
        name="NAVER Cloud",
        kind="official",
        category_hint="챗봇",
        url="https://www.navercloudcorp.com/",
        priority=1,
    ),
    Source(
        name="GeekNews",
        kind="priority_curated",
        category_hint="AI 전반",
        url="https://news.hada.io/",
        feed_url="https://news.hada.io/rss",
        priority=3,
    ),
]
