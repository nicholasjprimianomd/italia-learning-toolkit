from __future__ import annotations

import asyncio
import random

import flet as ft

from app.chat_client import ChatClient, ChatClientError, ChatMessage
from config import OPENAI_API_KEY
from data import (
    ARTICLE_OPTIONS,
    ARTICLE_QUESTIONS,
    PREPOSITION_QUESTIONS,
    REFERENCE_SECTIONS,
    VERB_OPTIONS,
    VERB_QUESTIONS,
)

SIDEBAR_BG = "#1f2530"
CARD_BG = "#151b24"
CHAT_PANEL_BG = "#1c2230"
ASSISTANT_BUBBLE_BG = "#1f2530"


def safe_update(*controls: ft.Control | None) -> None:
    for control in controls:
        if control is not None and getattr(control, "page", None):
            control.update()


class ReferenceView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.selected_index = 0
        self.topic_tiles: list[ft.ListTile] = []
        self.title_text = ft.Text(
            REFERENCE_SECTIONS[self.selected_index]["title"],
            weight=ft.FontWeight.BOLD,
            size=20,
            color=ft.Colors.WHITE,
        )
        self.reference_text = ft.Text(
            REFERENCE_SECTIONS[self.selected_index]["content"],
            selectable=True,
            expand=True,
            size=13,
            no_wrap=False,
            color=ft.Colors.WHITE,
        )
        self.view = self._build()

    def _build(self) -> ft.Control:
        self.topic_tiles = [self._build_tile(i, section["title"]) for i, section in enumerate(REFERENCE_SECTIONS)]

        sidebar = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Topics", weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.WHITE),
                    ft.Divider(height=1),
                    ft.Column(
                        controls=self.topic_tiles,
                        spacing=2,
                        expand=True,
                    ),
                ],
                expand=True,
                spacing=12,
            ),
            padding=12,
            width=280,
            bgcolor=SIDEBAR_BG,
            border_radius=12,
        )

        content_panel = ft.Container(
            content=ft.Column(
                [
                    self.title_text,
                    ft.Divider(),
                    self.reference_text,
                ],
                expand=True,
                spacing=16,
            ),
            expand=True,
            bgcolor=CARD_BG,
            border_radius=12,
            padding=20,
        )

        return ft.Row(
            controls=[sidebar, content_panel],
            expand=1,
        )

    def _build_tile(self, index: int, title: str) -> ft.ListTile:
        return ft.ListTile(
            title=ft.Text(title, color=ft.Colors.WHITE),
            selected=index == self.selected_index,
            on_click=lambda _: self._select_topic(index),
        )

    def _select_topic(self, index: int) -> None:
        self.selected_index = index
        for i, tile in enumerate(self.topic_tiles):
            tile.selected = i == index
            safe_update(tile)

        section = REFERENCE_SECTIONS[index]
        self.title_text.value = section["title"]
        self.reference_text.value = section["content"]
        safe_update(self.title_text, self.reference_text)

    def prime(self) -> None:
        safe_update(self.title_text, self.reference_text, *self.topic_tiles)


