# Version: 0.3.0

from __future__ import annotations

import os

os.environ.setdefault(
    "TOKENIZERS_PARALLELISM",
    "false",
)

import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any

import numpy as np
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer


APP_VERSION = "0.3.0"
PIPELINE_VERSION = "verified-rag-v3"

EMBEDDING_MODEL_NAME = (
    "intfloat/multilingual-e5-small"
)

DEFAULT_CHAT_MODEL = "Qwen3-30B-A3B"
DEFAULT_TOP_K = 12


class QuranRAGPipeline:
    """
    Retrieve Quran verses semantically and use an LLM
    only to select directly relevant trusted sources.
    """

    def __init__(
        self,
        project_root: Path,
    ) -> None:
        self.project_root = project_root

        load_dotenv(
            self.project_root / ".env"
        )

        self.dataset_path = (
            self.project_root
            / "data"
            / "processed"
            / "quran_dataset_clean.json"
        )

        self.embeddings_path = (
            self.project_root
            / "data"
            / "embeddings"
            / "quran_embeddings.npy"
        )

        self.cache_directory = (
            self.project_root
            / "data"
            / "cache"
        )

        self.cache_path = (
            self.cache_directory
            / "streamlit_response_cache.json"
        )

        self.api_key = os.getenv(
            "ARVAN_AI_API_KEY"
        )

        self.base_url = os.getenv(
            "ARVAN_CHAT_URL"
        )

        self.chat_model = os.getenv(
            "ARVAN_CHAT_MODEL",
            DEFAULT_CHAT_MODEL,
        )

        self._validate_configuration()

        self.cache_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.dataset_path,
            "r",
            encoding="utf-8",
        ) as file:
            self.quran_data = json.load(file)

        self.quran_embeddings = np.load(
            self.embeddings_path
        )

        if len(self.quran_data) != len(
            self.quran_embeddings
        ):
            raise ValueError(
                "Dataset and embeddings have "
                "different lengths."
            )

        self.embedding_model = (
            SentenceTransformer(
                EMBEDDING_MODEL_NAME,
                device="cpu",
            )
        )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        self.response_cache = (
            self._load_response_cache()
        )

    def _validate_configuration(
        self,
    ) -> None:
        """
        Validate required files and environment variables.
        """
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset file not found: "
                f"{self.dataset_path}"
            )

        if not self.embeddings_path.exists():
            raise FileNotFoundError(
                f"Embeddings file not found: "
                f"{self.embeddings_path}"
            )

        if not self.api_key:
            raise ValueError(
                "ARVAN_AI_API_KEY is missing "
                "from .env."
            )

        if not self.base_url:
            raise ValueError(
                "ARVAN_CHAT_URL is missing "
                "from .env."
            )

    def _load_response_cache(
        self,
    ) -> dict[str, Any]:
        """
        Load response cache from disk.
        """
        if not self.cache_path.exists():
            return {}

        try:
            with open(
                self.cache_path,
                "r",
                encoding="utf-8",
            ) as file:
                cache_data = json.load(file)

            if isinstance(cache_data, dict):
                return cache_data

        except (
            OSError,
            json.JSONDecodeError,
        ):
            pass

        return {}

    def _save_response_cache(
        self,
    ) -> None:
        """
        Save response cache atomically.
        """
        temporary_path = (
            self.cache_path.with_suffix(
                ".tmp"
            )
        )

        with open(
            temporary_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.response_cache,
                file,
                ensure_ascii=False,
                indent=2,
            )

        temporary_path.replace(
            self.cache_path
        )

    def _make_cache_key(
        self,
        question: str,
        top_k: int,
    ) -> str:
        """
        Build a versioned response cache key.
        """
        payload = {
            "pipeline_version": (
                PIPELINE_VERSION
            ),
            "question": question.strip(),
            "top_k": top_k,
            "embedding_model": (
                EMBEDDING_MODEL_NAME
            ),
            "chat_model": self.chat_model,
        }

        serialized_payload = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
        )

        return hashlib.sha256(
            serialized_payload.encode(
                "utf-8"
            )
        ).hexdigest()

    @staticmethod
    def _normalize_question(
        question: str,
    ) -> str:
        """
        Normalize common Persian and Arabic characters.
        """
        normalized = (
            question
            .strip()
            .lower()
        )

        replacements = {
            "ي": "ی",
            "ك": "ک",
            "ۀ": "ه",
            "ة": "ه",
            "ؤ": "و",
            "إ": "ا",
            "أ": "ا",
            "ٱ": "ا",
        }

        for old_char, new_char in (
            replacements.items()
        ):
            normalized = normalized.replace(
                old_char,
                new_char,
            )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        )

        return normalized.strip()

    def _expand_question(
        self,
        question: str,
    ) -> list[str]:
        """
        Add controlled Persian semantic variants.
        """
        normalized = self._normalize_question(
            question
        )

        expanded_queries = [
            question.strip()
        ]

        expansion_rules = [
            {
                "triggers": [
                    "متنفر",
                    "نفرت",
                    "بدش می آید",
                    "بدش می‌آید",
                    "دوست ندارد",
                ],
                "queries": [
                    "خدا چه کسانی را دوست ندارد؟",
                    "خدا خیانتکار ناسپاس را دوست ندارد",
                    "خدا مفسدان را دوست ندارد",
                    "خدا ستمکاران را دوست ندارد",
                    "خشم خدا بر چه کسانی است؟",
                    "چه کسانی مورد لعنت خدا هستند؟",
                ],
            },
            {
                "triggers": [
                    "محبوب خدا",
                    "دوست دارد",
                ],
                "queries": [
                    "خدا چه کسانی را دوست دارد؟",
                    "خدا نیکوکاران را دوست دارد",
                    "خدا پرهیزکاران را دوست دارد",
                    "خدا توبه کنندگان را دوست دارد",
                    "خدا صابران را دوست دارد",
                ],
            },
            {
                "triggers": [
                    "بخشیده",
                    "آمرزیده",
                    "آمرزش",
                    "می بخشد",
                    "می‌بخشد",
                ],
                "queries": [
                    "خدا چه کسانی را می آمرزد؟",
                    "خدا توبه کنندگان را می بخشد",
                    "کسانی که توبه کرده اند آمرزیده می شوند",
                    "برای چه کسانی طلب آمرزش می شود؟",
                ],
            },
            {
                "triggers": [
                    "صبر",
                    "سختی",
                    "مشکل",
                    "گرفتاری",
                ],
                "queries": [
                    "صبر در سختی",
                    "خدا با صابران است",
                    "پاداش صبر کنندگان",
                    "در برابر سختی صبر کنید",
                ],
            },
            {
                "triggers": [
                    "هدف زندگی",
                    "هدف از زندگی",
                    "برای چه زندگی",
                    "چرا زندگی",
                    "علت زندگی",
                    "معنای زندگی",
                ],
                "queries": [
                    "هدف آفرینش انسان چیست؟",
                    "هدف خلقت انسان و جن چیست؟",
                    "انسان برای چه آفریده شده است؟",
                    "جن و انسان را جز برای عبادت نیافریدم",
                    "انسان برای پرستش خدا آفریده شده است",
                    "زندگی دنیا وسیله آزمایش انسان است",
                    "مرگ و زندگی برای آزمایش انسان آفریده شدند",
                ],
            },
            {
                "triggers": [
                    "هدف آفرینش",
                    "هدف خلقت",
                    "چرا آفریده",
                    "برای چه آفریده",
                ],
                "queries": [
                    "جن و انسان را جز برای عبادت نیافریدم",
                    "هدف خلقت انسان عبادت خداست",
                    "انسان برای پرستش خدا آفریده شده است",
                    "خدا مرگ و زندگی را برای آزمایش آفرید",
                ],
            },
        ]

        for rule in expansion_rules:
            if any(
                trigger in normalized
                for trigger in rule["triggers"]
            ):
                expanded_queries.extend(
                    rule["queries"]
                )

        unique_queries = []

        for expanded_query in (
            expanded_queries
        ):
            clean_query = (
                expanded_query.strip()
            )

            if (
                clean_query
                and clean_query
                not in unique_queries
            ):
                unique_queries.append(
                    clean_query
                )

        return unique_queries

    def retrieve(
        self,
        question: str,
        top_k: int = DEFAULT_TOP_K,
    ) -> list[dict[str, Any]]:
        """
        Retrieve verses using the original question
        and controlled semantic expansions.
        """
        clean_question = question.strip()

        if not clean_question:
            raise ValueError(
                "Question must be "
                "a non-empty string."
            )

        if top_k < 1:
            raise ValueError(
                "top_k must be at least 1."
            )

        query_variants = (
            self._expand_question(
                clean_question
            )
        )

        query_inputs = [
            f"query: {query_variant}"
            for query_variant
            in query_variants
        ]

        query_embeddings = (
            self.embedding_model.encode(
                query_inputs,
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=False,
            )
        )

        all_scores = (
            query_embeddings
            @ self.quran_embeddings.T
        )

        combined_scores = np.max(
            all_scores,
            axis=0,
        )

        top_indices = np.argsort(
            combined_scores
        )[::-1][:top_k]

        results = []

        for rank, index in enumerate(
            top_indices,
            start=1,
        ):
            verse = self.quran_data[
                int(index)
            ]

            results.append(
                {
                    "rank": rank,
                    "score": float(
                        combined_scores[index]
                    ),
                    "surah": verse["surah"],
                    "ayah": verse["ayah"],
                    "arabic": verse["arabic"],
                    "fooladvand": (
                        verse["fooladvand"]
                    ),
                    "ansarian": (
                        verse["ansarian"]
                    ),
                }
            )

        return results

    @staticmethod
    def _extract_json_object(
        raw_text: str,
    ) -> dict[str, Any]:
        """
        Extract one JSON object from a model response.
        """
        clean_text = raw_text.strip()

        try:
            parsed = json.loads(
                clean_text
            )

            if isinstance(parsed, dict):
                return parsed

        except json.JSONDecodeError:
            pass

        match = re.search(
            r"\{.*?\}",
            clean_text,
            flags=re.DOTALL,
        )

        if not match:
            return {
                "selected_ranks": []
            }

        try:
            parsed = json.loads(
                match.group(0)
            )

            if isinstance(parsed, dict):
                return parsed

        except json.JSONDecodeError:
            pass

        return {
            "selected_ranks": []
        }

    def select_relevant_sources(
        self,
        question: str,
        retrieved_results: list[
            dict[str, Any]
        ],
    ) -> list[dict[str, Any]]:
        """
        Select only verses that directly answer
        the user's exact question.
        """
        candidates = []

        for result in retrieved_results:
            candidates.append(
                {
                    "rank": result["rank"],
                    "reference": (
                        f"{result['surah']}:"
                        f"{result['ayah']}"
                    ),
                    "fooladvand": (
                        result["fooladvand"]
                    ),
                    "ansarian": (
                        result["ansarian"]
                    ),
                }
            )

        prompt = f"""
You are a strict Quran source verifier.

The user question is in Persian:

{question}

The following candidate verses were retrieved:

{json.dumps(candidates, ensure_ascii=False, indent=2)}

Select candidate verses that directly or clearly answer
the meaning of the user's question.

Rules:

1. Use only the candidate verses.
2. Do not generate an answer.
3. Do not add any verse.
4. Do not explain your decision.
5. Do not select a verse only because it contains
   similar words.
6. For questions about whom God loves or does not love,
   select verses that explicitly mention love,
   lack of love, anger, curse, or enmity.
7. For questions about forgiveness, select verses that
   explicitly mention forgiveness, pardon, repentance,
   or asking forgiveness.
8. For conceptual questions such as the purpose of life,
   creation, death, worship, or testing, select verses
   that clearly express the Quranic purpose or meaning,
   even if they do not repeat the exact question words.
9. Do not select verses that merely mention worldly life
   without addressing its meaning, purpose, test,
   worship, or final destination.
10. If none clearly answer the question,
    return an empty list.
11. Return valid JSON only.

Required output:

{{"selected_ranks": [1, 2]}}
""".strip()

        response = (
            self.client
            .chat
            .completions
            .create(
                model=self.chat_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0,
                max_tokens=100,
            )
        )

        raw_output = (
            response
            .choices[0]
            .message
            .content
            or ""
        )

        parsed_output = (
            self._extract_json_object(
                raw_output
            )
        )

        selected_ranks = (
            parsed_output.get(
                "selected_ranks",
                [],
            )
        )

        if not isinstance(
            selected_ranks,
            list,
        ):
            return []

        valid_ranks = {
            result["rank"]
            for result
            in retrieved_results
        }

        normalized_ranks = []

        for rank in selected_ranks:
            try:
                normalized_rank = int(
                    rank
                )

            except (
                TypeError,
                ValueError,
            ):
                continue

            if (
                normalized_rank
                in valid_ranks
                and normalized_rank
                not in normalized_ranks
            ):
                normalized_ranks.append(
                    normalized_rank
                )

        return [
            result
            for result
            in retrieved_results
            if result["rank"]
            in normalized_ranks
        ]

    def ask(
        self,
        question: str,
        top_k: int = DEFAULT_TOP_K,
    ) -> dict[str, Any]:
        """
        Run retrieval, source verification, and caching.
        """
        clean_question = question.strip()

        if not clean_question:
            raise ValueError(
                "Question must be "
                "a non-empty string."
            )

        cache_key = self._make_cache_key(
            question=clean_question,
            top_k=top_k,
        )

        cached_result = (
            self.response_cache.get(
                cache_key
            )
        )

        if isinstance(
            cached_result,
            dict,
        ):
            result = dict(
                cached_result
            )

            result["from_cache"] = True

            return result

        retrieved_results = (
            self.retrieve(
                question=clean_question,
                top_k=top_k,
            )
        )

        selected_sources = (
            self.select_relevant_sources(
                question=clean_question,
                retrieved_results=(
                    retrieved_results
                ),
            )
        )

        result = {
            "question": clean_question,
            "sources": selected_sources,
            "retrieved_sources": (
                retrieved_results
            ),
            "embedding_model": (
                EMBEDDING_MODEL_NAME
            ),
            "generation_model": (
                self.chat_model
            ),
            "top_k": top_k,
            "from_cache": False,
            "pipeline_version": (
                PIPELINE_VERSION
            ),
        }

        self.response_cache[
            cache_key
        ] = dict(result)

        self._save_response_cache()

        return result

    def clear_response_cache(
        self,
    ) -> None:
        """
        Clear in-memory and file response cache.
        """
        self.response_cache = {}

        if self.cache_path.exists():
            self.cache_path.unlink()