class ArticleExerciseView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.questions = ARTICLE_QUESTIONS
        self.options = ARTICLE_OPTIONS

        self.current: dict[str, str] | None = None
        self.score = 0
        self.total = 0

        self.prompt_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.option_group = ft.RadioGroup(
            content=ft.Column(
                controls=[ft.Radio(value=option, label=option) for option in self.options],
                spacing=8,
            )
        )
        self.feedback_text = ft.Text("", size=14)
        self.explanation_text = ft.Text("", size=13, color=ft.Colors.ON_SURFACE_VARIANT)
        self.score_text = ft.Text("Score: 0 / 0", weight=ft.FontWeight.BOLD)

        actions = ft.Row(
            [
                ft.ElevatedButton("Check answer", icon="check_circle", on_click=self._on_check_answer),
                ft.OutlinedButton("New question", icon="refresh", on_click=self._on_new_question),
            ],
            spacing=12,
        )

        self.view = ft.Column(
            [
                ft.Text("Pick the correct definite article", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Match the article to gender, number, and sound.", size=14, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Divider(),
                self.prompt_text,
                self.option_group,
                actions,
                self.feedback_text,
                self.explanation_text,
                ft.Divider(height=24),
                self.score_text,
            ],
            spacing=16,
            expand=True,
        )

        self._load_new_question()

    def _load_new_question(self) -> None:
        self.current = random.choice(self.questions)
        prompt = (
            f"Which article matches {self.current['english']}? "
            f"({self.current['italian']} • {self.current['number']} {self.current['gender']})"
        )
        self.prompt_text.value = prompt

        self.option_group.value = None

        self.feedback_text.value = ""

        self.explanation_text.value = ""

        safe_update(self.prompt_text, self.option_group, self.feedback_text, self.explanation_text)

        self._update_score_text()

    def _on_new_question(self, _: ft.ControlEvent) -> None:
        self._load_new_question()

    def _on_check_answer(self, _: ft.ControlEvent) -> None:
        if not self.option_group.value:
            self._show_snack_bar("Select an article before checking.")
            return

        assert self.current is not None
        choice = self.option_group.value

        self.total += 1
        if choice == self.current["correct"]:
            self.score += 1
            self.feedback_text.value = "✔ Correct!"
            self.feedback_text.color = ft.Colors.GREEN_400
        else:
            self.feedback_text.value = f"✘ Not quite. The correct article is {self.current['correct']}."
            self.feedback_text.color = ft.Colors.RED_400

        self.explanation_text.value = self.current["explanation"]

        safe_update(self.feedback_text, self.explanation_text)

        self._update_score_text()

    def _update_score_text(self) -> None:
        if self.total == 0:
            self.score_text.value = "Score: 0 / 0"
        else:
            percent = (self.score / self.total) * 100
            self.score_text.value = f"Score: {self.score} / {self.total} ({percent:.0f}%)"
        safe_update(self.score_text)

    def _show_snack_bar(self, message: str) -> None:
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()


class VerbExerciseView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.questions = VERB_QUESTIONS
        self.options = VERB_OPTIONS

        self.current: dict[str, str] | None = None
        self.score = 0
        self.total = 0

        self.prompt_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.option_group = ft.RadioGroup(
            content=ft.Column(
                controls=[ft.Radio(value=option, label=option) for option in self.options],
                spacing=8,
            )
        )
        self.feedback_text = ft.Text("", size=14)
        self.explanation_text = ft.Text("", size=13, color=ft.Colors.ON_SURFACE_VARIANT)
        self.score_text = ft.Text("Score: 0 / 0", weight=ft.FontWeight.BOLD)

        actions = ft.Row(
            [
                ft.ElevatedButton("Check answer", icon="check_circle", on_click=self._on_check_answer),
                ft.OutlinedButton("New question", icon="refresh", on_click=self._on_new_question),
            ],
            spacing=12,
        )

        self.view = ft.Column(
            [
                ft.Text("Match verbs with pronouns", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Decide whether the sentence needs essere, stare, or avere — then pick the right conjugation.",
                    size=14,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Divider(),
                self.prompt_text,
                self.option_group,
                actions,
                self.feedback_text,
                self.explanation_text,
                ft.Divider(height=24),
                self.score_text,
            ],
            spacing=16,
            expand=True,
        )

        self._load_new_question()

    def _load_new_question(self) -> None:
        self.current = random.choice(self.questions)
        prompt = (
            f"Select the correct form of '{self.current['verb']}' for pronoun '{self.current['pronoun']}' "
            f"({self.current['english']})."
        )
        self.prompt_text.value = prompt

        self.option_group.value = None

        self.feedback_text.value = ""

        self.explanation_text.value = ""

        safe_update(self.prompt_text, self.option_group, self.feedback_text, self.explanation_text)

        self._update_score_text()

    def _on_new_question(self, _: ft.ControlEvent) -> None:
        self._load_new_question()

    def _on_check_answer(self, _: ft.ControlEvent) -> None:
        if not self.option_group.value:
            self._show_snack_bar("Select a verb form before checking.")
            return

        assert self.current is not None
        choice = self.option_group.value

        self.total += 1
        if choice == self.current["correct"]:
            self.score += 1
            self.feedback_text.value = "✔ Correct!"
            self.feedback_text.color = ft.Colors.GREEN_400
        else:
            self.feedback_text.value = f"✘ Not quite. The correct form is '{self.current['correct']}'."
            self.feedback_text.color = ft.Colors.RED_400

        self.explanation_text.value = self.current["explanation"]
        safe_update(self.feedback_text, self.explanation_text)

        self._update_score_text()

    def _update_score_text(self) -> None:
        if self.total == 0:
            self.score_text.value = "Score: 0 / 0"
        else:
            percent = (self.score / self.total) * 100
            self.score_text.value = f"Score: {self.score} / {self.total} ({percent:.0f}%)"
        safe_update(self.score_text)

    def _show_snack_bar(self, message: str) -> None:
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()


class PrepositionExerciseView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.questions = PREPOSITION_QUESTIONS

        self.current: dict[str, str] | None = None
        self.score = 0
        self.total = 0

        self.prompt_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.options_column = ft.Column(spacing=8)
        self.option_group = ft.RadioGroup(content=self.options_column)
        self.feedback_text = ft.Text("", size=14)
        self.explanation_text = ft.Text("", size=13, color=ft.Colors.ON_SURFACE_VARIANT)
        self.score_text = ft.Text("Score: 0 / 0", weight=ft.FontWeight.BOLD)

        actions = ft.Row(
            [
                ft.ElevatedButton("Check answer", icon="check_circle", on_click=self._on_check_answer),
                ft.OutlinedButton("New question", icon="refresh", on_click=self._on_new_question),
            ],
            spacing=12,
        )

        self.view = ft.Column(
            [
                ft.Text("Combine prepositions and articles", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Choose the correct fused form (preposizione articolata) for the prompt.",
                    size=14,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Divider(),
                self.prompt_text,
                self.option_group,
                actions,
                self.feedback_text,
                self.explanation_text,
                ft.Divider(height=24),
                self.score_text,
            ],
            spacing=16,
            expand=True,
        )

        self._load_new_question()

    def _load_new_question(self) -> None:
        self.current = random.choice(self.questions)
        prompt = (
            f"Combine '{self.current['preposition']}' with '{self.current['article_phrase']}' "
            f"({self.current['english']})."
        )
        self.prompt_text.value = prompt

        choices = {self.current["result"]}
        while len(choices) < min(4, len(self.questions)):
            choices.add(random.choice(self.questions)["result"])
        options = list(choices)
        random.shuffle(options)

        self.options_column.controls = [ft.Radio(value=option, label=option) for option in options]
        self.option_group.value = None

        self.feedback_text.value = ""

        self.explanation_text.value = ""

        safe_update(self.prompt_text, self.options_column, self.option_group, self.feedback_text, self.explanation_text)

        self._update_score_text()

    def _on_new_question(self, _: ft.ControlEvent) -> None:
        self._load_new_question()

    def _on_check_answer(self, _: ft.ControlEvent) -> None:
        if not self.option_group.value:
            self._show_snack_bar("Select an option before checking.")
            return

        assert self.current is not None
        choice = self.option_group.value

        self.total += 1
        if choice == self.current["result"]:
            self.score += 1
            self.feedback_text.value = "✔ Correct!"
            self.feedback_text.color = ft.Colors.GREEN_400
        else:
            self.feedback_text.value = f"✘ Not quite. The correct form is '{self.current['result']}'."
            self.feedback_text.color = ft.Colors.RED_400

        self.explanation_text.value = self.current["explanation"]
        safe_update(self.feedback_text, self.explanation_text)

        self._update_score_text()

    def _update_score_text(self) -> None:
        if self.total == 0:
            self.score_text.value = "Score: 0 / 0"
        else:
            percent = (self.score / self.total) * 100
            self.score_text.value = f"Score: {self.score} / {self.total} ({percent:.0f}%)"
        safe_update(self.score_text)

    def _show_snack_bar(self, message: str) -> None:
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()


class ChatView:
    MODELS = ["gpt-4o-mini", "gpt-4o"]

    def __init__(self, page: ft.Page, chat_client: ChatClient) -> None:
        self.page = page
        self.client = chat_client
        self.messages: list[ChatMessage] = [
            ChatMessage(
                role="system",
                content=(
                    "You are a friendly Italian tutor. Provide concise explanations and examples that reinforce Italian "
                    "vocabulary and grammar concepts."
                ),
            )
        ]

        self.model_dropdown = ft.Dropdown(
            label="Model",
            options=[ft.dropdown.Option(model) for model in self.MODELS],
            value=self.client.default_model if self.client.default_model in self.MODELS else self.MODELS[0],
            width=220,
        )
        self.status_text = ft.Text("", size=12, color=ft.Colors.ON_SURFACE_VARIANT)
        self.messages_view = ft.ListView(expand=True, spacing=10, auto_scroll=True, height=420)
        self.input_field = ft.TextField(
            label="Ask a question or describe what you are practising...",
            multiline=True,
            min_lines=3,
            max_lines=5,
            expand=True,
        )
        self.send_button = ft.ElevatedButton("Send", icon="send_rounded", on_click=self._on_send_message)
        clear_button = ft.OutlinedButton(
            "Clear conversation",
            icon="clear_all_rounded",
            on_click=self._on_clear_conversation,
        )

        header = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Chat with ChatGPT", size=20, weight=ft.FontWeight.BOLD),
                        self.status_text,
                    ],
                    expand=True,
                ),
                self.model_dropdown,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        footer = ft.Row([self.send_button, clear_button], spacing=12)

        self.view = ft.Column(
            [
                header,
                ft.Divider(),
                ft.Container(self.messages_view, bgcolor=CHAT_PANEL_BG, padding=12, border_radius=12),
                self.input_field,
                footer,
            ],
            spacing=16,
            expand=True,
        )

        self._refresh_api_status()

    def _refresh_api_status(self) -> None:
        if self.client.api_key:
            self.status_text.value = "API key loaded."
            self.status_text.color = ft.Colors.GREEN_400
        else:
            self.status_text.value = (
                "No API key detected. Set OPENAI_API_KEY in your environment or config.py to enable chatting."
            )
            self.status_text.color = ft.Colors.RED_400
        safe_update(self.status_text)

    def _append_message(self, speaker: str, message: str, is_user: bool) -> None:
        bubble_color = ft.Colors.BLUE_100 if is_user else ASSISTANT_BUBBLE_BG
        alignment = ft.alignment.center_right if is_user else ft.alignment.center_left
        text_align = ft.TextAlign.RIGHT if is_user else ft.TextAlign.LEFT

        bubble = ft.Container(
            content=ft.Column(
                [
                    ft.Text(speaker, size=12, color=ft.Colors.ON_SURFACE_VARIANT, text_align=text_align),
                    ft.Text(message, selectable=True, size=14, text_align=text_align),
                ],
                tight=True,
                spacing=2,
            ),
            bgcolor=bubble_color,
            padding=12,
            border_radius=12,
            alignment=alignment,
        )
        self.messages_view.controls.append(bubble)
        safe_update(self.messages_view)

    def _on_send_message(self, _: ft.ControlEvent) -> None:
        content = (self.input_field.value or "").strip()
        if not content:
            self._show_snack_bar("Write something before sending.")
            return

        user_message = ChatMessage(role="user", content=content)
        self.messages.append(user_message)
        self._append_message("You", content, is_user=True)

        self.input_field.value = ""
        safe_update(self.input_field)

        self.send_button.disabled = True
        safe_update(self.send_button)
        self._set_status("Contacting ChatGPT...", ft.Colors.ON_SURFACE_VARIANT)

        self.page.run_task(self._fetch_reply())

    async def _fetch_reply(self) -> None:
        try:
            reply = await asyncio.to_thread(
                self.client.send_chat,
                self.messages,
                model=self.model_dropdown.value,
            )
        except ChatClientError as exc:
            self.messages.pop()
            self._set_status(str(exc), ft.Colors.RED_400)
            self._show_snack_bar(str(exc))
            self.send_button.disabled = False
            safe_update(self.send_button)
            return

        assistant_message = ChatMessage(role="assistant", content=reply)
        self.messages.append(assistant_message)
        self._append_message("ChatGPT", reply, is_user=False)
        self._set_status("Reply received.", ft.Colors.GREEN_400)

        self.send_button.disabled = False
        safe_update(self.send_button)

    def _on_clear_conversation(self, _: ft.ControlEvent) -> None:
        self.messages = self.messages[:1]
        self.messages_view.controls.clear()
        safe_update(self.messages_view)
        self._set_status("Conversation cleared.", ft.Colors.ON_SURFACE_VARIANT)

    def _set_status(self, message: str, color: str) -> None:
        self.status_text.value = message
        self.status_text.color = color
        safe_update(self.status_text)

    def _show_snack_bar(self, message: str) -> None:
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()


def main(page: ft.Page) -> None:
    page.title = "Italian Learning Toolkit"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    
    # Only set window size for desktop apps (not web)
    import os
    if os.getenv("FLET_WEB_MODE", "").lower() != "true":
        try:
            page.window_width = 1200
            page.window_height = 800
        except AttributeError:
            # Window properties not available (web mode)
            pass

    theme_switch = ft.Switch(label="Dark mode", value=True)

    def toggle_theme(e: ft.ControlEvent) -> None:
        page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        page.update()

    theme_switch.on_change = toggle_theme

    page.appbar = ft.AppBar(
        title=ft.Text("Italian Learning Toolkit"),
        center_title=False,
        actions=[ft.Container(theme_switch, padding=ft.padding.only(right=16))],
    )

    reference_view = ReferenceView(page)
    article_view = ArticleExerciseView(page)
    verb_view = VerbExerciseView(page)
    preposition_view = PrepositionExerciseView(page)
    chat_view = ChatView(page, ChatClient(OPENAI_API_KEY))

    practice_tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Articles", content=ft.Column([article_view.view], expand=1)),
            ft.Tab(text="Verbs", content=ft.Column([verb_view.view], expand=1)),
            ft.Tab(text="Prepositions", content=ft.Column([preposition_view.view], expand=1)),
        ],
        expand=1,
        animation_duration=250,
    )

    main_tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Reference", content=ft.Column([reference_view.view], expand=1)),
            ft.Tab(text="Practice", content=ft.Column([practice_tabs], expand=1)),
            ft.Tab(text="Chat", content=ft.Column([chat_view.view], expand=1)),
        ],
        expand=1,
        animation_duration=250,
    )

    page.add(ft.Column([main_tabs], expand=1))
    reference_view.prime()
    page.update()


if __name__ == "__main__":
    # Run in web mode for cloud deployment
    # Use: ft.app(target=main, view=ft.AppView.WEB_BROWSER) for web-only
    # Or: ft.app(target=main) for desktop with web option
    import os
    if os.getenv("FLET_WEB_MODE", "").lower() == "true":
        ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=int(os.getenv("PORT", "8550")))
    else:
        ft.app(target=main)