def get_project_root() -> Path:
    """
    Return the project root containing app.py.
    """
    return (
        Path(__file__)
        .resolve()
        .parent
    )


@st.cache_resource(
    show_spinner=False,
)
def load_pipeline() -> QuranRAGPipeline:
    """
    Load heavy pipeline resources once.
    """
    return QuranRAGPipeline(
        project_root=get_project_root()
    )


def inject_custom_css() -> None:
    """
    Apply RTL layout and application styling.
    """
    st.markdown(
        """
        <style>
        .stApp {
            direction: rtl;
        }

        .block-container {
            max-width: 920px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, p, label {
            text-align: right;
        }

        .quran-arabic {
            direction: rtl;
            text-align: right;
            font-size: 1.55rem;
            line-height: 2.3;
            padding: 1rem 0;
        }

        .question-box {
            direction: rtl;
            text-align: right;
            border-right: 4px solid
                rgba(120, 120, 120, 0.55);
            padding: 0.8rem 1rem;
            margin-bottom: 1.2rem;
        }

        .source-reference {
            direction: rtl;
            text-align: right;
            font-weight: 700;
            margin-top: 0.8rem;
        }

        .app-note {
            direction: rtl;
            text-align: right;
            line-height: 2;
            opacity: 0.85;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_source(
    source: dict[str, Any],
) -> None:
    """
    Render one selected Quran source.
    """
    with st.container(
        border=True
    ):
        st.markdown(
            (
                f"### سوره {source['surah']}، "
                f"آیه {source['ayah']}"
            )
        )

        safe_arabic = html.escape(
            str(source["arabic"])
        )

        st.markdown(
            (
                '<div class="quran-arabic">'
                f"{safe_arabic}"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            "**ترجمه فولادوند**"
        )

        st.write(
            source["fooladvand"]
        )

        st.markdown(
            "**ترجمه انصاریان**"
        )

        st.write(
            source["ansarian"]
        )


def render_retrieved_source(
    source: dict[str, Any],
) -> None:
    """
    Render one retrieved candidate with Arabic and translations.
    """
    with st.container(
        border=True
    ):
        st.markdown(
            (
                f"**رتبه {source['rank']} — "
                f"سوره {source['surah']}، "
                f"آیه {source['ayah']}**"
            )
        )

        st.caption(
            (
                "امتیاز شباهت: "
                f"{source['score']:.4f}"
            )
        )

        safe_arabic = html.escape(
            str(source["arabic"])
        )

        st.markdown(
            (
                '<div class="quran-arabic">'
                f"{safe_arabic}"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            "**ترجمه فولادوند**"
        )

        st.write(
            source["fooladvand"]
        )

        st.markdown(
            "**ترجمه انصاریان**"
        )

        st.write(
            source["ansarian"]
        )


def render_result(
    result: dict[str, Any],
) -> None:
    """
    Render one complete verified result.
    """
    st.markdown("### پرسش")

    safe_question = html.escape(
        str(result["question"])
    )

    st.markdown(
        (
            '<div class="question-box">'
            f"{safe_question}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        "### آیات مرتبط"
    )

    selected_sources = (
        result["sources"]
    )

    if not selected_sources:
        st.warning(
            "در میان آیات بازیابی‌شده، "
            "آیه‌ای که پاسخ مستقیم یا روشن "
            "به این سؤال بدهد پیدا نشد."
        )

    else:
        for source in selected_sources:
            render_source(source)

    with st.expander(
        "مشاهده آیات اولیه بازیابی‌شده"
    ):
        for source in (
            result["retrieved_sources"]
        ):
            render_retrieved_source(
                source
            )

    if result.get(
        "from_cache",
        False,
    ):
        st.success(
            "این نتیجه از کش پاسخ‌ها "
            "بارگذاری شد."
        )

    st.caption(
        (
            f"Embedding: "
            f"{result['embedding_model']} | "
            f"Model: "
            f"{result['generation_model']} | "
            f"Top K: "
            f"{result['top_k']}"
        )
    )


def initialize_session_state() -> None:
    """
    Initialize Streamlit session values.
    """
    if "history" not in (
        st.session_state
    ):
        st.session_state.history = []


def main() -> None:
    """
    Run the Streamlit application.
    """
    st.set_page_config(
        page_title="پرسش از قرآن",
        page_icon="📖",
        layout="centered",
    )

    inject_custom_css()
    initialize_session_state()

    st.title("پرسش از قرآن")

    st.markdown(
        """
        <p class="app-note">
        سؤال خود را به فارسی بنویسید.
        سامانه ابتدا آیات مرتبط را به‌صورت معنایی
        بازیابی می‌کند و سپس فقط منابعی را نمایش
        می‌دهد که پاسخ مستقیم یا روشنی به سؤال دارند.
        متن عربی و ترجمه‌ها بدون بازنویسی مدل
        نمایش داده می‌شوند.
        </p>
        """,
        unsafe_allow_html=True,
    )

    try:
        with st.spinner(
            "در حال بارگذاری مدل و داده‌ها..."
        ):
            pipeline = load_pipeline()

    except Exception as error:
        st.error(
            "بارگذاری سامانه ناموفق بود."
        )

        st.exception(error)
        st.stop()

    with st.sidebar:
        st.header("تنظیمات")

        top_k = st.slider(
            "تعداد آیات اولیه",
            min_value=5,
            max_value=20,
            value=DEFAULT_TOP_K,
            step=1,
        )

        st.caption(
            f"نسخه برنامه: "
            f"{APP_VERSION}"
        )

        if st.button(
            "پاک کردن تاریخچه",
            use_container_width=True,
        ):
            st.session_state.history = []
            st.rerun()

        if st.button(
            "پاک کردن کش پاسخ‌ها",
            use_container_width=True,
        ):
            try:
                pipeline.clear_response_cache()

                st.session_state.history = []

                st.success(
                    "کش پاسخ‌ها پاک شد."
                )

            except Exception as error:
                st.error(
                    "پاک کردن کش ناموفق بود."
                )

                st.exception(error)

    with st.form(
        "question_form",
        clear_on_submit=False,
    ):
        question = st.text_area(
            "سؤال شما",
            placeholder=(
                "مثلاً: هدف زندگی چیست؟"
            ),
            height=110,
        )

        submitted = (
            st.form_submit_button(
                "جست‌وجو در قرآن",
                use_container_width=True,
            )
        )

    if submitted:
        clean_question = (
            question.strip()
        )

        if not clean_question:
            st.warning(
                "لطفاً یک سؤال وارد کنید."
            )

        else:
            try:
                with st.spinner(
                    "در حال بازیابی و "
                    "بررسی آیات..."
                ):
                    result = pipeline.ask(
                        question=clean_question,
                        top_k=top_k,
                    )

                st.session_state.history.insert(
                    0,
                    result,
                )

            except Exception as error:
                st.error(
                    "در پردازش سؤال "
                    "خطایی رخ داد."
                )

                st.exception(error)

    if st.session_state.history:
        st.divider()

        for index, result in enumerate(
            st.session_state.history
        ):
            render_result(result)

            if index < (
                len(
                    st.session_state.history
                )
                - 1
            ):
                st.divider()


if __name__ == "__main__":
    main()